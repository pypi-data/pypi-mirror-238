from __future__ import annotations

from .str_construct_exceptions import StrConstructBuildError, StrConstructFormatError


class ConstructBase:
    """ConstructBase forms the basis of all the StrConstruct class. All of them inherit
    from ConstructBase. ConstructBase provides two important public API that is exposed
    by all the StrConstruct objects; ``build`` and ``parse``. This class is intended for
    internal use only.

    The ``build`` method always returns a string. The ``parse`` method does the revers;
    it always gets a string. The input type of ``build`` and the return type of ``parse``
    depend on the type of the StrConstruct. For example, ``StrInt``'s build method
    gets an int while ``StrStruct`` gets a dictionary.

    An StrConstruct can be also be named by the division operator. The return object of
    the division operation is the same StrConstruct object used in the operation, not a
    new object. So it has all attributes of the original object.

        >>> d = StrInt("d")
        >>> d.name
        >>> id(d)
        140492806992128
        >>> d = "field" / d
        >>> d.name
        'field'
        >>> id(d)
        140492806992128

    There are two motivations here; a clear syntax for declaring multi-field protocols and
    of course compatibility with `Construct <https://construct.readthedocs.io/en/latest/
    index.html>`_.  See :class:`.StrStruct` for more information.

    Another important note is that `_value_` is a reserved value when it comes to naming
    fields. Long story short, the reason behind it is support passing around contexts.
    More info on contexts can be found TODO.
    """
    RESERVED_FIELD_NAME = "_value_"

    def _div(self, other):
        if not isinstance(other, str):
            raise TypeError("Division is support only for strings")
        if other == self.RESERVED_FIELD_NAME:
            raise StrConstructFormatError(
                f"{self.RESERVED_FIELD_NAME} is a reserved name for fields"
            )
        self.name = other
        return self

    def __truediv__(self, other: str) -> ConstructBase:
        """Used for naming StrConstruct objects.

        Args:
            other: The name of the construct. ``_value_`` is reserved for StrConstruct
                internal use.

        Returns:
            The same object with the new name
        """
        return self._div(other)

    def __rtruediv__(self, other: str) -> ConstructBase:
        """Used for naming StrConstruct objects.

        Args:
            other: The name of the construct. ``_value_`` is reserved for StrConstruct
                internal use.

        Returns:
            The same object with the new name
        """
        return self._div(other)

    def _build(self, _value_, **kwargs):
        """The build backed for different StrConstruct classes. Must be overridden by the
        child class.

        Args:
            _value_: The value to be built
            **kwargs: The context

        Raises:
            NotImplementedError if not overridden by the child class
        """
        raise NotImplementedError("Should be overridden by the child classes")

    def _parse(self, string, **kwargs):
        """The parse backed for different StrConstruct classes. Must be overridden by the
        child class.

        Args:
            string: The string to be parsed
            **kwargs: The context

        Raises:
            NotImplementedError if not overridden by the child class
        """
        raise NotImplementedError("Should be overridden by the child classes")

    def build(self, _value_=None, **kwargs):
        """Build an StrConstruct

        Args:
            _value_: The value to be built
            **kwargs: The context

        Returns:
            The built value
        """
        # Some StrConstruct class do not necessarily need a value for building. StrConst
        # and StrDefault are sample examples.
        return self._build(_value_, **kwargs)

    def parse(self, string, **kwargs):
        """Parse an StrConstruct

        Args:
            string: The string to be parsed
            **kwargs: The context

        Returns:
            The parsed value
        """
        self._parse_left = None
        return self._parse(string, **kwargs)

    def last_built(self):
        """Returns the value used for building last time

        Note that the value returned by this method is available only once. After the
        first call (per call to build()), the value is reset.

        This method is specially useful for StrConstructs that can build without input
        values e.g. StrConst, StrDefault.

        Returns:
            The value used for the last build.
        """
        output = self._last_built
        self._last_built = None
        return output

    def parse_left(self):
        """The remaining string that was not parsed in the last call to ``parse``.

        Note that the value returned by this method is available only once. After the
        first call (per call to parse()), the value is reset.

        Returns:
            The remaining string that was not parsed.
        """
        output = self._parse_left
        self._parse_left = None
        return output
