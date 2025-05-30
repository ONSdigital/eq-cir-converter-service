"""Utility functions for text processing."""

import re

from eq_cir_converter_service.config.logging_config import logging

logger = logging.getLogger(__name__)


def replace_b_with_strong(text: str) -> str:
    """Replaces <b> and </b> tags with <strong> and </strong>."""
    logger.debug("Replacing <b> with <strong> in text: %s", text)

    # Replace <b> with <strong> and </b> with </strong>
    return re.sub(
        r"<\s*/\s*b\s*>",
        "</strong>",
        re.sub(r"<\s*b\s*>", "<strong>", text, flags=re.IGNORECASE),
        flags=re.IGNORECASE,
    )


def split_paragraphs(text: str) -> list[str]:
    """Splits the text content by <p>...</p> and returns cleaned parts."""
    logger.debug("Splitting paragraphs from text: %s", text)

    # Use regex to find all <p>...</p> sections
    parts = re.findall(r"<p>(.*?)</p>", text, flags=re.DOTALL)
    logger.debug("Split paragraphs: %s", parts)
    return [part.strip() for part in parts if part.strip()]


def clean_text(text: str) -> str:
    """Removes <p>, <br> tags and replaces <b> tags with <strong> tags in the text."""
    logger.debug("Cleaning text: %s", text)

    text = re.sub(r"</?br>", "", text)  # Remove <br> tags
    text = re.sub(r"</?p>", "", text)  # Remove <p> tags
    text = replace_b_with_strong(text)  # Replace <b> with <strong>
    logger.debug("Cleaned text: %s", text)
    return text.strip()
