import datetime
from android_text_tool.serializer import TranslationsSerializer
from android_text_tool.translarions_storage import TranslationsStorage
from android_text_tool.utils import trim_value_prefix


import yaml


class TranslationsYAMLSerializer(TranslationsSerializer):
    def save(self, translations: TranslationsStorage):
        _languages = set()

        for _, value in translations.items():
            valueNames = sorted(value.keys())
            valueNames = [trim_value_prefix(x) for x in valueNames if x]
            _languages.update(valueNames)

        languages = list(_languages)

        projectDict = {
            "name": "Exported project - {}".format(
                datetime.datetime.now().replace(microsecond=0).isoformat()
            ),
            "languages": languages,
            "translations": self.export_translations(translations),
        }
        with open("exported.yaml", "w", encoding="utf-8") as file:
            yaml.dump(
                projectDict,
                file,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=True,
                encoding=None,
            )

    def export_translations(
        self, translations: TranslationsStorage
    ) -> list[dict[str, str]]:
        root_translations = list[dict[str, str]]()

        for key, value in translations.items():
            root_translation = next(
                (x for x in root_translations if x["key"] == key.file_name),
                None,
            )

            if root_translation is None:
                root_translation = dict()
                root_translation["key"] = key.file_name
                root_translation["translations"] = list()
                root_translations.append(root_translation)

            translation = dict()
            translation["key"] = key.key
            values: dict[str, str] = {}

            for lang_name, lang_value in value.items():
                values[trim_value_prefix(lang_name)] = (
                    lang_value if lang_value else ""
                )

            translation["values"] = values

            root_translation["translations"].append(translation)

        return root_translations
