from android_text_tool.serializer import TranslationsSerializer
from android_text_tool.translarions_storage import TranslationsStorage
from android_text_tool.utils import trim_value_prefix


import csv


class TranslationsCSVSerializer(TranslationsSerializer):
    def save(self, translations: TranslationsStorage):
        _columns = set()
        for _, value in translations.items():
            valueNames = sorted(value.keys())
            valueNames = [trim_value_prefix(x) for x in valueNames if x]
            _columns.update(valueNames)

        colums = ["key"] + list(_columns)

        f = open("result.csv", "w")
        writer = csv.writer(f)

        writer.writerow(colums)

        for key, value in translations.items():
            values = [value.get(x) for x in _columns if x]
            writer.writerow([key.key] + values)

        f.close()
