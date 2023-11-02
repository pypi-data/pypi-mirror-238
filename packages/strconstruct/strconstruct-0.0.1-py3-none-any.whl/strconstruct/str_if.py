import typing

from .construct_base import ConstructBase


class StrIf(ConstructBase):
    """StrIf helps with conditional statements in the protocol declaration. If it condition
    holds, it builds and parses using the sub-StrConstruct object. If the condition does
    not hold, the ``build`` method returns an empty string and the ``parse`` method returns
    None. Note that StrStruct does not include None and empty strings.

        >>> d = StrIf(True, StrInt("d"))
        >>> d.build(2)
        '2'
        >>> d.parse("3")
        3
        >>> d = StrIf(False, StrInt("d"))
        >>> d.build(2)
        ''
        >>> d.parse("3")
        >>>

    That's just a simple example. The condition can of course be callables.

        >>> d = StrIf(lambda this: this["n"], StrInt("d"))
        >>> d.build(3, n=True)
        '3'
        >>> d.build(3, n=False)
        ''
        >>> d.parse("5", n=True)
        5
        >>> d.parse("5", n=False)
        >>>

    Even more useful in StrStruct

        >>> d = StrStruct(
        ...     "field1" / StrInt("d"),
        ...     StrConst(","),
        ...     "field2" / StrIf(lambda this: this["n"], StrFloat(".2f")),
        ... )
        >>> d.build({"field1": 2, "field2": 2.34}, n=True)
        '2,2.34'
        >>> d.build({"field1": 2, "field2": 2.34}, n=False)
        '2,'

    You see the comma at the end of the last build? StrStruct is smart when it comes to
    separators in StrConstruct objects that build nothing.

        >>> d = StrStruct(
        ...     "field1" / StrInt("d"),
        ...     "field2" / StrIf(lambda this: this["n"], StrFloat(".2f")),
        ...     separator=","
        ... )
        >>> d.build({"field1": 2, "field2": 2.34}, n=True)
        '2,2.34'
        >>> d.build({"field1": 2, "field2": 2.34}, n=False)
        '2'
        >>> d.parse("2,2.34", n=True)
        {'field1': 2, 'field2': 2.34}
        >>> d.parse("2", n=False)
        {'field1': 2}

    OK, that's better.
    """
    def __init__(self, condition: typing.Union[typing.Callable, bool], subconstruct: ConstructBase):
        """
        Args:
            condition: The condition to determine whether build/parse should be stopped.
            subconstruct: The sub-StrConstruct object. If the condition holds, parsing and
                building will be deferred to this sub-StrConstruct object.
        """
        if not isinstance(condition, bool) and not callable(condition):
            raise TypeError("Condition for StrIf should either be bool or callable")
        self._condition = condition
        self._subconstruct = subconstruct
        self.name = None  # This should be done in the base class

    def _build(self, _value_, **ctx):
        """Backend method for building

        Args:
            _value_: The value to be built
            **kwargs: Other values that might be provided to the build method as additional
                context. This value is passed on to the condition, if callable. It is also
                sent to the sub-StrConstruct when its ``build`` method is called.

        Returns:
            The built string
        """
        if (isinstance(self._condition, bool) and self._condition is True) \
                or (callable(self._condition) and self._condition(ctx) is True):
            return self._subconstruct.build(_value_, **ctx)

        return ""

    def _parse(self, string, **ctx):
        """Backend method for parsing

        Args:
            string: The input string
            **ctx: Other values that might be provided to the build method as additional
                context. It's use is similar to :func:`~StrIf._build`.

        Returns:
            The parsed content as an ``int`` object
        """
        if isinstance(self._condition, bool) and self._condition is True \
                or (callable(self._condition) and self._condition(ctx) is True):
            output = self._subconstruct.parse(string, **ctx)
            self._parse_left = self._subconstruct.parse_left()
            return output
