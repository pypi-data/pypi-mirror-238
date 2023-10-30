"""Feature content."""
import pathlib
from dataclasses import dataclass
from typing import Callable


# pylint: disable=too-many-instance-attributes
@dataclass
class FeatureContent:
    """Feature content.

    Defined feature by provided attributes.
    """

    activation: str
    name: str | None
    response: str | None = None
    shadow: str | None = None
    func: Callable | None = None
    configuration: dict | None = None
    configuration_path: pathlib.Path | None = None

    def update(self, **kwargs):
        """Update feature"""
        self.__dict__ = {**self.__dict__, **kwargs}
