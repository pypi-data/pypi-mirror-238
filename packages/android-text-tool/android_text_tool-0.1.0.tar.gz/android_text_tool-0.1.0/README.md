# Android Text Tool

## Description

This is a useful script for exctracting all strings from a multimodule Android project.

NOTE: Before cleaning, please run:

```bash
    ./gradlew clean
```

in the root of your project.

## Installation

This script can be installed via PIP repositiory by running the following command:

```bash
    pip install android-text-tool
```

## Usage

Basic usage. Run the tool in the root of your project(please, don't forget to clean it before to prevent extracting strings from different libraries you use).

```bash
    android-text-tool .
```
