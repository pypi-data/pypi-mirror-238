from .construct_base import ConstructBase


class StrDefault(ConstructBase):
    """StrDefault provides a default value for the building procedure. Parsing is simply
    deferred to the sub-strConstruct object. Let's take an example.

        >>> d = StrDefault(StrInt("02X"), 17)
        >>> d.build()
        '11'
        >>> d.build(18)
        '12'

    Parsing, in the example above, behaves exactly according to the sub-StrConstruct
    i.e. StrInt(). StrDefault does not make the `parse` method to work with no data
    (that would make no sense when seeing it in terms of communication and protocol)

        >>> d.parse()
        ...
        TypeError: parse() missing 1 required positional argument: 'string'
        >>> d.parse("11")
        17
        >>> d.parse("12")
        18

    """

    def __init__(self, construct, default):
        """
        Args:
            construct: The underlying StrConstruct object
            default: The default value to be built when no data is give to the build
                method. Note that this value will be given to the StrConstruct object
                provided by `construct` and the output string depends on `construct`.
        """
        self.name = None
        self._parse_left = None
        self._last_built = None

        self._subconstruct = construct
        self._default = default

    def _build(self, _value_, **ctx) -> str:
        """Backend method for building default strings

        Args:
            _value_: The value to be built
            **ctx: Other values that might be provided to the build method as additional
                context. Not used by StrDefault

        Returns:
            The built string
        """
        # TODO: This should work with empty dict instead of None. See the following link
        # https://construct.readthedocs.io/en/latest/misc.html#default
        if _value_ is None:
            self._last_built = self._default
            return self._subconstruct.build(self._default)

        self._last_built = _value_
        return self._subconstruct.build(_value_)

    def _parse(self, string, **ctx):
        """Backend method for parsing numeric strings

        Args:
            string: The input string
            **kwargs: Other values that might be provided to the build method as additional
                context. Not used by StrDefault

        Returns:
            The parsed content. The type depends on the underlying StrConstruct object.
        """
        output = self._subconstruct.parse(string)
        self._parse_left = self._subconstruct.parse_left()
        return output
