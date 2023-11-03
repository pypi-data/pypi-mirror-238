import pathlib
from android_text_tool.serializers import create_serializer
from android_text_tool.parser import TranslationsParser
from android_text_tool.serializers import OutputFormat


# Extract strings from files
def extract_strings_from(
    files_to_parse: list[pathlib.Path],
    output_format: OutputFormat,
    default_language: str,
):
    """
    Extract strings from a list of xml files(Android resource file).
    """
    # XML parser for Android strings.xml files
    xml_parser = TranslationsParser()

    # Parse files and make translations
    translations = xml_parser.parseFiles(files_to_parse)

    # Create serializer for output format
    saver = create_serializer(output_format, default_language)

    # Save translations to output file
    saver.save(translations=translations)
