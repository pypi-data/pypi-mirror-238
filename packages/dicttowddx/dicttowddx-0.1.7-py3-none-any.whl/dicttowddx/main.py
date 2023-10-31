import base64
from collections.abc import Iterable
from typing import Any

from yattag import Doc, indent


class DictToWDDX:
    """This class is used to convert a simple python dict to wddx data format"""

    def __init__(
        self,
        data: dict,
        force_type: bool = False,
        format_output: bool = False,
        display_indent: int = 4,
    ) -> None:
        if not data or not isinstance(data, dict):
            raise TypeError(f"Data must be of type dict, type {type(data)} given")
        self.data = data
        self.format_output = format_output
        self.display_indent = display_indent
        self.force_type = force_type
        self.doc, self.tag, self.text = Doc().tagtext()

    @staticmethod
    def to_type(value) -> str:
        """This function is used to convert a value to a type"""
        non_str = {
            "bool": "boolean",
            "int": "number",
            "float": "number",
            "bytes": "binary",
            "datetime": "dateTime",
        }
        main_type = type(value).__name__
        return non_str.get(main_type) if main_type != "str" else "string"

    def wddx_type(self, value) -> str:
        """This function is used to force the type of the value"""
        return self.to_type(value) if self.force_type else "string"

    def is_binary(self, value) -> Any:
        """This function is used to check if the value is binary"""
        if self.force_type and self.wddx_type(value) == "binary":
            return self.text(base64.b64encode(value).decode())
        if type(value).__name__ == "bytes":
            return self.text(value.decode("utf-8"))
        return self.text(str(value))

    def none_or_data(self, value):
        """This function is used to check if the value is None or binary"""
        if value is None:
            self.doc.asis("<null/>")
        else:
            with self.tag(self.wddx_type(value)):
                self.is_binary(value)

    def to_wddx(self) -> str:
        """This function is used to convert a simple python dict to wddx data format"""

        self.doc.asis("<wddxPacket version='1.0'><header/>")
        with self.tag("data"):
            with self.tag("struct"):
                for key in self.data:
                    if key is None:
                        raise KeyError("Key cannot be None", "{}".format(key))
                    if isinstance(self.data.get(key), Iterable) and (
                        not isinstance(self.data.get(key), (str, bytes))
                    ):
                        with self.tag("var", name=key):
                            with self.tag("array", length=len(self.data.get(key))):
                                for elem in self.data.get(key):
                                    self.none_or_data(elem)
                    else:
                        with self.tag("var", name=key):
                            self.none_or_data(self.data.get(key))
        self.doc.asis("</wddxPacket>")
        val = self.doc.getvalue()
        return (
            val
            if not self.format_output
            else indent(val, indentation=" " * self.display_indent, newline="\n")
        )
