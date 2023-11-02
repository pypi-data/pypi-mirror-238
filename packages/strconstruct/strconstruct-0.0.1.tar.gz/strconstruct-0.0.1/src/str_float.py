from .construct_base import ConstructBase
from .str_construct_exceptions import StrConstructParseError

class StrFloat(ConstructBase):
    """StrFloat is a class for building and parsing strings that show floating-point
    numeric values. The number of decimal digits can also be specified.

        >>> StrFloat(".1f").build(2)
        '2.0'
        >>> StrFloat(".1f").build(2.0)
        '2.0'
        >>> StrFloat(".1f").parse("2.1")
        2.1
        >>> StrFloat(".1f").parse("2.0")
        2.0

    The length makes the object more strict when it comes to parsing strings. The following
    raises an ``StrConstructParseError`` exception.

        >>> StrFloat(".4f").parse("2.018")
        ...
        strconstruct.str_construct_exceptions.StrConstructParseError: Insufficient
        characters found. At least 4 decimal numbers are needed

    When a length is not specified, parsing becomes greedy, as far as there is parsable
    character.

        >>> StrFloat("f").parse("19.98765@")
        19.98765
        >>> StrFloat(".2f").parse("19.18765@")
        19.18

    """
    def __init__(self, format_):
        """
        Args:
            format_: The format of the floating-point number. The only supported format
                is ``f``. This module can receive the number of the decimal digits.

        Raises:
            ValueError: If the format is invalid
        """
        self.name = None
        self._format = f"{{:{format_}}}"

        if len(format_) == 0:
            raise ValueError("Invalid format. Only 'f' is supported by StrFloat")

        self._format_type = format_[-1]
        if self._format_type != "f":
            raise ValueError(f"Format ({self._format_type}) not supported by StrFloat")

        break_down = format_[:-1].split(".")
        try:
            self._format_length = int(break_down[1])
        # ValueError happens if breakdown[1] is an empty string
        # IndexError happens if there is not index 1 at all
        except (ValueError, IndexError):
            self._format_length = None

    def _build(self, _value_, **kwargs) -> str:
        """Backend method for building strings representing floating-point numbers

        Args:
            _value_: The value to be built
            **kwargs: Other values that might be provided to the build method as additional
                context. Ignore by StrFloat.

        Returns:
            The built string
        """
        return f"{self._format}".format(_value_)

    def _parse(self, string, **kwargs) -> float:
        """Backend method for parsing strings representing floating-point numbers

        Args:
            string: The input string
            **kwargs: Other values that might be provided to the build method as additional
                context. Will be ignored by StrFloat

        Returns:
            The parsed content as a ``float`` object
        """
        break_down = string.split(".")
        if len(break_down) == 1:
            whole = break_down[0]
            decimal = ""
        else:
            whole, decimal = break_down[0:2]
        if self._format_length is not None:
            if len(decimal) < self._format_length:
                raise StrConstructParseError(
                    f"Insufficient characters found. At least {self._format_length} "
                    "decimal numbers are needed"
                )
            decimal = decimal[:self._format_length]
        else:
            if len(decimal) == 0:
                index = 0
            else:
                for index, char in enumerate(decimal):
                    if not char.isdigit():
                        break
                else:
                    index += 1

            decimal = decimal[:index]

        self._parse_left = string[(len(whole) + 1 + len(decimal)) :]
        return float(".".join([whole, decimal]))
