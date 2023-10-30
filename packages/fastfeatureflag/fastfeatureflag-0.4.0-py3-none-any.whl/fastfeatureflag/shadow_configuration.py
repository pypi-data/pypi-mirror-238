"""Defining shadow configurations."""


# pylint: disable=too-few-public-methods
class ShadowConfiguration:
    """Shadow mode configuration"""

    def __init__(self, func, *args, **kwargs) -> None:
        """Loading the shadow configuration

        With this constructor, the necessary arguments are saved
        to call the shadow method form the decorated method.

        Args:
            func (function): The alternative method which should be called
                instead of the original one.
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        """Runs the alternative method.

        Runs the alternative method and together with __get__ creates a
        decorator class.

        Returns:
            Any: Returns the output from the provided alternative method.
        """
        return self.func(*args, **kwargs)

    def __get__(self, instance, owner):
        """
        Fix: make our decorator class a decorator, so that it also works to
        decorate instance methods.
        https://stackoverflow.com/a/30105234/10237506
        """
        from functools import partial

        return partial(self.__call__, instance)

    def run(self, *args, **kwargs):
        return self.func(*args, **kwargs)
