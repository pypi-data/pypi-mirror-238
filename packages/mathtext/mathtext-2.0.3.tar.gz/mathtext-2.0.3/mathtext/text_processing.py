""" Run text processing sequences on a student message """

import logging
import re
import yaml

from pathlib import Path

from mathtext.constants import TOKENS2INT_ERROR_INT, DATA_DIR
from mathtext.utils.converters import text2num, text2int, text2float
from mathtext.utils.extractors import (
    extract_approved_answer_from_phrase,
    extract_approved_keyword_from_phrase,
)
from mathtext.utils.formatters import (
    text2equation,
    text2exponent,
    text2fraction,
    text2time,
)


log = logging.getLogger(__name__)


regex_evaluation_functions = {
    "text2exponent": text2exponent,
    "text2fraction": text2fraction,
    "text2time": text2time,
    "text2equation": text2equation,
}


def format_int_or_float_answer(text):
    """Attempts to convert a student message into an int or float

    >>> format_int_or_float_answer("12")
    12
    >>> format_int_or_float_answer("maybe 0.5")
    0.5
    >>> format_int_or_float_answer("I don't know")
    32202
    >>> format_int_or_float_answer("¹1")
    32202
    """
    try:
        num = text2num(text)
        if num != TOKENS2INT_ERROR_INT:
            return num

        result = text2float(text)
        if result and result != None:
            return result

        result = text2int(text)
        if result and result != 0:
            return result
    except ValueError:
        log.exception("ValueError")
    except Exception:
        log.exception("Exception")
    return TOKENS2INT_ERROR_INT


# TODO: Support instantiating variables from API
# def load_config(filepath=DATA_DIR / "v2_text_processing_config.yaml"):
#     kwargs = yaml.safe_load(Path(filepath).open())
#     init(**kwargs)


# def init(**kwargs):
#     # global APPROVED_RESPONSE_CASES, NUMBER_MAP
#     for k, v in kwargs.items():
#         globals()[k.upper()] = v


def run_regex_evaluations(message_text, expected_answer):
    """Calls functions that evaluate for specific answer types with regex"""
    regex_functions = "text2time text2equation text2fraction text2exponent".split()
    for regex_function in regex_functions:
        eval_function = regex_evaluation_functions[regex_function]
        result = eval_function(message_text, expected_answer)
        if result != TOKENS2INT_ERROR_INT and result:
            return result


def normalize_message_and_answer(student_message, expected_answer):
    """
    >>> normalize_message_and_answer("Maybe 5000", "5,000")
    ('maybe 5000', '5000')
    >>> normalize_message_and_answer("Yeah I think so", "Yes")
    ('yeah i think so', 'yes')
    """
    normalized_student_message = (
        str(student_message).strip().replace(",", "").lower()[0:100]
    )
    normalized_expected_answer = str(expected_answer).strip().replace(",", "").lower()
    return normalized_student_message, normalized_expected_answer


def run_text_evaluations_on_test_case(message_text, expected_answer):
    result = ""
    (
        normalized_student_message,
        normalized_expected_answer,
    ) = normalize_message_and_answer(message_text, expected_answer)

    if normalized_student_message.replace(
        " ", ""
    ) == normalized_expected_answer.replace(" ", ""):
        return expected_answer

    tokenized_student_message = normalized_student_message.split()

    result = extract_approved_answer_from_phrase(
        tokenized_student_message, normalized_expected_answer, expected_answer
    )
    if result:
        return result[0]

    result = extract_approved_keyword_from_phrase(
        tokenized_student_message, normalized_expected_answer, expected_answer
    )
    if result:
        return result

    result = run_regex_evaluations(message_text, expected_answer)
    if result:
        return result

    result = format_int_or_float_answer(message_text)
    if result != TOKENS2INT_ERROR_INT and result:
        return str(result)

    return TOKENS2INT_ERROR_INT
