"""This module contains the feature flag implementation."""

import importlib
import pathlib
from functools import partial
from typing import Any, Callable

from fastfeatureflag.errors import CannotRunShadowWithoutFunctionError
from fastfeatureflag.feature_content import FeatureContent
from fastfeatureflag.feature_flag_configuration import FeatureFlagConfiguration
from fastfeatureflag.shadow_configuration import ShadowConfiguration


class feature_flag:  # pylint: disable=invalid-name
    """Feature flag

    Feature flag containing the flag and the shadow
    mode.
    """

    def __init__(
        self,
        activation: str = "off",
        response: Any | None = None,
        name: str | None = None,
        configuration: dict | None = None,
        configuration_path: pathlib.Path | None = None,
        **kwargs,
    ):
        """Initialize feature

        Initialize feature and if not registered, start the register process.

        Args:
            activation (str, optional): The activation of the feature `on|off`.
                Defaults to "off".
            response (Any | None, optional): What should an deactivated feature return.
                Defaults to None.
            name (str | None, optional): Name of the feature. Used for grouping features together.
                Defaults to None.
            configuration (dict | None, optional): Use a dict for configuring features.
                Defaults to None.
            configuration_path (pathlib.Path | None, optional): A path to a configuration toml.
                Defaults to None.
        """
        super().__init__()
        self.kwargs = kwargs

        self._feature = FeatureContent(
            activation=activation,
            name=name,
            response=response,
            configuration=configuration,
            configuration_path=configuration_path,
        )
        # TODO: COnfigure flag here, set func in __call__

        FeatureFlagConfiguration(
            feature=self._feature,
            **self.kwargs,  # TODO: shadow? Jkwargs? needed?
        )

    def __get__(self, instance, owner):
        """
        Fix: make our decorator class a decorator, so that it also works to
        decorate instance methods.
        https://stackoverflow.com/a/30105234/10237506
        """

        return partial(self.__call__, instance)

    def __call__(self, func, *args, **kwargs):
        self._feature.func = func

        return FeatureFlagConfiguration(
            feature=self._feature,
            **self.kwargs,  # TODO: shadow? Jkwargs? needed?
        )

    def shadow(self, run: Callable | str, *args, **kwargs):
        """Shadow feature

        Args:
            run (function): The alternative method which should be called.
        """
        if self._feature.activation == "on":
            return self

        if isinstance(run, str):
            module, function = run.rsplit(".", 1)
            run = getattr(importlib.import_module(module), function)

        if run is None or not callable(run):
            raise CannotRunShadowWithoutFunctionError() from None

        def decorated_function(
            func: Callable, *args, **kwargs
        ):  # pylint: disable=unused-argument
            """Inner wrapper for the decorated function.

            Args:
                func (function): The original function

            Returns:
                run: Function running the alternative function.
            """
            shadow_run = ShadowConfiguration(run, *args, **kwargs)
            return shadow_run
            # return shadow_run.run

        return decorated_function

    def pytest(self, passing: bool = True):
        """Enabling feature flag with pytest.

        Pytest expects functions (not callables). This method specifies, how a test
        should behave. Pass/Fail. Or if the feature is "on" return the original test.

        Args:
            passing (bool, optional): Outcome of the assumed test. Defaults to True.
        """

        def wrapper(func):
            def inner():
                assert passing

            if self._feature.activation == "on":
                return func

            return inner

        return wrapper
