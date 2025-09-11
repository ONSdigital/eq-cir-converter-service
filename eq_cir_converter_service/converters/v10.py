"""v10 converter utility functions."""

import re
from collections import Counter

from jsonpath_ng.ext import parse

from eq_cir_converter_service.types.custom_types import Schema

# Compiled regular expressions for HTML tag processing
REGEX_B_OPEN = re.compile(r"<\s*b\s*>", flags=re.IGNORECASE)
REGEX_B_CLOSE = re.compile(r"<\s*/\s*b\s*>", flags=re.IGNORECASE)
REGEX_P_TAGS = re.compile(r"</?p>", flags=re.IGNORECASE)
REGEX_BR_TAGS = re.compile(r"</?br>", flags=re.IGNORECASE)
REGEX_PARAGRAPH_SPLIT = re.compile(r"<p>(.*?)</p>", flags=re.IGNORECASE | re.DOTALL)
REGEX_PLACEHOLDER = re.compile(r"\{(.*?)}", flags=re.IGNORECASE)

PlaceholdersDict = dict[str, str | list | object]


def convert_to_v10(schema: Schema, paths: list[str]) -> Schema:
    """Transforms the schema dictionary based on the provided JSONPath expressions.

    Following steps are performed:
    1. Iterate over each JSONPath expression in the paths list.
    2. For each path, use the jsonpath-ng library to find all matching elements
    in the schema.
    3. For each matched element, retrieve the context (the parent structure) and
    the path data (information about the matched element).
    4. Return a single context or list of contexts (e.g. "$.title",
    can only return one survey title, so a single context returned but "$..question.description[*]"
    will likely return multiple contexts, depending on schema structure),
    5. Process the element accordingly using helper functions.
    6. Finally, return the transformed schema.

    Parameters:
    - schema: The input schema to transform.
    - paths: A list containing JSONPath paths to look for.

    Returns:
    - A new schema with the transformations applied.
    """
    for path in paths:
        jsonpath_expression = parse(path)
        for extracted_value in jsonpath_expression.find(schema):
            context = extracted_value.context.value
            path_data = extracted_value.path
            if hasattr(path_data, "index"):
                process_context_list(context, path_data.index)
            elif hasattr(path_data, "fields"):
                process_context_dict(context, path_data.fields[0])

    return schema


def get_sanitised_text(text: str) -> str:
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


def split_paragraphs_into_list(paragraphs_string: str) -> list[str]:
    """Extracts paragraphs from string, returning a list of cleaned paragraph strings.

    :param paragraphs_string: The string to extract paragraphs from.
    :return: A list of cleaned paragraphs.
    """
    paragraphs = REGEX_PARAGRAPH_SPLIT.findall(paragraphs_string)
    # Remove empty items from the list (empties being side effects of regex)
    return [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]


def extract_placeholder_names_from_text_field(text: str) -> list[str]:
    """Extracts placeholders from the text, returning a list of placeholder names.

    :param text: The input text containing placeholders.
    :return: A list of placeholder names.
    """
    return REGEX_PLACEHOLDER.findall(text)


def split_paragraphs_with_placeholders(
    placeholders_dict: PlaceholdersDict,
) -> list[str | PlaceholdersDict]:
    """Splits the 'text' field in the text_obj into paragraphs, cleaning HTML tags and extracting placeholders.

    Following steps are performed:
    1. Split the 'text' field into paragraphs based on <p> tags.
    2. For each paragraph:
        - Clean HTML tags from each paragraph.
        - Check for placeholders in paragraph
        - Attach relevant placeholder definitions (if any) from the 'placeholders' list.
    3. Return a list of cleaned paragraphs or dictionaries with placeholders.

    :param placeholders_dict: A dictionary containing 'text' and 'placeholders'.
    example::
    Input:
    {
      "text": "<p>Hello {first_name}</p><p>{last_name}</p>",
      "placeholders": [
        {
          "placeholder": "first_name",
          "value": {
            "identifier": "FIRST_NAME",
            "source": "metadata"
          }
        },
        {
          "placeholder": "last_name",
          "value": {
            "identifier": "LAST_NAME",
            "source": "metadata"
          }
        }
      ]
    }
    Output:
    {
      "text": "Hello {first_name}",
      "placeholders": [
        {
          "placeholder": "first_name",
          "value": {
            "identifier": "FIRST_NAME",
            "source": "metadata"
          }
        }
      ]
    },
    {
      "text": "{last_name}",
      "placeholders": [
        {
          "placeholder": "last_name",
          "value": {
            "identifier": "LAST_NAME",
            "source": "metadata"
          }
        }
      ]
    }
    :return: A list of cleaned paragraphs or dictionaries with placeholders.
    """
    placeholder_text = str(placeholders_dict.get("text", ""))
    placeholders = placeholders_dict.get("placeholders", [])
    paragraphs = split_paragraphs_into_list(placeholder_text)

    output_paragraphs: list[str | dict[str, str | list | object]] = []
    for paragraph in paragraphs:
        sanitised_paragraph = get_sanitised_text(paragraph)
        placeholders_found_in_paragraph = Counter(extract_placeholder_names_from_text_field(sanitised_paragraph))
        paragraphs_with_matching_placeholders: list[dict] = []
        for placeholder_name, count in placeholders_found_in_paragraph.items():
            paragraphs_with_placeholders_definitions = []
            # placeholders are always a list
            for placeholder in placeholders:  # type: ignore
                if placeholder.get("placeholder", None) == placeholder_name:
                    paragraphs_with_placeholders_definitions = [placeholder]

            if paragraphs_with_placeholders_definitions:
                paragraphs_with_matching_placeholders.extend(
                    paragraphs_with_placeholders_definitions[0] for _ in range(count)
                )
        if paragraphs_with_matching_placeholders:
            output_paragraphs.append(
                {"text": sanitised_paragraph, "placeholders": paragraphs_with_matching_placeholders},
            )
        else:
            output_paragraphs.append(sanitised_paragraph)

    return output_paragraphs


def process_string(string: str) -> str | list[str]:
    """Processes a string, cleaning HTML tags and splitting into paragraphs if necessary.

    :param string: The input string to process.
    :return: A cleaned string or a list of paragraphs.
    """
    if REGEX_PARAGRAPH_SPLIT.search(string):
        # If the text contains <p> tags, split into paragraphs
        # and clean each paragraph
        paragraphs = [get_sanitised_text(paragraph) for paragraph in split_paragraphs_into_list(string)]
        # Return string if only one paragraph
        return paragraphs[0] if len(paragraphs) == 1 else paragraphs
    return get_sanitised_text(string)


def process_placeholder(
    placeholders_dict: PlaceholdersDict,
) -> PlaceholdersDict | list[str | PlaceholdersDict]:
    """Processes a placeholder object, cleaning HTML tags and extracting paragraphs with placeholders.

    :param placeholders_dict: A dictionary containing 'text' and possibly 'placeholders'.
    :return: A cleaned text object or a list of paragraphs with placeholders.
    """
    if REGEX_PARAGRAPH_SPLIT.search(str(placeholders_dict.get("text", ""))):
        # If the text contains <p> tags, split into paragraphs
        # and clean each paragraph, extracting placeholders
        return split_paragraphs_with_placeholders(placeholders_dict)
    placeholders_dict["text"] = get_sanitised_text(str(placeholders_dict["text"]))
    return placeholders_dict


def process_list(list_items: list[str | list | dict]) -> list[str | list | dict]:
    """Processes a list of elements, cleaning HTML tags and extracting paragraphs from text objects.

    :param list_items: A sequence of strings, lists, or dictionaries to process.
    :return: A list of processed elements, which may include cleaned strings or lists of paragraphs.
    """
    transformed_list: list[str | list | dict] = []

    for item in list_items:
        if isinstance(item, dict):
            expandable_key = next(
                (key for key, value in item.items() if isinstance(value, str) and REGEX_PARAGRAPH_SPLIT.search(value)),
                None,
            )
            if expandable_key is not None:
                paragraphs = split_paragraphs_into_list(item[expandable_key])
                transformed_list.extend({expandable_key: paragraph} for paragraph in paragraphs)
            else:
                transformed_list.append(process_item(item))
        else:
            processed = process_item(item)
            if isinstance(processed, list):
                transformed_list.extend(processed)
            else:
                transformed_list.append(processed)

    return transformed_list


def process_item(item: str | list | dict) -> str | list | dict:
    """Recursively processes an item, handling strings, lists, and dictionaries.

    :param item: The item to process, which can be a string, list, or dictionary.
    :return: The processed item, which may be a cleaned string, a list of paragraphs, or a dictionary.
    """
    if isinstance(item, str):
        return process_string(item)
    if isinstance(item, dict):
        if "text" in item:
            return process_placeholder(item)
        return {key: process_item(value) for key, value in item.items()}
    return process_list(item)


def process_context_dict(context: dict, key: str) -> None:
    """Processes a dictionary context by updating the value at the given key."""
    context[key] = process_item(context[key])


def process_context_list(context: list, index: int) -> None:
    """Processes a list context by updating or expanding the value at the given index."""
    processed_item = process_item(context[index])
    if isinstance(processed_item, list):
        # Replaces the slice of a list (context) with the value of "processed" to accommodate placeholder objects
        # Multi paragraphs single element replaced with the actual multiple elements after processing
        # from index of the original element onwards
        context[index : index + 1] = processed_item
    else:
        context[index] = processed_item
