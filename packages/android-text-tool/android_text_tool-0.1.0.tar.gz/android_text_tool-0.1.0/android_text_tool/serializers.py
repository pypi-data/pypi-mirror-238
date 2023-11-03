import enum

from android_text_tool.serializer import TranslationsSerializer
from android_text_tool.serializer_csv import TranslationsCSVSerializer
from android_text_tool.serializer_dinodyct import (
    TranslationsDynodictSerializer,
)
from android_text_tool.serializer_yaml import TranslationsYAMLSerializer


class OutputFormat(enum.Enum):
    """
    Output format.
    """

    CSV = "csv"
    YAML = "yaml"
    DYNODICT = "dynodict"

    @classmethod
    def get_value_from_string(cls, value: str) -> "OutputFormat":
        """
        Returns the OutputFormat from a string.
        """

        for item in cls:
            if item.value == value:
                return item

        raise ValueError("Unknown output format")


def create_serializer(
    outputType: OutputFormat, default_language: str
) -> TranslationsSerializer:
    """
    A factory method for creating serializers. Returns a serializer for the
    specified output format.
    """

    serializers: dict[OutputFormat, TranslationsSerializer] = {
        OutputFormat.CSV: TranslationsCSVSerializer,
        OutputFormat.YAML: TranslationsYAMLSerializer,
        OutputFormat.DYNODICT: TranslationsDynodictSerializer,
    }

    try:
        serializer_class = serializers[outputType]
        return serializer_class(default_language=default_language)
    except KeyError:
        raise RuntimeError("Unknown serializer")
