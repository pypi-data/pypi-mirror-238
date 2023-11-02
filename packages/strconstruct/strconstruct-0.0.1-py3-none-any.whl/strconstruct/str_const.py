from .construct_base import ConstructBase
from .str_construct_exceptions import StrConstructParseError, StrConstructBuildError


class StrConst(ConstructBase):
    """StrConst is helpful when there is constant fields and removes the need to specify
    them when building.

        >>> packet = StrConst("MyString")
        >>> packet.build()
        'MyString'

    It can also build without a value, which becomes an important feature when using
    StrStruct (it can be defined only once).

        >>> packet = StrStruct(
        ...     StrConst(">"),
        ...     "value" / StrInt("d"),
        ...     StrConst("\\n"),
        ... )
        >>> packet.build({"value": 22})
        '>22\\n'

    """

    def __init__(self, const):
        """
        Args:
            const: The constant value use for both building and parsing
        """
        self.name = None
        self._parse_left = None
        self._last_built = None

        self._const = const

    def _build(self, _value_, **ctx) -> str:
        """Backend method for building constant strings

        Args:
            _value_: The value to be built
            **ctx: Other values that might be provided to the build method as additional
                context. Ignore by StrConst.

        Returns:
            The built string
        """
        if _value_ is not None and _value_ != self._const:
            raise StrConstructBuildError("StrConst needs the same constant value or nothing to build")

        self._last_built = self._const
        return self._const

    def _parse(self, string: str, **ctx) -> str:
        """Backend method for parsing constant strings

        Args:
            string: The input string
            **kwargs: Other values that might be provided to the build method as additional
                context. Will be ignored by StrConst

        Returns:
            The parsed content as an ``str`` object
        """
        if not string.startswith(self._const):
            raise StrConstructParseError(f"Expected '{self._const}' but found '{string}'")
        self._parse_left = string[len(self._const) :]
        return self._const
