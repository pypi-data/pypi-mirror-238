# Android Text Tool

## Description

This script is useful for extracting all strings from a multimodule Android project. It supports different output formats
which may be useful for you. Currently supported csv, yaml, dynodict-yaml. JSON is coming soon.

NOTE: Before starting using this tool, please run in your project root otherwise you may get a lot of rubbish strings in
the output file:

```bash
./gradlew clean
```

## Installation

This tool can be installed via PIP repositiory by running the following command:

```bash
pip install android-text-tool
```

or if you use Poetry, run this:

```bash
poetry add android-text-tool
```

## Usage

### Basic usage

Run the tool in the root directory of your project(please, don't forget to clean it before to prevent extracting strings from different libraries you use).

```bash
android-text-tool . -f csv
```

As a result, you'll get a CSV file which contains all string resources from your project.

### Advanced usage

```bash
android-text-tool [-h] -f {csv,yaml,dynodict} [-l DEFAULT_LANGUAGE] path
```

Positional arguments:

* `path` - the path of the Android project to scan.

Optional arguments:

* `-f {csv,yaml,dynodict}`, `--format {csv,yaml,dynodict}` - the output format to save the translations. Default is csv.
* `-l DEFAULT_LANGUAGE`, `--default-language DEFAULT_LANGUAGE` - the default language for the translations. This language code will be used for strings inside `value` folder. Default is en.

## Supported output formats

### CSV

This is a comma-separated sheet.

Example:

```csv
key,es,ht,fr,en
translation1,Test1,Test1,Test1,Test1
translation2,Test1,Test1,Test1,Test1
translation3,Test1,Test1,Test1,Test1
```

### YAML

Example:

```yaml
languages:
- en
- ht
- es
- fr
name: Exported project - 2023-11-03T02:29:50
translations:
- key: strings.xml
  translations:
  - key: translation1
    values:
      en: Test1
      fr: Test1
      ht: Test1
  - key: translation2
    values:
      en: Test1
      fr: Test1
      ht: Test1
```

### Dynodict YAML

This format is for a tool which is going to be released soon. It's under development. Please, do not use it.
