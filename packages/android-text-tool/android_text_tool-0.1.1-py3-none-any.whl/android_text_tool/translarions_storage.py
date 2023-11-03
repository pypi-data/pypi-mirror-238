from .translation_key import TranslationKey


class TranslationsStorage:
    """
    Translations storage.
    Format - map of Translation key to dict.
    Value dict is LangCode to translation
    """

    def __init__(self) -> None:
        self.translations: dict[TranslationKey, dict[str, str]] = {}
