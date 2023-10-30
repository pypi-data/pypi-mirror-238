""" Utilites for processing chatbot message text to extract number words (text2int) """
import datetime
import re

from unidecode import unidecode

from mathtext.constants import TOKENS2INT_ERROR_INT
from mathtext.utils.checkers import is_time


def text2time(text, expected_answer=None):
    """Converts a time string or object to a hh:mm formatted str or returns error code
    >>> text2time("11:30")
    '11:30'
    >>> text2time("10: 20")
    '10:20'
    >>> text2time("13:20 PM")
    '13:20'
    >>> text2time("0:50")
    '0:50'
    >>> text2time("09:22")
    '9:22'
    >>> text2time("I don't know")
    32202
    >>> text2time("Maybe it's thirty")
    32202
    >>> text2time("2.0")
    32202
    """
    formatted_time = text
    try:
        timestamp = datetime.datetime.strptime(text[3:-1], "%H:%M:%S")
        formatted_time = timestamp.strftime("%H:%M")
    except ValueError:
        pass

    extracted_time = re.findall(r"\b\d{1,2}\s*:\s*\d{2}\b", formatted_time)
    if not extracted_time:
        return TOKENS2INT_ERROR_INT

    text_normalized = (
        extracted_time[0].lower().replace(" ", "").replace("am", "").replace("pm", "")
    )

    # Remove leading 0 if 2 or more digits
    text_reformatted = re.sub(r"\b(?<!\d)0(\d{1,2}?:)\b", r"\1", text_normalized)

    if not is_time(text_reformatted):
        return TOKENS2INT_ERROR_INT
    return text_reformatted


symbol_answer_types = {
    ">": [">", "g", "gt", "greater"],
    "<": ["<", "l", "lt", "less"],
    ">=": [">=", "gte"],
    "<=": ["<=", "lte"],
    "=": ["=", "e", "equal"],
}


def text2symbol(text, expected_answer):
    """Returns a properly formatted >, <, = answer or the error code

    >>> text2symbol(">", ">")
    '>'
    >>> text2symbol(">=", ">=")
    '>='
    >>> text2symbol("<", "L")
    'L'
    >>> text2symbol("gte", ">=")
    '>='
    >>> text2symbol(">", ">")
    '>'
    >>> text2symbol("1", ">")
    32202
    """
    expected_answer_type = None
    for answer_type in symbol_answer_types:
        if expected_answer.lower() in symbol_answer_types[answer_type]:
            expected_answer_type = answer_type

    if expected_answer_type:
        message_formatted = (
            text.lower()
            .translate(str.maketrans("", "", '!"#$%&\()*+,-./:;?@[\\]^_`{|}~'))
            .split()
        )

        # Convert student answer to valid format
        for answer_type in symbol_answer_types:
            # Returns the expected_answer if student gave correct answer
            matched_word = [
                expected_answer
                for word in message_formatted
                if word in symbol_answer_types[expected_answer_type]
            ]
            if matched_word:
                return matched_word[0]

            # Returns the properly formatted answer if student gave an appropriate option, but wrong answer
            matched_word = [
                answer_type
                for word in message_formatted
                if word in symbol_answer_types[answer_type]
            ]
            if matched_word:
                return matched_word[0]
    return TOKENS2INT_ERROR_INT


text_answer_types = {
    "Yes": ["y", "yes", "yah", "yeah", "ok", "okay", "yea"],
    "No": ["n", "no", "nah"],
    "T": ["t", "true", "y", "yes", "yah", "yeah", "ok", "okay", "yea"],
    "F": ["f", "false", "n", "no", "nah"],
    "A": ["a"],
    "B": ["b"],
    "C": ["c"],
    "D": ["d"],
    "Even": ["even"],
    "Odd": ["odd"],
    "Monday": ["mon", "monday"],
    "Tuesday": ["tues", "tuesday"],
    "Wednesday": ["wed", "wednesday"],
    "Thursday": ["thurs", "thursday"],
    "Friday": ["fri", "friday"],
    "Saturday": ["sat", "saturday"],
    "Sunday": ["sun", "sunday"],
}

expected_answer_type_groups = {
    "yes-no": ["Yes", "No"],
    "true-false": ["T", "F"],
    "multiple-choice": ["A", "B", "C", "D"],
    "even-odd": ["Even", "Odd"],
    "day-of-the-week": [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ],
}


def text2text(text, expected_answer):
    """Converts a valid text answer to the expected answer's format or returns error code
    >>> text2text("odd", "Odd")
    'Odd'
    >>> text2text("Even", "Even")
    'Even'
    >>> text2text("Y", "Yes")
    'Yes'
    >>> text2text("a", "A")
    'A'
    >>> text2text("Yes", "Yes")
    'Yes'
    >>> text2text("true", "T")
    'T'
    >>> text2text("True", "T")
    'T'
    >>> text2text("1", None)
    32202
    >>> text2text("I have no idea", "F")
    'F'
    >>> text2text("no", "1")
    32202
    """

    # Determine the expected answer type
    expected_answer_group = None
    for group in expected_answer_type_groups:
        if expected_answer in expected_answer_type_groups[group]:
            expected_answer_group = group

    if not expected_answer_group:
        return TOKENS2INT_ERROR_INT

    # Check that the expected answer is one of the types
    expected_answer_type = None
    answer_type_group = None
    for answer_type in expected_answer_type_groups[expected_answer_group]:
        for answer_option in text_answer_types[answer_type]:
            if expected_answer.lower() in text_answer_types[answer_type]:
                expected_answer_type = answer_type

    if not expected_answer_type:
        return TOKENS2INT_ERROR_INT

    message_formatted = (
        text.lower()
        .translate(str.maketrans("", "", '!"#$%&\()*+,-./:;?@[\\]^_`{|}~'))
        .split()
    )

    # Handle if the student entered a right answer that's the right type
    for answer_option in text_answer_types[expected_answer_type]:
        matched_word = [
            expected_answer for word in message_formatted if word == answer_option
        ]
        if matched_word:
            return matched_word[0]

    # Handle if the student entered a wrong answer that's one of the right types
    for answer_option in expected_answer_type_groups[expected_answer_group]:
        for answer in text_answer_types[answer_option]:
            matched_word = [
                answer_option for word in message_formatted if word == answer
            ]

            if matched_word:
                return matched_word[0]

    return TOKENS2INT_ERROR_INT


def text2exponent(text, expected_answer=None):
    """Returns a properly formatted exponent answer or the error code

    >>> text2exponent("7^2", "7^2")
    '7^2'
    >>> text2exponent("14 ^2", "14^2")
    '14^2'
    >>> text2exponent("2.5 ^ 80", "2.5^80")
    '2.5^80'
    >>> text2exponent("I don't know", "2.5^80")
    32202
    >>> text2exponent("It might be 2 ^ 8", "2^8")
    '2^8'
    >>> text2exponent("3^4", "5^6")
    '3^4'
    """
    superscript_list = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]

    text = re.sub(r"(to\s*the)", "^", text)

    base = ""
    exponent = ""
    for char in text:
        if char in superscript_list:
            exponent += unidecode(char)
        else:
            base += char

    if exponent:
        text = base + "^" + exponent

    match = re.search(r"[-]?\d+(\.\d+)?\s*\^\s*[-]?\d+(\.\d+)?", text)
    try:
        matched_text = match.group(0)
    except AttributeError:
        return TOKENS2INT_ERROR_INT

    answer = matched_text.replace(" ", "")

    return answer


def text2fraction(text, expected_answer=None):
    """Returns a properly formatted fraction answer or the error code

    >>> text2fraction("65/6", "65/6")
    '65/6'
    >>> text2fraction("1/3", "1/3")
    '1/3'
    >>> text2fraction("8 / 10", "8/10")
    '8/10'
    >>> text2fraction("55 1 /28", "55 1/28")
    '55 1/28'
    >>> text2fraction("14  1/2", "14 1/2")
    '14 1/2'
    >>> text2fraction("25 12/3 maybe?", "25 12/3")
    '25 12/3'
    """
    text = re.sub(r"(over|oer|ovr)", "/", text)

    match = re.search(r"(\d+\s+)?\d+\s*/\s*\d+", text)

    if match:
        normalize_fraction = (
            match[0].replace(" /", "/").replace("/ ", "/").replace("  ", " ")
        )
        return normalize_fraction

    return TOKENS2INT_ERROR_INT


def text2equation(text, expected_answer=None):
    """Returns a properly formatted multiplication equation or the error code

    >>> text2equation("2 times 15", "2x15")
    '2x15'
    >>> text2equation("3 *9", "3x9")
    '3x9'
    >>> text2equation("4multiply10", "4x10")
    '4x10'
    """
    # Converts multiplication words to x
    text = re.sub(r"(times|multiplied\s*by|multiplied|multiply)|\*", "x", text)

    # Extracts multiplication equation from phrases
    match = re.search(r"[-]?\d+(\.\d+)?\s*x\s*[-]?\d+(\.\d+)?", text)
    try:
        normalized_equation = match[0].replace(" ", "")
        return normalized_equation
    except AttributeError:
        return TOKENS2INT_ERROR_INT
    except TypeError:
        return TOKENS2INT_ERROR_INT
    return TOKENS2INT_ERROR_INT
