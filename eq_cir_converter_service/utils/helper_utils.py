"""Utility functions for text processing."""

import re
from collections import Counter
from copy import deepcopy

from eq_cir_converter_service.config.logging_config import logging

logger = logging.getLogger(__name__)

# --- Regular Expressions ---
# Compiled regular expressions for HTML tag processing
REGEX_B_OPEN = re.compile(r"<\s*b\s*>", flags=re.IGNORECASE)
REGEX_B_CLOSE = re.compile(r"<\s*/\s*b\s*>", flags=re.IGNORECASE)
REGEX_P_TAGS = re.compile(r"</?p>", flags=re.IGNORECASE)
REGEX_BR_TAGS = re.compile(r"</?br>", flags=re.IGNORECASE)
REGEX_PARA_SPLIT = re.compile(r"<p>(.*?)</p>", flags=re.IGNORECASE | re.DOTALL)
REGEX_PLACEHOLDER = re.compile(r"\{(.*?)\}", flags=re.IGNORECASE)


# --- HTML Tag Processing ---
def clean_html_tags(text: str) -> str:
    """Cleans HTML tags from the text, replacing <b> with <strong> and removing <br> and <p> tags."""
    text = REGEX_B_OPEN.sub("<strong>", text)  # Replace <b> with <strong>
    text = REGEX_B_CLOSE.sub("</strong>", text)  # Replace </b> with </strong>
    text = REGEX_BR_TAGS.sub("", text)  # Remove <br> tags
    text = REGEX_P_TAGS.sub("", text)  # Remove <p> tags
    return text.strip()


# --- Paragraph Extraction ---
def extract_paragraphs(html: str) -> list[str]:
    """Extracts paragraphs from HTML content, returning a list of cleaned paragraph strings."""
    return REGEX_PARA_SPLIT.findall(html)


# --- Placeholder Extraction ---
def extract_placeholders(text: str) -> list[str]:
    """Extracts placeholders from the text, returning a list of placeholder names."""
    return REGEX_PLACEHOLDER.findall(text)


# --- Handle "text" with "placeholders" ---
def split_text_with_placeholders(
    text_obj: dict[str, str | list | object],
) -> list[str | dict[str, str | list | object]]:
    """Splits the 'text' field in the text_obj into paragraphs, cleaning HTML tags and extracting placeholders."""
    raw_text = text_obj.get("text", "")
    placeholders = text_obj.get("placeholders", [])
    paragraphs = extract_paragraphs(raw_text)

    result = []
    for para in paragraphs:
        cleaned = clean_html_tags(para).strip()
        if not cleaned:
            continue

        used_counts = Counter(extract_placeholders(cleaned))
        relevant = []
        for ph_name, count in used_counts.items():
            matching = [ph for ph in placeholders if ph["placeholder"] == ph_name]
            if matching:
                relevant.extend(deepcopy(matching[0]) for _ in range(count))

        if relevant:
            result.append({"text": cleaned, "placeholders": relevant})
        else:
            result.append(cleaned)

    return result


# --- Helper Functions for process_element ---
def process_string(text: str) -> str | list[str]:
    """Processes a string, cleaning HTML tags and splitting into paragraphs if necessary."""
    if REGEX_PARA_SPLIT.search(text):
        # If the text contains <p> tags, split into paragraphs
        # and clean each paragraph
        paragraphs = [clean_html_tags(p).strip() for p in extract_paragraphs(text) if clean_html_tags(p).strip()]
        if len(paragraphs) == 1:
            return paragraphs[0]  # return string if only one paragraph
        return paragraphs
    return clean_html_tags(text).strip()


def process_text_object(
    obj: dict[str, str | list | object],
) -> dict[str, str | list | object] | list[str | dict[str, str | list | object]]:
    """Processes a text object, cleaning HTML tags and extracting paragraphs with placeholders."""
    if REGEX_PARA_SPLIT.search(obj.get("text", "")):
        # If the text contains <p> tags, split into paragraphs
        # and clean each paragraph, extracting placeholders
        return split_text_with_placeholders(obj)
    obj["text"] = clean_html_tags(obj["text"]).strip()
    return obj


def process_list(elements: list[str | list | object]) -> list[str | list | object]:
    """Processes a list of elements, cleaning HTML tags and extracting paragraphs from text objects."""
    result: list[str | list | object] = []
    for item in elements:
        if isinstance(item, dict):
            expanded = False
            for k, v in item.items():
                if isinstance(v, str) and REGEX_PARA_SPLIT.search(v):
                    # If the value is a string with <p> tags, extract paragraphs
                    # and clean each paragraph
                    # and extract placeholders
                    paragraphs = extract_paragraphs(v)
                    for para in paragraphs:
                        cleaned = clean_html_tags(para).strip()
                        if cleaned:
                            result.append({k: cleaned})
                    expanded = True
                    break
            if not expanded:
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
    """Recursively processes an element, handling strings, text objects, lists, and dictionaries."""
    if isinstance(element, str):
        return process_string(element)
    if isinstance(element, dict) and "text" in element:
        return process_text_object(element)
    if isinstance(element, list):
        return process_list(element)
    if isinstance(element, dict):
        return {k: process_element(v) for k, v in element.items()}
    return element
