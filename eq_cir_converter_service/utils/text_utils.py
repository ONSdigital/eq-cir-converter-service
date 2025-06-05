"""Utility functions for text processing."""

import re

from eq_cir_converter_service.config.logging_config import logging

logger = logging.getLogger(__name__)

REGEX_B_OPEN = re.compile(r"<\s*b\s*>", flags=re.IGNORECASE)
REGEX_B_CLOSE = re.compile(r"<\s*/\s*b\s*>", flags=re.IGNORECASE)
REGEX_P_TAGS = re.compile(r"</?p>", flags=re.IGNORECASE)
REGEX_BR_TAGS = re.compile(r"</?br>", flags=re.IGNORECASE)
REGEX_PARA_SPLIT = re.compile(r"<p>(.*?)</p>", flags=re.DOTALL)


def replace_b_with_strong(text: str) -> str:
    """Replaces <b> and </b> tags with <strong> and </strong>."""
    logger.debug("Replacing <b> with <strong> in text: %s", text)

    text = REGEX_B_OPEN.sub("<strong>", text)
    text = REGEX_B_CLOSE.sub("</strong>", text)
    logger.debug("Replaced text: %s", text)
    return text


def split_paragraphs(text: dict[str, str | list | object] | str) -> list[str]:
    """Splits the text content by <p>...</p> and returns cleaned parts."""
    logger.debug("Splitting paragraphs from text: %s", text)

    # Use regex to find all <p>...</p> sections
    parts = REGEX_PARA_SPLIT.findall(text)
    logger.debug("Split paragraphs: %s", parts)
    return [part.strip() for part in parts if part.strip()]


def clean_text(text: str) -> str:
    """Removes <p>, <br> tags and replaces <b> tags with <strong> tags in the text."""
    logger.debug("Cleaning text: %s", text)

    text = REGEX_BR_TAGS.sub("", text)  # Remove <br> tags
    text = REGEX_P_TAGS.sub("", text)  # Remove <p> tags
    text = replace_b_with_strong(text)  # Replace <b> with <strong>
    logger.debug("Cleaned text: %s", text)
    return text.strip()
