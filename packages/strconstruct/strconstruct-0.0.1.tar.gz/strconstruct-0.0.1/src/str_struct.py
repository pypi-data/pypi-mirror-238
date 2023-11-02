
from .construct_base import ConstructBase
from .str_construct_exceptions import StrConstructBuildError, StrConstructParseError, StrStopFieldError

class StrStruct(ConstructBase):
    """StrStruct is arguably one of the most important modules in this package when it
    comes to real-life protocols; they are usually a `set of fields`, rather than
    individual values.

    StrStruct looks like a struct declaration in C. Here is an example

        >>> d = StrStruct(
        ...     "field1" / StrInt("d"),
        ...     "field2" / StrConst(","),
        ...     "field3" / StrFloat(".2f"),
        ... )

    Every field `can` be renamed (using the division operator - see :mod:`~ConstructBase`
    for more information). For building, since this is a multi-field StrConstruct, it
    receives a dictionary. Similarly, the ``parse`` method returns a dictionary.

        >>> d.build({"field1": 12, "field3": 4.876})
        '12,4.88'
        >>> d.parse("199,8.76")
        {'field1': 199, 'field2': ',', 'field3': 8.76}

    The fields can be nameless as well. If they are, they need to be able to build without
    a given value (like ``StrConst``, ``StrDefault``) as there will no way provide them with
    some value in the input dictionary. In the previous example, we can agree that ``field2``
    can become nameless; we'll never need to give it a value.

        >>> d = StrStruct(
        ...     "field1" / StrInt("d"),
        ...     StrConst(","),
        ...     "field3" / StrFloat(".2f"),
        ... )
        >>> d.build({"field1": 12, "field3": 4.876})
        '12,4.88'
        >>> d.parse("199,8.76")
        {'field1': 199, 'field3': 8.76}

    It's worth noting the difference that the nameless field made in the result of the ``parse``
    method; it's absent from the result. Importantly, the parser `does parse` all the fields;
    named, nameless or hidden (more on hidden later). This ensures that the parser is receiving
    a correct message. After all, this is designed for dealing with protocols.

        >>> d.parse("199-8.76")
        ...
        strconstruct.str_construct_exceptions.StrConstructParseError: Expected ',' but found '-8.76'

    The fields can be hidden as well. In that case, they can receive values during build but
    they will be absent from the parse result.

        >>> d = StrStruct(
        ...     "field1" / StrInt("d"),
        ...     StrConst(","),
        ...     "_field3" / StrDefault(StrFloat(".2f"), 13.23),
        ... )
        >>> d.build({"field1": 12})
        '12,13.23'
        >>> d.build({"field1": 12, "_field3": 87.12})
        '12,87.12'
        >>> d.parse("37,19.45")
        {'field1': 37}

    StrStructs can be nested too. This is an important functionality when it comes to
    multi-level protocols.

        >>> d = StrStruct(
        ...     "field1" / StrInt("d"),
        ...     StrConst(","),
        ...     "field3" / StrSwitch(
        ...         lambda this:this["field1"],
        ...         {
        ...             1: StrStruct(
        ...                 "field4" / StrFloat(".2f"),
        ...                 StrConst("\\n"),
        ...             ),
        ...             2: StrStruct(
        ...                 "field4" / StrInt("d"),
        ...                 StrConst("\\r"),
        ...             )
        ...         }
        ...     )
        ... )
        >>> d.build({"field1":2, "field3":{"field4":2}})
        '2,2\\r'
        >>> d.build({"field1":1, "field3":{"field4":2}})
        '1,2.00\\n'

    As can be seen, each StrStruct needs its own dict when building.

    A useful argument that StrStruct accepts is ``separator``. When present, the
    ``build`` method puts that separator between all the fields. Similarly, the
    ``parse`` method expects the separator to be present in the input string

        >>> d = StrStruct(
        ...     "field1" / StrInt("d"),
        ...     "field2" / StrInt("02X"),
        ...     "field3" / StrFloat(".2f"),
        ...     separator=":"
        ... )
        >>> output = d.build(
        ...     {
        ...         "field1": 2,
        ...         "field2": 15,
        ...         "field3": 3.1,
        ...     }
        ... )
        >>> output
        '2:0F:3.10'

    """
    def __init__(self, *args: ConstructBase, separator: str = ""):
        """
        Args:
            *args: A set of StrConstructs objects. They can be named, nameless or have
                hidden names
            separator: Sets a separator for all the fields
        """
        for item in args:
            if not isinstance(item, ConstructBase):
                raise TypeError(
                    "All items need to be of type ConstructBase (e.g. StrFloat, StrInt, etc.). Found "
                    f"a {type(item)}."
                )
        self.name = None
        self._fields = args
        self._separator = separator

    def _build(self, values, **ctx):
        """Backend method for building

        Args:
            _value_: The value to be built
            **ctx: Other values that might be provided to the build method as additional
                context. StrStruct passes this to its child sub-StrConstruct objects.
                It also adds to this context every time an StrConstruct object is build.
                That's how the child StrConstruct objects have access to the context, which
                includes both user-defined and build contexts.

        Returns:
            The built string
        """
        if not isinstance(values, dict):
            raise TypeError("The value for building an StrConstruct should be a dict")

        outputs = []
        for field in self._fields:
            if field.name is None:
                # Well there is no name. So we can't find a given value. In this case, the
                # build method of the corresponding object is expected to be able to build
                # without a give value. Let's give it a try.
                try:
                    output = field.build(**ctx)
                except StrStopFieldError:
                    # Nothing problematic. The StopIf construct has signaled to stop building
                    break
                except StrConstructBuildError as e:
                    raise StrConstructBuildError("Could not build the nameless field")

            else:
                try:
                    value = values[field.name]
                except KeyError:
                    # If the key-value pair is not provided, try to build it with no value
                    try:
                        output = field.build(**ctx)
                    except StrStopFieldError:
                        break
                    # Some constructs can build without values. But we still need to add
                    # their value to the context.
                    last_build = field.last_built()
                    if last_build is not None:
                        ctx[field.name] = last_build
                else:
                    try:
                        output = field.build(value, **ctx)
                    except StrStopFieldError:
                        break
                    ctx[field.name] = value  # Could use field.last_built() as well.
            # Some fields, if they build nothing (like StrIf when its condition doesn't hold),
            # return empty strings
            if output != "":
                outputs.append(output)

        return self._separator.join(outputs)

    def _parse(self, string, **ctx):
        outputs = {}
        missing_separator_error_pending = False
        for index, field in enumerate(self._fields):
            try:
                output = field.parse(string, **ctx)
            except StrStopFieldError:
                break
            if field.name is not None and field.name[0] != "_":
                if field.name in ctx.keys():
                    raise ValueError(f"Got two definitions for {field.name}")
                ctx[field.name] = output
            # Some fields, if they parse nothing (like StrIf when its condition doesn't hold),
            # return None
            if output is None:
                continue
            if field.name is not None and field.name[0] != "_":
                outputs[field.name] = output
            string = field.parse_left()
            self._parse_left = string

            if missing_separator_error_pending is True:
                # If we reach this point, the current StrConstruct could build and if there
                # is an exception pending, raise it.
                raise StrConstructParseError(f"Separator ('{self._separator}') not found")
            # No need to check the separator for the last item
            if index != (len(self._fields) - 1) and self._separator != "":
                if not string.startswith(self._separator):
                    # We didn't find the separator and it's not the last item. But don't
                    # raise an error just yet. The next item might parse nothing. If the next
                    # parses something, then we need to raise the error.
                    missing_separator_error_pending = True
                string = string[len(self._separator):]

        return outputs
