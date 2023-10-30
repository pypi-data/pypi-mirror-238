"""Feature configuration."""
import importlib
import os
import pathlib
from functools import partial
from typing import Any

import toml  # pylint: disable=import-error

from fastfeatureflag.config import Config
from fastfeatureflag.errors import (
    CannotRunShadowWithoutFunctionError,
    FeatureContentNotDict,
    FeatureNotRegistered,
    WrongFeatureSchema,
)
from fastfeatureflag.feature_content import FeatureContent
from fastfeatureflag.shadow_configuration import ShadowConfiguration


class FeatureFlagConfiguration:
    """Feature configuration

    Raises:
        FileNotFoundError: When file not available
        NotImplementedError: Raised when feature was disabled,
            but was still called.
        KeyError: The configuration key:value pair does not match.
        CannotRunShadowWithoutFunctionError: The shadow method
            needs a function to run.
        FeatureNotRegistered: A feature was requested which
            hasn't been registered. Perhaps an spelling error?
        FeatureContentNotDict: The provided feature is not structured
            as a dict.
        WrongFeatureSchema: The feature configuration does not comply
            to the feature schema.
    """

    _registered_features: list[FeatureContent] = []
    _configuration: dict

    def __init__(
        self,
        feature: FeatureContent,
        shadow: str | None = None,
        fastfeatureflag_configuration: Config = Config(),
        **kwargs,
    ):
        self.__fastfeatureflag_configuration = fastfeatureflag_configuration
        self._options = kwargs
        self._shadow = shadow

        self.__check_for_configuration(feature=feature)
        self.__check_name(feature=feature)
        self.__sync_features(feature)
        self.feature = feature

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self.feature.shadow:
            return self._shadow_function(*args, **kwargs)

        return self._decorated_function(*args, **kwargs)

    def __get__(self, instance, owner):
        """
        Fix: make our decorator class a decorator, so that it also works to
        decorate instance methods.
        https://stackoverflow.com/a/30105234/10237506
        """
        return partial(self.__call__, instance)

    def __check_name(
        self,
        feature: FeatureContent,
    ):
        """Check for name

        Check if feature with given name is registered. If not, register
        new feature with name and activation.

        Args:
            feature(FeatureContent): Feature containing all information.
        """
        if feature.name:
            if not self.is_registered(feature.name):
                self.register(
                    name=feature.name,
                    feature_content={"activation": feature.activation},
                )

    def __check_for_configuration(self, feature: FeatureContent):
        """Check if configuration is available

        Check if a configuration is either available as dict or from a config file.
        If so, load the configuration.

        Args:
            configuration (dict): Configuration as dict
            configuration_path (pathlib.Path): Path to configuration
        """
        if feature.configuration:
            self._load_configuration(feature.configuration)

        if feature.configuration_path:
            configuration = self._load_configuration_from_file(
                path=feature.configuration_path
            )
            feature.configuration = configuration

        if feature.configuration_path is None and feature.configuration is None:
            (
                feature.configuration_path,
                feature.configuration,
            ) = self.__check_config_at_default_location()

    def __sync_features(self, feature):
        """Sync features.

        A loaded feature by config file etc. might differ from the
        decorated feature. They need to be synced.

        The loaded activation overwrites the decorator activation.
        The decorated function will be saved with the registered feature.
        The shadow method defined in the config will be used when no other
            shadow was provided.

        Args:
            feature (_type_): _description_
        """
        if self.is_registered(name=feature.name):
            registered_feature = self.get_feature_by_name(feature.name)
            registered_feature.func = feature.func

            if (  # TODO: exlude to seperate method
                registered_feature.activation == "off"
                or os.environ.get(registered_feature.activation) == "off"
            ):
                feature.activation = "off"

            elif (
                registered_feature.activation == "on"
                or os.environ.get(registered_feature.activation) == "on"
            ):
                feature.activation = "on"

            else:
                raise KeyError(
                    f"Wrong key. Possible keys: on|off, got: {registered_feature.activation}"
                )

            if registered_feature.response:
                feature.response = registered_feature.response

            if not feature.shadow:
                feature.shadow = registered_feature.shadow

    def __check_config_at_default_location(self):
        path_to_default_config = (
            self.__fastfeatureflag_configuration.PATH_TO_DEFAULT_CONFIGURATION
        )
        if path_to_default_config.exists():
            return path_to_default_config, self._load_configuration_from_file(
                path=path_to_default_config
            )

        return None, None

    def _load_configuration(self, configuration: dict):
        for feature in configuration:
            self.register(name=feature, feature_content=configuration.get(feature))

    def _load_configuration_from_file(self, path) -> dict[str, Any]:
        if path.exists():
            content = toml.load(path)
            self._load_configuration(configuration=content)
        else:
            raise FileNotFoundError("Config file not found") from None

        return content

    def _decorated_function(self, *args, **kwargs):
        """Function build with all parameters.

        This function is returned and executes additional steps
        before the original function (from `decorated_function`)
        is called.

        Raises:
            NotImplementedError: Raised if the feature flag is off.
            KeyError: Raised when the activation keyword is not known.

        Returns:
            object: The original/input function containing also all options.
        """
        if (
            self.feature.activation == "off"
            or os.environ.get(self.feature.activation) == "off"
        ):
            if self.feature.response:
                return self.feature.response

            raise NotImplementedError("Feature not implemented") from None

        if (
            self.feature.activation == "on"
            or os.environ.get(self.feature.activation) == "on"
        ):
            self._options = self._options | kwargs
            return self.feature.func(*args, **self._options)

        raise KeyError(
            f"Wrong key. Possible keys: on|off, got: {self.feature.activation}"
        )

    def _shadow_function(self, *args, **kwargs):
        if self.feature.activation == "on":
            return self._decorated_function(*args, **kwargs)

        if isinstance(self.feature.shadow, str):
            module, function = self.feature.shadow.rsplit(".", 1)
            run = getattr(importlib.import_module(module), function)

        if run is None or not callable(run):
            raise CannotRunShadowWithoutFunctionError() from None

        shadow_run = ShadowConfiguration(func=run, *args, **kwargs)
        return shadow_run.run()

    def update(
        self,
        activation: str = "off",
        response: Any | None = None,
        name: str | None = None,
    ):
        """Update feature(s).

        Args:
            activation (str, optional): Activation of feature. Defaults to "off".
            response (Any | None, optional): Response of decorated function. Defaults to None.
            name (str | None, optional): Name of the feature. Defaults to None.
        """
        self.feature.update(activation=activation, name=name, response=response)

        if name:
            if self.is_registered(self.feature.name):
                registered_feature = self.get_feature_by_name(self.feature.name)
                registered_feature.update(
                    activation=activation, name=name, response=response
                )
                registered_feature.func = self.feature.func
            else:
                self.register(self.feature.name or "no name provided", self.feature)

    def _sync_feature(self):
        registered_feature = self.get_feature_by_name(self.feature.name)
        if self.feature.__dict__ != registered_feature.__dict__:
            self.feature.__dict__ = registered_feature.__dict__

    @classmethod
    def get_feature_by_name(cls, name) -> FeatureContent:
        """Find feature

        Find registered feature by name.

        Args:
            name (str): Name of the registered feature

        Returns:
            dict: Feature
        """
        for feature in cls._registered_features:
            if name == feature.name:
                return feature

        raise FeatureNotRegistered

    @classmethod
    def register(cls, name: str, feature_content: dict | Any):
        """Register feature

        Register feature by name with activation.

        Args:
            name (str): Name of the feature
            activation (str): on/off
        """
        if not isinstance(feature_content, dict):
            raise FeatureContentNotDict(
                f"Feature content is type {type(feature_content)}"
            )

        if not cls.is_registered(name):
            try:
                feature = FeatureContent(name=name, **feature_content)
            except TypeError as caught_exception:
                raise WrongFeatureSchema(
                    "Feature content schema not valid. Perhaps wrong keywords have been used."
                ) from caught_exception

            cls._registered_features.append(feature)

    @classmethod
    def is_registered(cls, name):
        """Check if feature is registered

        Args:
            name (str): Feature name.

        Returns:
            bool: True|False
        """
        for feature in cls._registered_features:
            if name == feature.name:
                return True
        return False

    @classmethod
    def clean(cls):
        """Empty registered features"""
        cls._registered_features = []

    @property
    def feature_name(self) -> str | None:
        """Return feature name

        Returns:
            str: Feature name
        """
        return self.feature.name

    @property
    def feature_active(self) -> str:
        """Return activation status

        Returns:
            str: Activation: on|off
        """
        return self.feature.activation

    @property
    def registered_features(self) -> list[FeatureContent]:
        """Return list of registered features

        Returns:
            list[Feature]: List containing Feature()s
        """
        return self._registered_features

    @property
    def configuration(self) -> dict | None:
        """Return configuration

        Returns:
            dict: Configuration
        """
        return self.feature.configuration

    @configuration.setter
    def configuration(self, new_configuration):
        self.clean()
        self._load_configuration(configuration=new_configuration)
        self.__sync_features(feature=self.feature)
        self.feature.configuration = new_configuration

    @property
    def configuration_path(self) -> pathlib.Path | None:
        """Return path to configuration file

        Returns:
            pathlib.Path | None: Path to configuration file
        """
        return self.feature.configuration_path

    @configuration_path.setter
    def configuration_path(self, path: pathlib.Path):
        self.configuration = self._load_configuration_from_file(path=path)
        self.feature.configuration_path = path
