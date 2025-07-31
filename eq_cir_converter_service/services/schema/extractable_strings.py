"""Extractable strings from EQ schemas.

This module defines a list of JSON paths and their descriptions for extracting
strings from EQ schemas. It also provides context definitions for better understanding
of the extracted strings.
"""

EXTRACTABLE_STRINGS = [
    {"json_path": "$.legal_basis", "description": "Questionnaire legal basis"},
    {"json_path": "$.messages.*", "description": "Global answer error message"},
    {
        "json_path": "$.submission.guidance",
        "description": "Submission guidance",
    },
    {"json_path": "$.submission.warning", "description": "Submission warning"},
    {
        "json_path": "$.post_submission.guidance.contents[*].title",
        "description": "Post submission guidance heading",
    },
    {
        "json_path": "$.post_submission.guidance.contents[*].description",
        "description": "Post submission guidance description",
    },
    {
        "json_path": "$.post_submission.guidance.contents[*].list[*]",
        "description": "Post submission guidance list item",
        "additional_context": ["ListHeading", "ListDescription"],
    },
    {"json_path": "$..page_title", "description": "Page title"},
    {
        "json_path": "$.sections[*].repeat.title",
        "description": "Section title (repeating section)",
    },
    {
        "json_path": "$.sections[*].repeat.page_title",
        "description": "Section page title suffix (repeating section)",
    },
    {
        "json_path": "$.sections[*].summary.items[*].title",
        "description": "Section summary item title",
    },
    {
        "json_path": "$.sections[*].summary.items[*].add_link_text",
        "description": "Section summary list add link",
    },
    {
        "json_path": "$.sections[*].summary.items[*].empty_list_text",
        "description": "Section summary empty list text",
    },
    {
        "json_path": "$.sections[*].summary.items[*].item_label",
        "description": "Label for the item title on a section summary",
    },
    {"json_path": "$..blocks[*].title", "description": "Block title"},
    {
        "json_path": "$..summary.item_title",
        "description": "List collector summary item",
    },
    {
        "json_path": "$..summary.empty_list_text",
        "description": "List collector empty list text",
    },
    {
        "json_path": "$..summary.add_link_text",
        "description": "List collector add link text",
    },
    {
        "json_path": "$..summary.item_label",
        "description": "List collector item label",
    },
    {
        "json_path": "$..add_block.cancel_text",
        "description": "List collector add block cancel link",
    },
    {
        "json_path": "$..repeating_blocks[*].question.title.text",
        "description": "Repeating block question",
    },
    {"json_path": "$..content.title", "description": "Content page main heading"},
    {"json_path": "$..content.instruction[*]", "description": "Content instruction"},
    {
        "json_path": "$..content.contents[*].title",
        "description": "Content page heading",
        "context": "Content",
    },
    {
        "json_path": "$..content.contents[*].description",
        "description": "Content page description",
        "context": "Content",
    },
    {
        "json_path": "$..content.contents[*].list[*]",
        "description": "Content page list item",
        "context": "Content",
        "additional_context": ["ListHeading", "ListDescription"],
    },
    {
        "json_path": "$..content.contents[*].definition.title",
        "description": "Definition title",
        "context": "Content",
    },
    {
        "json_path": "$..content.contents[*].definition.contents[*].description",
        "description": "Definition description",
        "context": "Content",
    },
    {
        "json_path": "$..content_variants[*].content.title",
        "description": "Content page heading",
        "context": "Content",
    },
    {
        "json_path": "$..content_variants[*].content.contents[*].description",
        "description": "Content page description",
        "context": "Content",
    },
    {
        "json_path": "$..question.description[*]",
        "description": "Question description",
        "context": "Question",
    },
    {
        "json_path": "$..question.instruction[*]",
        "description": "Question instruction",
        "context": "Question",
    },
    {
        "json_path": "$..question.warning",
        "description": "Question warning",
        "context": "Question",
    },
    {
        "json_path": "$..question.definitions[*].title",
        "description": "Question definition link",
        "context": "Question",
    },
    {
        "json_path": "$..question.definitions[*].contents[*].title",
        "description": "Question definition heading",
        "context": "Question",
    },
    {
        "json_path": "$..question.definitions[*].contents[*].description",
        "description": "Question definition description",
        "context": "Question",
    },
    {
        "json_path": "$..question.definitions[*].contents[*].list[*]",
        "description": "Question definition list item",
        "context": "Question",
        "additional_context": ["ListHeading", "ListDescription"],
    },
    {
        "json_path": "$..question.definition.title",
        "description": "Question definition heading",
        "context": "Question",
    },
    {
        "json_path": "$..question.definition.contents[*].title",
        "description": "Question definition heading",
        "context": "Question",
    },
    {
        "json_path": "$..question.definition.contents[*].description",
        "description": "Question definition description",
        "context": "Question",
    },
    {
        "json_path": "$..question.definition.contents[*].list[*]",
        "description": "Question definition list item",
        "context": "Question",
        "additional_context": ["ListHeading", "ListDescription"],
    },
    {
        "json_path": "$..question.guidance.contents[*].title",
        "description": "Question guidance heading",
        "context": "Question",
    },
    {
        "json_path": "$..question.guidance.contents[*].description",
        "description": "Question guidance description",
        "context": "Question",
    },
    {
        "json_path": "$..question.guidance.contents[*].list[*]",
        "description": "Question guidance list item",
        "context": "Question",
        "additional_context": ["ListHeading", "ListDescription"],
    },
    {
        "json_path": "$..question.calculation.title",
        "description": "Question calculation title",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].validation.messages.*",
        "description": "Answer error message",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].label",
        "description": "Answer",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].instruction",
        "description": "Checkbox answer instruction",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].placeholder",
        "description": "Dropdown field placeholder text",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].description",
        "description": "Answer description",
        "context": "Question",
        "additional_context": ["Answer"],
    },
    {
        "json_path": "$..answers[*].playback",
        "description": "Relationships playback template",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].options[*].label",
        "description": "Answer option",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].options[*].description",
        "description": "Answer option description",
        "context": "Question",
        "additional_context": ["AnswerOption"],
    },
    {
        "json_path": "$..answers[*].options[*].detail_answer.label",
        "description": "Detail answer label",
        "context": "Question",
        "additional_context": ["AnswerOption"],
    },
    {
        "json_path": "$..answers[*].options[*].detail_answer.description",
        "description": "Detail answer description",
        "context": "Question",
        "additional_context": ["AnswerOption"],
    },
    {
        "json_path": "$..answers[*].options[*].title",
        "description": "Relationships answer option question text",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].options[*].playback",
        "description": "Relationships answer option playback text",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].guidance.show_guidance",
        "description": "Answer guidance show link",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].guidance.hide_guidance",
        "description": "Answer guidance hide link",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].guidance.contents[*].title",
        "description": "Answer guidance heading",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].guidance.contents[*].description",
        "description": "Answer guidance description",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].guidance.contents[*].list[*]",
        "description": "Answer guidance list item",
        "context": "Question",
        "additional_context": ["ListHeading", "ListDescription"],
    },
    {
        "json_path": "$..primary_content[*].title",
        "description": "Introduction main title",
    },
    {
        "json_path": "$..primary_content[*].contents[*].list[*]",
        "description": "Introduction main list item",
        "context": "PrimaryContent",
        "additional_context": ["ListHeading", "ListDescription"],
    },
    {
        "json_path": "$..primary_content[*].contents[*].description",
        "description": "Introduction main description",
        "context": "PrimaryContent",
    },
    {
        "json_path": "$..primary_content[*].contents[*].guidance.contents[*].title",
        "description": "Introduction main guidance title",
        "context": "PrimaryContent",
    },
    {
        "json_path": "$..primary_content[*].contents[*].guidance.contents[*].description",
        "description": "Introduction main guidance description",
        "context": "PrimaryContent",
        "additional_context": ["ListHeading"],
    },
    {
        "json_path": "$..primary_content[*].contents[*].guidance.contents[*].list[*]",
        "description": "Introduction main guidance list",
        "context": "PrimaryContent",
        "additional_context": ["ListHeading"],
    },
    {
        "json_path": "$..preview_content.title",
        "description": "Introduction preview title",
    },
    {
        "json_path": "$..preview_content.contents[*].description",
        "description": "Introduction preview description",
        "context": "PreviewContent",
    },
    {
        "json_path": "$..preview_content.questions[*].question",
        "description": "Introduction preview question title",
        "context": "PreviewContent",
    },
    {
        "json_path": "$..preview_content.questions[*].contents[*].description",
        "description": "Introduction preview question description",
        "context": "PreviewContent",
        "additional_context": ["PreviewQuestionListHeading"],
    },
    {
        "json_path": "$..preview_content.questions[*].contents[*].list[*]",
        "description": "Introduction preview question list item",
        "context": "PreviewContent",
        "additional_context": ["PreviewQuestionListHeading"],
    },
    {
        "json_path": "$..secondary_content[*].contents[*].title",
        "description": "Introduction additional title",
    },
    {
        "json_path": "$..secondary_content[*].contents[*].list[*]",
        "description": "Introduction additional list item",
        "context": "ListHeading",
        "additional_context": ["ListDescription"],
    },
    {
        "json_path": "$..secondary_content[*].contents[*].description",
        "description": "Introduction additional description",
        "context": "ListHeading",
    },
]
