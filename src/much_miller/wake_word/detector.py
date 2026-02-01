"""Domain logic for wake word detection."""

WAKE_WORD = "figaro"


def contains_wake_word(text: str) -> bool:
    """Check if the text contains the wake word.

    Args:
        text: Transcribed text to check

    Returns:
        True if wake word is found, False otherwise
    """
    return WAKE_WORD in text.lower()
