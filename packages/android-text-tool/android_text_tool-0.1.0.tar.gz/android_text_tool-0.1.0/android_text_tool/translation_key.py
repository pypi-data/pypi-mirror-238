from dataclasses import dataclass


@dataclass(frozen=True)
class TranslationKey:
    """A translation key."""

    file_name: str
    key: str
