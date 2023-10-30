"""Configuration

This module holds all relevant configuration parts, splitted for individual use cases.
"""
import pathlib


# pylint: disable=too-few-public-methods
class Config:
    """Default configuration"""

    PATH_TO_DEFAULT_CONFIGURATION = pathlib.Path().cwd() / "fastfeatureflag_config.toml"


class TestConfig(Config):
    """Test specific configuration"""

    PATH_TO_CONFIGURATION = (
        pathlib.Path().cwd()
        / "tests"
        / "unittests"
        / "resources"
        / "fastfeatureflag_config.toml"
    )

    DEFAULT_CONFIG = config = {
        "test_feature_off": {"activation": "off"},
        "test_feature_on": {"activation": "on"},
        "test_feature_environment": {"activation": "TEST_ACTIVATION"},
        "test_shadow_method": {
            "activation": "off",
            "shadow": "tests.unittests.resources.shadow_test_method.shadow_test_method",
        },
    }

    WRONG_SCHEMA = {"wrong_schema": {"not_activation": "not_on"}}
