import typing

from .construct_base import ConstructBase
from .str_construct_exceptions import StrStopFieldError

class StrStopIf(ConstructBase):
    """StrStopIf is condition str-construct object that signals StrStruct to stop building
    or parsing. It raises an StrStopFieldError exception for that purpose. Therefore if used
    by itself, it raises that exception, when the condition is met.

        >>> from strconstruct import StrStopIf
        >>> d = StrStopIf(True)
        >>> d.build({})
        ...
        strconstruct.str_construct_exceptions.StrStopFieldError: Found a boolean condition
            for StopIf. Stopping
        >>> d.parse("")
        ...
        strconstruct.str_construct_exceptions.StrStopFieldError: Found a boolean condition
            for StopIf. Stopping

    The most useful application of StrStopIf is with StrStruct

        >>> packet = StrStruct(
        ...     "field1" / StrInt("d"),
        ...     StrStopIf(lambda this: this["n"]),
        ...     StrConst(","),
        ...     "field2" / StrFloat(".2f"),
        ... )
        >>> packet.build({"field1": 2}, n=True)
        '2'
        >>> packet.build({"field1": 2, "field2": 3.1}, n=True)
        '2'
        >>> packet.build({"field1": 2, "field2": 3.1}, n=False)
        '2,3.10'
        >>> packet.parse("2", n=True)
        {'field1': 2}
        >>> packet.parse("2,3.10", n=True)
        {'field1': 2}
        >>> packet.parse("2,3.10", n=False)
        {'field1': 2, 'field2': 3.1}

    """

    def __init__(self, condition: typing.Union[typing.Callable, bool]):
        """
        Args:
            condition: The condition to determine whether build/parse should be stopped.
                If it is a callable, it should accept one argument (for the context) and
                return a boolean value. If it returns True, ``StrStopFieldError`` will
                be raised by the ``build`` and ``parse`` methods.
        """
        if not isinstance(condition, bool) and not callable(condition):
            raise TypeError("Condition for StrStopIf should either be bool or callable")
        self._condition = condition
        self.name = None  # This should be done in the base class

    def _build(self, _value_, **kwargs) -> str:
        """Backend method for building. This class does not build anything. If the condition
        is not met, it simply returns an empty string.

        Args:
            _value_: The value to build. Will be ignored by this class
            **kwargs: Other values that might be provided to the build method as additional
                context.

        Returns:
            Always an empty string

        Raises:
            StrStopFieldError: If the stopping condition is met.
        """
        self._last_built = None
        ctx = kwargs
        if isinstance(self._condition, bool):
            if self._condition is True:
                raise StrStopFieldError("Found a boolean condition for StopIf. Stopping")

        # The type of self._condition has been confirmed in __init__
        elif self._condition(ctx):
            raise StrStopFieldError("The callable condition for StopIf is met. Stopping")

        return ""

    def _parse(self, string, **kwargs) -> None:

        """Backend method for parsing. This method does no parsing. If the stopping
        condition is met, it simply returns None.

        Args:
            string: The input string. Will be ignored by this class
            **kwargs: Other values that might be provided to the build method as additional
                context.

        Raises:
            StrStopFieldError: If the stopping condition is met.
        """
        ctx = kwargs
        self._parse_left = string
        if isinstance(self._condition, bool):
            if self._condition is True:
                raise StrStopFieldError("Found a boolean condition for StopIf. Stopping")
            else:
                return

        if self._condition(ctx):
            raise StrStopFieldError("The callable condition for StopIf is met. Stopping")
