import typing

from .construct_base import ConstructBase


class StrIfThenElse(ConstructBase):
    """StrIfThenElse is similar to StrIf except that it also accepts a second sub-StrConstruct
    object, which will be used when the condition is not met. In other words, unlike StrIf,
    StrIfThenElse always builds something.

        >>> d = StrIfThenElse(lambda this: this["n"], StrInt("d"), StrFloat(".2f"))
        >>> d.build(3, n=True)
        '3'
        >>> d.build(3, n=False)
        '3.00'
        >>> d.parse("1.23", n=True)
        1
        >>> d.parse("1.23", n=False)
        1.23

    Its use in StrConstruct is more interesting:

        >>> d = StrStruct(
        ...     "field1" / StrInt("d"),
        ...     StrConst(","),
        ...     "field2" / StrIfThenElse(lambda this: this["field1"] > 2, StrFloat(".3f"), StrFloat(".2f")),
        ... )
        >>> d.build({"field1": 2, "field2": 2.343})
        '2,2.34'
        >>> d.build({"field1": 3, "field2": 2.343})
        '3,2.343'
        >>> d.parse("2,2.343")
        {'field1': 2, 'field2': 2.34}
        >>> d.parse("3,2.343")
        {'field1': 3, 'field2': 2.343}
    """
    def __init__(
            self, condition: typing.Union[typing.Callable, bool],
            then_subconstruct: ConstructBase,
            else_subconstruct: ConstructBase,
        ):
        """
        Args:
            condition: The condition to determine whether build/parse should be stopped.
            then_subconstruct: If the condition holds, parsing and building will be deferred
                to this sub-StrConstruct object.
            else_subconstruct: If the condition does not hold, parsing and building will be
                deferred to this sub-StrConstruct object.
        """
        if not isinstance(condition, bool) and not callable(condition):
            raise TypeError("Condition for StrIfThenElse should either be bool or callable")
        self._condition = condition
        self._then_subconstruct = then_subconstruct
        self._else_subconstruct = else_subconstruct
        self.name = None

    def _build(self, _value_, **ctx):
        """Backend method for building

        Args:
            _value_: The value to be built
            **kwargs: Other values that might be provided to the build method as additional
                context. This value is passed on to the condition, if callable. It is also
                sent to the sub-StrConstructs when their ``build`` method is called.

        Returns:
            The built string
        """
        if (isinstance(self._condition, bool) and self._condition is True) \
                or (callable(self._condition) and self._condition(ctx) is True):
            return self._then_subconstruct.build(_value_, **ctx)

        return self._else_subconstruct.build(_value_, **ctx)

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
            output = self._then_subconstruct.parse(string, **ctx)
            self._parse_left = self._then_subconstruct.parse_left()
            return output

        output = self._else_subconstruct.parse(string, **ctx)
        self._parse_left = self._else_subconstruct.parse_left()
        return output
