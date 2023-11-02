import typing

from .construct_base import ConstructBase


class StrRebuild(ConstructBase):
    """StrRebuild is useful for calculating the input value of the ``build`` method
    during the build process. It only affects the build process. Parsing is simply
    deferred to the child StrConstruct object.

        >>> d = StrRebuild(StrInt("d"), lambda x: 2 * x["n"])
        >>> d.build({}, n=5)
        '10'

    My favorite use case of StrRebuild (and construct's Rebuild) is calculating checksum.
    Here is an example.

        >>> d = StrStruct(
        ...     "stx" / StrDefault(StrInt("02X"), 12),
        ...     "counter" / StrInt("d"),
        ...     "payload" / StrInt("d"),
        ...     "checksum" / StrRebuild(
        ...         StrInt("d"),
        ...         lambda ctx: sum([ctx["stx"], ctx["counter"], ctx["payload"]]) % 256
        ...     ),
        ...     "etx" / StrConst("\\n"),
        ...     separator=","
        ... )
        >>>
        >>> d.build({"counter": 3, "payload": 5})
        '0C,3,5,20,\\n'

    As said before, parsing doesn't recalculate the fields and checks the outcome against
    the received string.

        >>> d.parse("0C,3,5,20,\\n")
        {'stx': 12, 'counter': 3, 'payload': 5, 'checksum': 20, 'etx': '\\n'}
        >>> d.parse("0C,3,5,21,\\n")
        {'stx': 12, 'counter': 3, 'payload': 5, 'checksum': 21, 'etx': '\\n'}

    """
    def __init__(self, subconstruct: ConstructBase, callback: typing.Callable):
        """
        Args:
            subconstruct: The sub-StrConstruct object. Both build and parse will be
                deferred to this sub-StrConstruct object. But for build the value fed
                to the ``build`` method is collected from the ``callback``.
            callback: The callback for rebuilding the build value. It should receive one
                argument (for the context) and return a value. The type of the return value
                should be suitable for ``subconstruct``.
        """
        if not callable(callback):
            raise TypeError("Condition for StopIf should either be bool or callable")
        self.name = None
        self._last_built = None

        self._callback = callback
        self._subconstruct = subconstruct

    def _build(self, _value_, **ctx):
        """Backend method for building

        Args:
            _value_: Not used by this StrConstruct
            **kwargs: The main input for the callback function to extract the "value".
                It is also sent to the sub-StrConstruct when its ``build`` method is called.
                This behavior is similar to construct's ``Rebuild``.

                    >>> d = Rebuild(Int8ub, lambda x: 10)
                    >>> d.build(2)
                    b'\\n'
                    >>> d.build(20)
                    b'\\n'

        Returns:
            The built string
        """
        self._last_built = self._callback(ctx)
        return self._subconstruct.build(self._last_built, **ctx)

    def _parse(self, string, **ctx):
        """Backend method for parsing

        Args:
            string: The input string
            **ctx: Other values that might be provided to the build method as additional
                context. It's also sent to the sub-StrConstruct object

        Returns:
            The parsed content. The type depends on the child StrConstruct
        """
        output = self._subconstruct.parse(string, **ctx)
        self._parse_left = self._subconstruct.parse_left()
        return output
