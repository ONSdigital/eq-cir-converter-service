"""Utility functions for text processing."""

import re
from collections import Counter
from collections.abc import Sequence
from copy import deepcopy
from typing import Any

from eq_cir_converter_service.config.logging_config import logging

logger = logging.getLogger(__name__)

# --- Regular Expressions ---
# Compiled regular expressions for HTML tag processing
REGEX_B_OPEN = re.compile(r"<\s*b\s*>", flags=re.IGNORECASE)
REGEX_B_CLOSE = re.compile(r"<\s*/\s*b\s*>", flags=re.IGNORECASE)
REGEX_P_TAGS = re.compile(r"</?p>", flags=re.IGNORECASE)
REGEX_BR_TAGS = re.compile(r"</?br>", flags=re.IGNORECASE)
REGEX_PARAGRAPH_SPLIT = re.compile(r"<p>(.*?)</p>", flags=re.IGNORECASE | re.DOTALL)
REGEX_PLACEHOLDER = re.compile(r"\{(.*?)\}", flags=re.IGNORECASE)


# --- HTML Tag Processing ---
def remove_and_replace_tags(text: str) -> str:
    """Cleans HTML tags from the text, replacing <b> with <strong> and removing <br> and <p> tags.

    :param text: The input text containing HTML tags.
    :return: The cleaned text with HTML tags removed or replaced.
    """
    return REGEX_P_TAGS.sub(
        "",
        REGEX_BR_TAGS.sub(
            "",
            REGEX_B_CLOSE.sub(
                "</strong>",
                REGEX_B_OPEN.sub("<strong>", text),
            ),
        ),
    ).strip()


# --- Paragraph Extraction ---
def split_paragraphs_into_list(paragraphs_string: str) -> list[str]:
    """Extracts paragraphs from string, returning a list of cleaned paragraph strings.

    :param paragraphs_string: The string to extract paragraphs from.
    :return: A list of cleaned paragraphs.
    """
    paragraphs = REGEX_PARAGRAPH_SPLIT.findall(paragraphs_string)
    # Remove empty items from the list (empties being side effects of regex)
    return [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]


# --- Placeholder Extraction ---
def extract_placeholder_names_from_text_field(text: str) -> list[str]:
    """Extracts placeholders from the text, returning a list of placeholder names.

    :param text: The input text containing placeholders.
    :return: A list of placeholder names.
    """
    return REGEX_PLACEHOLDER.findall(text)


# --- Handle "text" with "placeholders" ---
def split_paragraphs_with_placeholders(
    placeholders_dict: dict[str, str | list | object],
) -> list[str | dict[str, str | list | object]]:
    """Splits the 'text' field in the text_obj into paragraphs, cleaning HTML tags and extracting placeholders.

    :param placeholders_dict: A dictionary containing 'text' and 'placeholders'.
    example::
    {
        'placeholders': [
            'text': '<p>Hello {first_name}</p><p>{last_name}</p>',
            {
                'placeholder': 'first_name',
                'value': {
                    'identifier': 'FIRST_NAME',
                    'source': 'metadata'
                }
            },
            {
                'placeholder': 'last_name',
                'value': {
                    'identifier': 'LAST_NAME',
                    'source': 'metadata'
                }
            }
        ],
    }
    :return: A list of cleaned paragraphs or dictionaries with placeholders.
    """
    placeholder_text = str(placeholders_dict.get("text", ""))
    placeholders_list = placeholders_dict.get("placeholders", "")
    # Divide the string into paragraphs list based on presence of <p> tags
    paragraphs = split_paragraphs_into_list(placeholder_text)

    output_paragraphs: list[str | dict[str, str | list | object]] = []
    # For each separated paragraph attach the relevant placeholder(s) if present or keep the paragraph as is
    for paragraph in paragraphs:
        paragraph_with_tags_removed = remove_and_replace_tags(paragraph).strip()
        placeholder_names_with_count = Counter(extract_placeholder_names_from_text_field(paragraph_with_tags_removed))
        paragraphs_with_matching_placeholders: list[dict] = []
        for placeholder_name, count in placeholder_names_with_count.items():
            # isinstance() added for type checking purposes
            if isinstance(placeholders_list, list):
                # List that stores the placeholder definitions for each placeholder name in "text"
                paragraphs_with_placeholders = []
                for placeholder in placeholders_list:
                    # Ensure the correct placeholder is added that matches the placeholder name in "text"
                    if placeholder.get("placeholder", None) == placeholder_name:
                        paragraphs_with_placeholders = [placeholder]

                # If any placeholders added to this list, create a deep copy for each placeholder name
                if paragraphs_with_placeholders:
                    paragraphs_with_matching_placeholders.extend(
                        deepcopy(paragraphs_with_placeholders[0]) for _ in range(count)
                    )
        # If there are placeholders in the paragraph, add them to the output in the correct format (with paragraph text)
        if paragraphs_with_matching_placeholders:
            output_paragraphs.append(
                {"text": paragraph_with_tags_removed, "placeholders": paragraphs_with_matching_placeholders},
            )
        # Else just add the cleaned paragraph
        else:
            output_paragraphs.append(paragraph_with_tags_removed)

    return output_paragraphs


# --- Helper Functions for process_element ---
def process_string(string: str) -> str | list[str]:
    """Processes a string, cleaning HTML tags and splitting into paragraphs if necessary.

    :param string: The input string to process.
    :return: A cleaned string or a list of paragraphs.
    """
    if REGEX_PARAGRAPH_SPLIT.search(string):
        # If the text contains <p> tags, split into paragraphs
        # and clean each paragraph
        paragraphs = [remove_and_replace_tags(paragraph).strip() for paragraph in split_paragraphs_into_list(string)]
        # Return string if only one paragraph
        return paragraphs[0] if len(paragraphs) == 1 else paragraphs
    return remove_and_replace_tags(string).strip()


def process_placeholder(
    placeholders_dict: dict[str, str | list | object],
) -> dict[str, str | list | object] | list[str | dict[str, str | list | object]]:
    """Processes a placeholder object, cleaning HTML tags and extracting paragraphs with placeholders.

    :param placeholders_dict: A dictionary containing 'text' and possibly 'placeholders'.
    :return: A cleaned text object or a list of paragraphs with placeholders.
    """
    if REGEX_PARAGRAPH_SPLIT.search(str(placeholders_dict.get("text", ""))):
        # If the text contains <p> tags, split into paragraphs
        # and clean each paragraph, extracting placeholders
        return split_paragraphs_with_placeholders(placeholders_dict)
    placeholders_dict["text"] = remove_and_replace_tags(str(placeholders_dict["text"])).strip()
    return placeholders_dict


def process_list(list_items: Sequence[str | Sequence[Any] | dict]) -> list[str | list | object]:
    """Processes a list of elements, cleaning HTML tags and extracting paragraphs from text objects.

    :param list_items: A sequence of strings, lists, or dictionaries to process.
    :return: A list of processed elements, which may include cleaned strings or lists of paragraphs.
    """
    result: list[str | list | object] = []

    for item in list_items:
        if isinstance(item, dict):
            if expandable_key := next(
                # If the value is a string with <p> tags, extract paragraphs
                # and clean each paragraph
                # and extract placeholders
                (k for k, v in item.items() if isinstance(v, str) and REGEX_PARAGRAPH_SPLIT.search(v)),
                None,
            ):
                paragraphs = split_paragraphs_into_list(item[expandable_key])
                result.extend({expandable_key: paragraph} for paragraph in paragraphs)
            else:
                result.append(process_element(item))
        else:
            processed = process_element(item)
            if isinstance(processed, list):
                result.extend(processed)
            else:
                result.append(processed)

    return result


# --- Recursive Processor ---
def process_element(element: str | list | object) -> str | list | object:
    """Recursively processes an element, handling strings, placeholders object, lists, and dictionaries.

    :param element: The element to process, which can be a string, placeholders object, list, or dictionary.
    :return: The processed element, which may be a cleaned string, a list of paragraphs, or a dictionary.
    """
    if isinstance(element, str):
        return process_string(element)
    if isinstance(element, dict) and "text" in element:
        return process_placeholder(element)
    if isinstance(element, list):
        return process_list(element)
    if isinstance(element, dict):
        return {k: process_element(v) for k, v in element.items()}
    return element
