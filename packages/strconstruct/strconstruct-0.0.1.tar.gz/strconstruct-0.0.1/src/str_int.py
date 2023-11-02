from .construct_base import ConstructBase
from .str_construct_exceptions import StrConstructParseError


class StrInt(ConstructBase):
    """StrInt can be used for building and parsing numeric fields. An StrInt, needs a format to
    be constructed, similar to other str-construct classes. The constructed objects can be used
    to build and parse strings.

        >>> from strconstruct import StrInt
        >>> StrInt("d").build(2)
        '2'
        >>> StrInt("d").build(-2)
        '-2'
        >>> StrInt("d").parse("3")
        3
        >>> StrInt("d").parse("-3")
        -3

    StrInt accepts, ``d``, ``x``, and ``X`` formats. They work set decimal, lower-case hex and
    upper-case hex formats, respectively.

        >>> StrInt("x").build(15)
        'f'
        >>> StrInt("X").build(15)
        'F'
        >>> StrInt("X").parse("F")
        15

    Similar to other str-construct classes, StrInt is strict with parsing. The following line
    of code raises ``StrConstructParseError``.

        >>> StrInt("x").parse("F")

    Finally, all the formats accept lengths with an optional padding value of zero:

        >>> StrInt("013X").build(10)
        '000000000000A'
        >>> StrInt("13X").parse("000000000000A")
        10

    If the expected number of characters is not received during parsing, a
    ``StrConstructParseError`` is raise. For example, the parsing for the following lines code
    will fail.

        >>> StrInt("3d").parse("12")
        >>> StrInt("13X").parse("00000000000A")

    It's also important to note that when no length is specified, the search continues until
    a non-parsable character is found. If there is a length, only that many of characters is
    processed by the parser method.

        >>> StrInt("d").parse("12345>")
        12345
        >>> StrInt("2d").parse("12345>")
        12
        >>> StrInt("02d").parse("12345>")
        12

    """
    def __init__(self, format_):
        """
        Args:
            format_: The format of the StrInt. The supported values are ``d``, ``x``, and ``X``.
                Length can also be specified with an optional padding value of zero.
        """
        self.name = None
        self._format = f"{{:{format_}}}"

        if len(format_) == 0:
            raise ValueError(
                "Invalid format. At least the integer representation should be "
                "provided (e.g. 'd', 'x' etc.)"
            )

        self._format_type = format_[-1]
        if self._format_type not in ["d", "x", "X"]:
            raise ValueError(f"Format ({self._format_type}) not supported by StrInt")

        self._supported_chars = [str(item) for item in range(10)]
        if self._format_type == "x":
            self._supported_chars += [chr(item) for item in range(ord("a"), ord("f") + 1)]
        elif self._format_type == "X":
            self._supported_chars += [chr(item) for item in range(ord("A"), ord("F") + 1)]

        if format_[0] == "0":
            _format_length = format_[1:-1]
        else:
            _format_length = format_[0:-1]
        try:
            self._format_length = int(_format_length)
        except ValueError:
            self._format_length = None

    def _build(self, _value_, **kwargs) -> str:
        """Backend method for building numeric strings

        Args:
            _value_: The value to be built
            **kwargs: Other values that might be provided to the build method as additional
                context. Ignore by StrInt.

        Returns:
            The built string
        """
        return f"{self._format}".format(_value_)

    def _parse(self, string, **kwargs) -> int:
        """Backend method for parsing numeric strings

        Args:
            string: The input string
            **kwargs: Other values that might be provided to the build method as additional
                context. Will be ignored by StrFloat

        Returns:
            The parsed content as an ``int`` object
        """
        if string[0] == "-":
            multiplier = -1
            string = string[1:]
        elif string[0] == "+":
            multiplier = 1
            string = string[1:]
        else:
            multiplier = 1
        if self._format_length is not None:
            if len(string) < self._format_length:
                raise StrConstructParseError(
                    f"Insufficient characters found. At least {self._format_length} "
                    "character is needed"
                )
            number = string[:self._format_length]
            parse_left = string[self._format_length:]
        else:
            number = []
            for index, char in enumerate(string):
                if char in self._supported_chars:
                    number.append(char)
                else:
                    break
            number = "".join(number)
            parse_left = string[index:]

        if number == "":
            raise StrConstructParseError("No numeric content collected from the input")

        self._parse_left = parse_left
        if self._format_type == "d":
            return int(number) * multiplier
        if self._format_type == "x" or self._format_type == "X":
            return int(number, 16) * multiplier
