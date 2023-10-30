from unidecode import unidecode
import re

from mathtext.constants import TOKENS2INT_ERROR_INT
from mathtext.utils.checkers import is_float
from mathtext.utils.regex_tokenizers import tokenize_words as tokenize


def unicode2str(text):
    """Convert unicode characters to regular string characters

    Does not convert superscript because that will happen in text2exponents if an exponent answer
    """
    superscript_list = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
    decoded_text = ""
    try:
        for char in text:
            if char in superscript_list:
                decoded_text += char
            else:
                decoded_text += unidecode(char)
    except TypeError:
        pass

    text = decoded_text
    return text


def text2float(text):
    """Convert text representation of a float into a float

    >>> text2float("1.23")
    1.23
    >>> text2float("1")
    1.0
    >>> text2float("I don't know")
    Traceback (most recent call last):
    ...
    ValueError: could not convert string to float: "Idon'tknow"
    >>> text2float("2..0")
    2.0
    >>> text2float("4 . 5")
    4.5
    """
    # if isinstance(text, str):
    text_spaces_stripped = text.replace(" ", "")
    processed_text = re.sub(r"\.+", ".", text_spaces_stripped)

    return float(processed_text)


def text2num(text):
    """is it an integer or float and return the appropriate type, or send 32202

    >>> text2num("0.2")
    0.2
    >>> text2num("1")
    1
    >>> text2num("Not sure")
    32202
    >>> text2num("¹6")
    32202
    """
    if text.isdigit():
        try:
            return int(text)
        except ValueError:
            pass

    if is_float(text):
        return text2float(text)

    return 32202


"""
From SO (StackOverflow): https://stackoverflow.com/a/493788/623735
"""

# TODO: Would it be better to use sets instead of tuples and lists? // list w/ in = o^n speed // o^1 with set
UNITS = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
)

DIGITS = range(1001)

# TODO: Why is "" written twice?
TENS = (
    "",
    "",
    "twenty",
    "thirty",
    "forty",
    "fifty",
    "sixty",
    "seventy",
    "eighty",
    "ninety",
)

SCALES = ["hundred", "thousand", "million", "billion", "trillion"]

NUM_WORDS = {}
NUM_WORDS["and"] = (1, 0)

TRANSLATION_DICT = {
    "fourty": "forty",
    "dirty": "thirty",
    "for": "four",
    "thre": "three",
    "threee": "three",
    "fity": "fifty",
}


def dict_get_noop(key=None, default_type=str, dictionary=None):
    if dictionary is None:
        dictionary = dict_get_noop.dictionary
    else:
        dict_get_noop.dictionary = dictionary
    return dictionary.get(key, default_type(key))


# TODO: dict comprehension and .update may be faster
for idx, word in enumerate(UNITS):
    NUM_WORDS[word] = (1, idx)
for idx, word in enumerate(DIGITS):
    NUM_WORDS[str(word)] = (1, idx)
for idx, word in enumerate(TENS):
    NUM_WORDS[word] = (1, idx * 10)
for idx, word in enumerate(SCALES):
    NUM_WORDS[word] = (10 ** (idx * 3 or 2), 0)


dict_get_noop.dictionary = None


def filter_translate_tokens(tokens, include=NUM_WORDS.keys(), exclude=",!?&%$#@:;/\\'"):
    dict_get_noop(dictionary=TRANSLATION_DICT)

    filtered_tokens = []
    for t in tokens:
        t = t.strip().lower()
        t = t.strip(",").strip().strip("-").strip().strip(".")
        t = t.lower().strip()

        try:
            t = TRANSLATION_DICT[t]
        except:
            pass

        if t and t in include and t not in exclude:
            filtered_tokens.append(t)

    return list(map(dict_get_noop, filtered_tokens))


def extract_decimal_number(tokens):
    """
    >>> extract_decimal_number(["I", "think", "it", "'s", "1", "2", ".", "5"])
    12.5
    >>> extract_decimal_number(["2", ".", "5"])
    2.5
    """
    decimal_number = ""
    is_decimal = False

    for token in tokens:
        if token.isdigit():
            decimal_number += token
        elif token == ".":
            if not is_decimal:
                decimal_number += "."
                is_decimal = True
        else:
            if is_decimal:
                break
    if is_decimal:
        try:
            return float(decimal_number)
        except:
            return None
    return None


def text2float(text):
    current = result = 0
    tokens = tokenize(text)

    is_decimal_result = extract_decimal_number(tokens)
    if is_decimal_result:
        return is_decimal_result


def has_punctuation_between_numbers(text):
    pattern = r"\d\s*[^\d\s]+\s*\d"
    return bool(re.search(pattern, text))


def text2int(text, numwords=NUM_WORDS, units=UNITS, tens=TENS, scales=SCALES):
    """Take expression containing a numberical expression and convert to a an integer

    >>> text2int('one two')
    3
    >>> text2int('thre and for')
    7
    >>> text2int('one twenty')
    21
    >>> text2int('one')
    1
    >>> text2int('notanumber')
    32202
    >>> text2int('not one')
    1
    >>> text2int('4 hundred')
    400
    >>> text2int('forty-two')
    42
    >>> text2int('123')
    123
    >>> text2int('fourteen')
    14
    >>> text2int('fifteen')
    15
    >>> text2int('one thousand four hundred ninety two')
    1492
    >>> text2int('ONE thousand forty-siX')
    1046
    >>> text2int('Seventeen Hundred')
    1700
    """
    if has_punctuation_between_numbers(text):
        return TOKENS2INT_ERROR_INT

    current = result = 0
    tokens = tokenize(text)

    filtered_tokens = filter_translate_tokens(tokens)

    # Handles numbers longer than 4 characters (ie., 1234)
    if not filtered_tokens:
        for tok in tokens:
            result = text2num(tok)
            if result != TOKENS2INT_ERROR_INT:
                return result

    # filtered_tokens = [t for t in filtered_tokens if t in numwords]
    # has_digits = bool(re.findall('[0-9]+'))
    # NOTE: For + in = n^2 - may need to work on this without in (set/dict)
    for word in filtered_tokens:
        if word not in numwords:
            # continue
            return TOKENS2INT_ERROR_INT

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current


def test():
    text2int(
        "seven billion one hundred million thirty one thousand three hundred thirty seven"
    )
