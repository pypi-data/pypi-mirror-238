import typing

from .construct_base import ConstructBase
from .str_construct_exceptions import StrConstructParseError, StrConstructBuildError


class StrSwitch(ConstructBase):
    """StrSwitch helps with running different build/parse paths depending on a set
    of conditions, similar to switch statement in languages like C.

        >>> from strconstruct import StrSwitch, StrInt, StrFloat
        >>> d = StrSwitch(
        ...     1,
        ...     {
        ...         1: StrFloat("0.3f"),
        ...         2: StrInt("02d")
        ...     }
        ... )
        >>> d.build(2)
        '2.000'
        >>> d = StrSwitch(
        ...     2,
        ...     {
        ...         1: StrFloat("0.3f"),
        ...         2: StrInt("02d")
        ...     }
        ... )
        >>> d.build(2)
        '02'

    Of course the above example is not very useful by itself. It just attempts to show
    how the first argument selects the build path. A more useful scenario, is to provide
    a callable as the condition:

        >>> from strconstruct import StrFloat, StrConst, StrDefault, StrStruct, StrInt
        >>> d = StrSwitch(
        ...     lambda this: this["n"],
        ...     {
        ...         1: StrFloat("0.1f"),
        ...         2: StrConst("@"),
        ...         3: StrDefault(StrInt("03X"), 17),
        ...         4: StrStruct(
        ...             "field1" / StrInt("d"),
        ...             StrConst("-"),
        ...             "field2" / StrFloat(".2f"),
        ...         )
        ...     },
        ...     default=StrInt("d")
        ... )
        >>> d.build(2, n=1)
        '2.0'
        >>> d.build(n=2)
        '@'
        >>> d.build(n=3)
        '011'
        >>> d.build(16, n=3)
        '010'
        >>> d.build(14, n=103)
        '14'
        >>> d.build(
        ...     {
        ...         "field1": 13,
        ...         "field2": 17.29,
        ...     },
        ...     n=4,
        ... )
        '13-17.29'

    The callable should receive an argument, which will be set to the context when called.
    (`Construct <https://construct.readthedocs.io/en/latest/index.html>`_ also provides
    `context <https://construct.readthedocs.io/en/latest/meta.html#the-context>`_ and
    `this <https://construct.readthedocs.io/en/latest/meta.html#using-this-expression>`_)

    Parsing provides a similar functionality

        >>> d = StrSwitch(
        ...     lambda ctx: 1,
        ...     {
        ...         1: StrFloat("0.1f"),
        ...         2: StrConst("@")
        ...     }
        ... )
        >>> d.parse("2.0")
        2.0
        >>> d = StrSwitch(
        ...     lambda ctx: 2,
        ...     {
        ...         1: StrFloat("0.1f"),
        ...         2: StrConst("@")
        ...     }
        ... )
        >>> d.parse("@")
        '@'
    """
    def __init__(self, condition: typing.Any, cases: dict, default: ConstructBase = None):
        """
        Args:
            condition: The condition for selecting cases. Can be a value or a callable. If
                a callable, it should be able to receive an argument and return a value for
                selecting a case (provided by ``cases``). The context will be given to the
                callable.
            cases: The cases from which one will be selected based on ``condition``. The
                keys will be compared to ``condition`` (or its return value when callable).
                The values should be strconstruct objects. The selected strconstruct object
                will be used for building.
            default: The default case for building - used when none of the cases is
                a match.
        """
        # TODO: Add reference for "context in the above documentation"
        self.name = None
        self._condition = condition
        self._cases = cases
        self._default = default

    def _build(self, _value_, **kwargs) -> str:
        """Backend method for building numeric strings

        If the provide ``condition`` is callable, this method will call it to get a value and
        decide which build path should be take.

        Args:
            _value_: The value to be built
            **kwargs: Other values that might be provided to the build method as additional
                context. Can be used for providing value to the condition

                >>> d = StrSwitch(
                ...     lambda this: this["n"],
                ...     {
                ...         1: StrFloat("0.1f"),
                ...         2: StrInt("02d")
                ...     }
                ... )
                >>> d.build(2, n=1)
                '2.0'
                >>> d.build(2, n=2)
                '02'

        Returns:
            The built string

        Raises:
            StrConstructBuildError: If ``condition`` or its return value, when callable, does
                not have a match in the provided cases and no default case is provided.
        """
        ctx = kwargs
        condition = self._condition
        if callable(condition):
            condition = condition(ctx)
        try:
            subconstruct = self._cases[condition]
        except KeyError:
            if self._default is None:
                raise StrConstructBuildError("No match found and default is not set")
            subconstruct = self._default
        return subconstruct.build(_value_, **kwargs)

    def _parse(self, string, **ctx):
        """Backend method for parsing numeric strings

        Args:
            string: The input string
            **ctx: Other values that might be provided to the build method as additional
                context. Can be used for providing value to the condition. See
                :func:`~StrSwitch._build` for more info.

        Returns:
            The parsed content. The type depends on the selected case
        """
        condition = self._condition
        if callable(condition):
            condition = condition(ctx)
        try:
            subconstruct = self._cases[condition]
        except KeyError:
            if self._default is None:
                raise StrConstructParseError("No match found and default is not set")
            subconstruct = self._default
        output = subconstruct.parse(string, **ctx)
        self._parse_left = subconstruct.parse_left()
        return output
