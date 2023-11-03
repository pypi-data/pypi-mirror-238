#!/usr/bin/env python3

import argparse
import pathlib
from android_text_tool.main import extract_strings_from
from android_text_tool.serializers import OutputFormat


def main():
    arg_parser = argparse.ArgumentParser(
        description="The Strings extractor from an Android project."
    )

    arg_parser.add_argument(
        "path", action="store", help="the path of the Android project to scan."
    )
    arg_parser.add_argument(
        "-f",
        "--format",
        action="store",
        required=True,
        choices=[file_format.value for file_format in OutputFormat],
        default=OutputFormat.CSV.value,
        help="the output format to save the translations.",
    )
    arg_parser.add_argument(
        "-l",
        "--default-language",
        action="store",
        required=False,
        default="en",
        help="the default language for the translations.",
    )
    args = arg_parser.parse_args()

    target_dir = pathlib.Path(args.path)
    output_format = OutputFormat.get_value_from_string(args.format)
    default_language = args.default_language

    if not target_dir.exists():
        print("The target directory doesn't exist.")
        raise SystemExit(1)

    print("Scanning of the project directory...")

    all_files = [
        f.resolve() for f in target_dir.glob("**/*.xml") if f.is_file()
    ]

    print("Total XML files: {}.".format(len(all_files)))

    print("Extracting strings...")

    extract_strings_from(
        files_to_parse=all_files,
        output_format=output_format,
        default_language=default_language,
    )

    print("Done.")


if __name__ == "__main__":
    main()
