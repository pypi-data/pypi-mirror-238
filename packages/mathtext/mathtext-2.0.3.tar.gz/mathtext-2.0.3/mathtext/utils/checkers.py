import re

from mathtext.utils.default_values import OLD_BUTTONS_LOOKUP, PROFANITY_LOOKUP


def is_float(x):
    """Return False if the value is not a valid float and cannot be coerced into a float

    >>> is_float('0.4')
    True
    >>> is_float('1')
    True
    >>> is_float('Not sure')
    False
    >>> is_float("Don't know if it's 0.5 or 1")
    False
    """
    try:
        float(x)
        return True
    except ValueError:
        return False


def is_time(text):
    match = re.search(r"\b(\d{1,2}):(\d{2})\b", text)
    if match:
        # Check that the matched hour and minute values are valid
        hour = int(match.group(1))
        minute = int(match.group(2))
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return True
    return False


def has_unicode_characters(text):
    unicode_characters = re.compile(r"[\u0080-\uFFFF]")
    if unicode_characters.search(text):
        return True
    return False


def is_old_button(message):
    """Detects if a message exactly matches button text from outside the math Q and A turn

    >>> is_old_button("Yes 🥱")
    True
    >>> is_old_button("yes 🥱")
    False
    >>> is_old_button("The answer is Yes 🥱")
    False
    >>> is_old_button("Yes")
    False
    """
    return message in OLD_BUTTONS_LOOKUP


def has_profanity(message):
    """Detects whether a word in message has a profanity keyword

    >>> has_profanity("Fuck we'll chat later")
    True
    >>> has_profanity("you f u c k")
    True
    >>> has_profanity("I love you")
    False
    >>> has_profanity("Maybe 62")
    False
    """
    pattern = (
        r"\b(?:" + "|".join([re.escape(word) for word in PROFANITY_LOOKUP]) + r")\b"
    )
    matches = re.findall(pattern, message, flags=re.IGNORECASE)
    return bool(matches)


def has_multiple_valid_answers(extracted_approved_responses):
    """Checks if a student message has more than one valid answer

    >>> has_multiple_valid_answers([('answer', 't'), ('answer', 'f')])
    True
    >>> has_multiple_valid_answers([('answer', 'a'), ('answer', 'b'), ('answer', 'c'), ('answer', 'd')])
    True
    >>> has_multiple_valid_answers([('expected_answer', '5')])
    False
    >>> has_multiple_valid_answers([('answer', 'a'), ('expected_answer', '5')])
    True
    """
    extracted_answers_list = []
    for answer_type in extracted_approved_responses:
        if answer_type[0] == "answer" or answer_type[0] == "expected_answer":
            extracted_answers_list.append(answer_type)
    if len(extracted_answers_list) > 1:
        return True
    return False


def is_number(normalized_student_message):
    """Checks whether a student message can be converted to an integer or float
    >>> is_number("maybe 5000")
    False
    >>> is_number("2")
    True
    >>> is_number("2.75")
    True
    >>> is_number("-3")
    True
    """
    try:
        if float(normalized_student_message):
            return True
    except ValueError:
        pass
    try:
        if int(normalized_student_message):
            return True
    except ValueError:
        pass
    return False


def has_multiple_numbers(tokenized_student_message):
    """Checks whether a student message has multiple numbers"""
    nums = 0
    for tok in tokenized_student_message:
        if is_number(tok):
            nums += 1
    if nums > 1:
        return True
    return False
