from android_text_tool.translation_key import TranslationKey
from android_text_tool.translarions_storage import TranslationsStorage
from android_text_tool.utils import progressbar


import pathlib
import xml.etree.ElementTree as ET


class TranslationsParser:
    def __init__(self) -> None:
        pass

    def parseFiles(self, file_list: list[pathlib.Path]):
        storage: TranslationsStorage = TranslationsStorage()
        translation_storage = storage.translations

        for file in progressbar(file_list, "Extracting lines: "):
            parent_folder = file.parent.name
            translations = self.parseXML(file)

            file_name = file.name

            for key, value in translations.items():
                dict_key = TranslationKey(file_name, key)

                try:
                    value_dict = translation_storage[dict_key]
                except KeyError:
                    value_dict = {}
                    translation_storage[dict_key] = value_dict

                value_dict[parent_folder] = value

        return translation_storage

    def parseXML(self, xmlfile):
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        translations = {}

        for item in root.findall(".//string[@name]"):
            name = item.get("name")
            if name is None:
                continue

            translations[name] = item.text

        return translations
