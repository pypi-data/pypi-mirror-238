import typing

from .construct_base import ConstructBase
from .str_construct_exceptions import StrConstructParseError, StrCheckError


class StrCheck(ConstructBase):
    """StrCheck builds and parses nothing. It is useful only adding additional verification,
    for example, to an StrStruct.

        >>> d = StrStruct(
        ...     "f1" / StrInt("d"),
        ...     StrCheck(lambda x: x["f1"] == 30)
        ... )
        >>> d.build({"f1":30})
        '30'
        >>> d.build({"f1":31})
        ...
        strconstruct.str_construct_exceptions.StrCheckError: Check failed. Context was {'f1': 31}
        >>> d.parse("30")
        {'f1': 30}
        >>> d.parse("29")
        ...
        strconstruct.str_construct_exceptions.StrCheckError: Check failed. Context was {'f1': 29}

    As can be seen in the example, the context is passed onto the StrCheck object and function
    pointer in StrCheck should return a boolean. If True, the check passes. The context is
    put together during both building and parsing. In both cases, it is a dictionary with
    "parsed" values (not strings).

    It can be combined with other types of StrConstruct objects as well, of course.

        >>> d = StrStruct(
        ...     "f1" / StrInt("d"),
        ...     StrConst(","),
        ...     "f2" / StrRebuild(StrInt("d"), lambda x: x["f1"] * 2),
        ...     StrCheck(lambda x: x["f2"] == 30),
        ... )
        >>> d.build({"f1": 15})
        '15,30'
        >>> d.parse("15,30")
        {'f1': 15, 'f2': 30}
        >>>
        >>> d.build({"f1": 14})
        ...
        strconstruct.str_construct_exceptions.StrCheckError: Check failed. Context was {'f1': 14, 'f2': 28}
        >>> d.parse("14,31")
        ...
        strconstruct.str_construct_exceptions.StrCheckError: Check failed. Context was {'f1': 14, 'f2': 31}

    It is mostly useful for parsing. An example is verifying checksum of received strings (during
    parsing).
    """
    def __init__(self, condition: typing.Callable):
        """
        Args:
            condition: A function pointer that should get the context and return a boolean.
                The function will be evaluated during both ``run`` and ``build``. If it
                returns a False, ``build`` and ``parse`` StrCheckError.

        """
        if not callable(condition):
            raise TypeError("Condition for StrCheck should be a callable")
        self.name = None
        self._last_built = None
        self._parse_left = None

        self._condition = condition

    def _build(self, _value_, **ctx) -> str:
        """Backend method for building

        Args:
            _value_: The value to be built. Not used by this StrConstruct
            **ctx: Other values that might be provided to the build method as additional
                context.

        Returns:
            Always an empty string

        Raises:
            StrCheckError, if the function pointer returns False
        """
        if self._condition(ctx) is False:
            raise StrCheckError(f"Check failed. Context was {ctx}")

        return ""

    def _parse(self, string, **ctx) -> int:
        """Backend method for parsing

        Args:
            string: The input string
            **ctx: Other values that might be provided to the build method as additional
                context.

        Raises:
            StrCheckError, if the function pointer returns False
        """
        if self._condition(ctx) is False:
            raise StrCheckError(f"Check failed. Context was {ctx}")
