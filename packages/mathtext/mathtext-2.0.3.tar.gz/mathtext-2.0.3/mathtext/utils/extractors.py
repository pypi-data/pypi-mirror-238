import copy

from mathtext.constants import TOKENS2INT_ERROR_INT
from mathtext.utils.checkers import has_multiple_valid_answers, has_multiple_numbers
from mathtext.utils.default_values import (
    APPROVED_RESPONSES_BY_TYPE,
    KEYWORD_LOOKUP,
    TEXT_ANSWER_LOOKUP,
)


def extract_approved_responses_to_list(
    tokenized_student_message, normalized_expected_answer
):
    """Searches the student message for predefined answers or keywords as well as common mispellings

    >>> extract_approved_responses_to_list(['yes', 'hint'], '15')
    [('answer', 'yes')]
    >>> extract_approved_responses_to_list(['2'], '3')
    []
    """
    answer_dict = copy.deepcopy(APPROVED_RESPONSES_BY_TYPE)
    if not answer_dict.get(normalized_expected_answer, ""):
        answer_dict[normalized_expected_answer] = "expected_answer"

    extracted_approved_responses = [
        (
            answer_dict[token.replace(".", "").replace("*", "")],
            token.replace(".", "").replace("*", ""),
        )
        for token in tokenized_student_message
        if token.replace(".", "").replace("*", "") in answer_dict
    ]
    return extracted_approved_responses


def extract_approved_answer_from_phrase(
    tokenized_student_message, normalized_expected_answer, expected_answer
):
    """Searches a message for predefined answers or keywords as well common mispellings

    >>> extract_approved_answer_from_phrase(['maybe', 'y'], 'yes', 'Yes')
    ('Yes', True)
    >>> extract_approved_answer_from_phrase(['*menu*', 'y'], 'yes', 'Yes')
    ('Yes', True)
    >>> extract_approved_answer_from_phrase(['maybe', '5000'], '5000', '5000')
    ('5000', True)
    """
    extracted_approved_responses = extract_approved_responses_to_list(
        tokenized_student_message, normalized_expected_answer
    )
    # Sends to number eval if multiple numbers
    if has_multiple_numbers(tokenized_student_message):
        return TOKENS2INT_ERROR_INT, False
    # Sends an error if input has multiple valid answers (ie., T and F)
    if has_multiple_valid_answers(extracted_approved_responses):
        return TOKENS2INT_ERROR_INT, False

    # Catches new expected answer cases (not in APPROVED_RESPONSES_BY_TYPE yet)
    for answer_type in extracted_approved_responses:
        if answer_type[0] == "expected_answer":
            return expected_answer, True

    for answer_type in extracted_approved_responses:
        if (
            answer_type[0] == "answer"
            and normalized_expected_answer in TEXT_ANSWER_LOOKUP[answer_type[1]]
        ):
            return expected_answer, True

    for answer_type in extracted_approved_responses:
        if answer_type[0] == "answer":
            # Look up the key of the expected answer to look up the appropriate value for the student answer

            try:
                lookup_index = TEXT_ANSWER_LOOKUP[normalized_expected_answer].index(
                    normalized_expected_answer
                )
            except:
                lookup_index = 0

            try:
                answer = TEXT_ANSWER_LOOKUP[answer_type[1]][lookup_index]
            except:
                answer = TEXT_ANSWER_LOOKUP[answer_type[1]][0]
            return answer.capitalize(), False

    return TOKENS2INT_ERROR_INT, False


def extract_approved_keyword_from_phrase(
    tokenized_student_message, normalized_expected_answer, expected_answer
):
    """Searches a message for predefined answers or keywords as well common mispellings

    >>> extract_approved_keyword_from_phrase(['I', 'need', 'the', 'menu'], 'yes', 'Yes')
    'menu'
    """
    extracted_approved_responses = extract_approved_responses_to_list(
        tokenized_student_message, normalized_expected_answer
    )
    for answer_type in extracted_approved_responses:
        if answer_type[0] == "keyword":
            return KEYWORD_LOOKUP[answer_type[1]]
    return TOKENS2INT_ERROR_INT
