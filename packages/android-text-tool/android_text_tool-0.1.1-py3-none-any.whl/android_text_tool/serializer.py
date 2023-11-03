from abc import abstractmethod
from android_text_tool.translarions_storage import TranslationsStorage


class TranslationsSerializer:
    """
    Translations serializer.
    """

    def __init__(self, default_language: str = "en"):
        """
        Translations serializer. This is an abstract class.

        :param default_language: Default language for empty translations.
        """
        self.default_language = default_language

    @abstractmethod
    def save(self, translations: TranslationsStorage):
        """
        Save translations to a file.
        Must be implemented in a subclass.
        """
        raise NotImplementedError()
