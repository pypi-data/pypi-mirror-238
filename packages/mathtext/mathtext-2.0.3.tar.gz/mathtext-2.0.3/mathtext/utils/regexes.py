#!/usr/bin/env python
# mashup of nlpia2.text_processing.re_patterns and nlpia2.text_processing.constants
# -*- coding: utf-8 -*-
# ^-- This allows unicode copypasta below
import re
import string

RE_WORD_SIMPLE = RE_FINDALL_TOKENS = r"\w+(?:\'\w+)?|[^\w\s]"
CRE_WORD_SIMPLE = CRE_FINDALL_TOKENS = re.compile(RE_WORD_SIMPLE)


MAX_ORD = 127
MAX_CHR = MAX_CHAR = chr(MAX_ORD)
APOSTROPHE_CHARS = "'`’"
UNPRINTABLE = "".join(set(chr(i) for i in range(MAX_ORD + 1)) - set(string.printable))
string.unprintable = (
    UNPRINTABLE  # monkey patch so import string from this module if you want this!
)


###################################################
# nlpia2.text_processing.constants.py
#
# TODO: only need APOSTROPHE_CHARS
# from nlpia2.text_processing.constants import APOSTROPHE_CHARS

DASH_CHARS = "-‑—−–"
RE_DASH_CHAR = "[" + DASH_CHARS + "]"

APOSTROPHE_CHARS = "'’‘ʻ`′"
RE_APOSTROPHE_CHAR = "[" + APOSTROPHE_CHARS + "]"

# nlpia2.text_processing.constants.py
###################################################

#####################################################################################
#####################################################################################
# pugnlp.regexes

ASCII_CHARACTERS = "".join([chr(i) for i in range(128)])

# for Twitter tweets
########################################################################


#####################################################
# Sequence getters/iterators/wrappers


def iter_finds(regex_obj, s):
    """Generate all matches found within a string for a regex and yield each match as a string"""
    if isinstance(regex_obj, str):
        for m in re.finditer(regex_obj, s):
            yield m.group()
    else:
        for m in regex_obj.finditer(s):
            yield m.group()


def try_next(it, default=None):
    try:
        return next(it)
    except StopIteration:
        return default


def try_get(obj, idx, default=None):
    try:
        return obj.__getitem__(idx)
    except IndexError:
        return default


def wrap(s, prefix=r"\b", suffix=r"\b", grouper="()"):
    r"""Wrap a string (tyically a regex) with a prefix and suffix (usually a nonconuming word break)
    Arguments:
      prefix, suffix (str): strings to append to the front and back of the provided string
      grouper (2-len str or 2-tuple): characters or strings to separate prefix and suffix from the middle
    >>> wrap(r'\w*')
    '\\b(\\w*)\\b'
    >>> wrap(r'middle', prefix=None)
    '(middle)\\b'
    """
    wrapped = prefix or ""
    wrapped += try_get(grouper, 0, "")
    wrapped += s or ""
    wrapped += try_get(grouper, 1, try_get(grouper, 0, ""))
    return wrapped + (suffix or "")


# Sequence getters/iterators/wrapeers
######################################################

RE_BAD_FILENAME = "[{}]".format(re.escape(string.punctuation + string.unprintable))
RE_PUNCT = "[{}]".format(re.escape(string.punctuation))
RE_UPPER_CLASS = re.compile(r"[A-Z]")
RE_LOWER_CLASS = re.compile(r"[a-z]")
RE_DIGIT_CLASS = re.compile(r"[0-9]")
# \w = r'[a-zA-Z0-9_]'
RE_WORD_CLASS = r"[a-zA-Z0-9_]"

# numerals only allowed at the end of a word, but include it in the word
# hyphens and underscores only allowed at the end of letters before any numerals
# start with an optional dot, then have to have at least 1 letter
# optional numerals at the end of word segments, underscores and hyphens between word segments

# FIXME: seems broke
RE_WORD = r"^([a-zA-Z][-_a-zA-Z]*[\w0-9])[\W]*$"
CRE_WORD = re.compile(RE_WORD)
# RE_WORD_UNGROUPED = r'[a-zA-Z][-_a-zA-Z]*[\w0-9]'

RE_WORD_BASIC = r"[.]?[a-zA-Z]+[0-9]*"
RE_WORD_BASIC_B = wrap(RE_WORD_BASIC)
RE_WORD_LIBERAL = r"[-.a-zA-Z0-9_]+"
RE_WORD_LIBERAL_B = wrap(RE_WORD_LIBERAL)
RE_WORD_CAPITALIZED = r"[A-Z][a-z]+[0-9]{0,3}"
RE_WORD_CAPITALIZED_B = r"\b(" + RE_WORD_CAPITALIZED + ")\\b"
RE_WORD_ACRONYM = r"[A-Z0-9][A-Z0-9]{1,6}[0-9]{0,2}"
RE_WORD_ACRONYM_B = r"\b(" + RE_WORD_ACRONYM + ")\\b"
RE_WORD_LOWERCASE = r"[a-z]+[0-9]{0,3}"
RE_WORD_LOWERCASE_B = r"\b(" + RE_WORD_LOWERCASE + ")\\b"
RE_CAMEL_BASIC = "(" + RE_WORD_CAPITALIZED + "){2,6}"
RE_CAMEL_BASIC_B = r"\b(" + RE_CAMEL_BASIC + ")\\b"
RE_CAMEL_BASIC_LONG = "(" + RE_WORD_CAPITALIZED + "){7,256}"
RE_CAMEL_BASIC_LONG_B = r"\b(" + RE_CAMEL_BASIC + ")\\b"
RE_CAMEL_NORMAL = "(" + RE_CAMEL_BASIC + ")|([a-z]+(" + RE_WORD_CAPITALIZED + "){1,5})"
RE_CAMEL_NORMAL_B = r"\b(" + RE_CAMEL_NORMAL + ")\\b"
RE_CAMEL_LIBERAL = (
    r"\b("
    "(" + RE_CAMEL_NORMAL + ")|"
    "(" + RE_WORD_ACRONYM + "(" + RE_WORD_CAPITALIZED + "){1,5}" + ")|"
    "(" + "[a-z]{0,24}(" + RE_WORD_CAPITALIZED + "){1,5}" + RE_WORD_ACRONYM + ")"
    ")\\b"
)
RE_CAMEL_LIBERAL_B = r"\b(" + RE_CAMEL_LIBERAL + ")\\b"
CRE_CAMEL_LIBERAL_B = re.compile(RE_CAMEL_LIBERAL_B)
RE_CAMEL = RE_CAMEL_LIBERAL
RE_CAMEL_B = RE_CAMEL_LIBERAL_B

CHARS_DASHES = "–"
CHARS_ALGEBRA = "-+*/^!=().a-zA-Z0-9_'"
RE_WORD_ALGEBRA = "[" + CHARS_ALGEBRA + "]+"

QUOTE_CHARS = "\"'`’“”"
RE_WORD_BASIC_QUOTED = "|".join(c + RE_WORD_BASIC + c for c in QUOTE_CHARS)
RE_WORD_LIBERAL_QUOTED = "|".join(c + RE_WORD_LIBERAL + c for c in QUOTE_CHARS)
RE_WORD_ALGEBRA_QUOTED = "|".join(c + RE_WORD_ALGEBRA + c for c in QUOTE_CHARS)
RE_PHRASE_BASIC_QUOTED = "|".join(
    c + "((" + RE_WORD_BASIC + ")|\\W)+" + r"\W?" + c for c in QUOTE_CHARS
)
RE_PHRASE_LIBERAL_QUOTED = "|".join(
    c + "((" + RE_WORD_LIBERAL + ")|\\W)+" + c for c in QUOTE_CHARS
)
RE_PHRASE_ALGEBRA_QUOTED = "|".join(
    c + "((" + RE_WORD_ALGEBRA + ")|\\W)+" + c for c in QUOTE_CHARS
)

# 2 to 3 "words" joined by internal underscores is just an underscored word
RE_WORD_UNDERSCORED = "|".join("[_]+".join([RE_WORD_BASIC] * i) for i in range(2, 4))
# 4 to 64 "words" joined by internal underscores is a "PHRASE", like the title of a book or file
RE_PHRASE_UNDERSCORED = "|".join("[_]+".join([RE_WORD_BASIC] * i) for i in range(4, 65))
# 2 to 3 "words" joined by internal hyphens is just a hyphenated (compound) word
RE_WORD_HYPHENATED = "|".join("[_]+".join([RE_WORD_BASIC] * i) for i in range(2, 4))
# 4 to 64 "words" joined by internal hyphens is a "PHRASE"
RE_PHRASE_HYPHENATED = "|".join("[_]+".join([RE_WORD_BASIC] * i) for i in range(4, 65))

# based on pci/unused/chapter3/generatefeedvector.py
RE_HTML_TAG = r"[\s]*<[^>]+>[\s]*"
RE_DOUBLEQUOTE = r'["]+'
# \d = [0-9]  # also unicode numerals in all scripts (but only in unicode-supporting flavors unlike Java)
# \w = [a-zA-Z0-9_]

CHARS_LOWER = "".join(chr(i) for i in range(ord("a"), ord("z") + 1))
CHARS_UPPER = "".join(chr(i) for i in range(ord("A"), ord("Z") + 1))
CHARS_DIGIT = "".join(chr(i) for i in range(ord("0"), ord("9") + 1))
CHARS_ALPHA = CHARS_LOWER + CHARS_UPPER
CHARS_ALPHANUM = CHARS_ALPHA + CHARS_DIGIT
RE_CLASS_ALPHANUM = "[a-zA-Z0-9]"

# Dots and allowed to delimit words, none of the 3 apostrophes nor & symbol do
RE_WORD_DELIM = r"[^-&a-zA-Z0-9_" + APOSTROPHE_CHARS + r"]"
# FIXME: Only single-hyphenated words are accecpted, unaccptable-multi-hyphenated words
RE_HYPHENATED_ALPHA = r"\w+\-\w+"
RE_HYPHENATED_ALPHA_B = r"\b(" + RE_HYPHENATED_ALPHA + ")\\b"
RE_HYPHENATED_ALPHANUM = r"[a-zA-Z]\w*\-\w*[a-zA-Z][0-9]*"
RE_HYPHENATED_ALPHANUM_B = r"\b(" + RE_HYPHENATED_ALPHANUM + ")\\b"
RE_DOT_PREFIXED_ALPHANUM = "[.]" + RE_WORD_BASIC
RE_DOT_PREFIXED_ALPHANUM_B = r"\b(" + RE_DOT_PREFIXED_ALPHANUM + ")\\b"
RE_DOT_PREFIXED_HYPHENATED_ALPHANUM = "[.]" + RE_HYPHENATED_ALPHANUM
RE_DOT_PREFIXED_HYPHENATED_ALPHANUM_B = (
    r"\b(" + RE_DOT_PREFIXED_HYPHENATED_ALPHANUM + ")\\b"
)
# for .Net or .Netable
RE_HYPHENATED_DOTTED_ALPHANUM = r"[a-zA-Z]\w*[-.]\w*[a-zA-Z][0-9]*"
RE_HYPHENATED_DOTTED_ALPHANUM_B = r"\b(" + RE_HYPHENATED_DOTTED_ALPHANUM + ")\\b"

# FIXME: Plural words at end single quotes around plural words to be interpretted as possessive
RE_POSESSIVE_ALPHA = r"\w+'[sS]|\w+\-\w+[sS]'|\w+\-\w+"
RE_POSESSIVE_ALPHA_B = r"\b(" + RE_POSESSIVE_ALPHA + ")\\b"
RE_HYPHENATED_POSESSIVE_ALPHA = r"\w+\-\w+'[sS]|\w+\-\w+[sS]'|\w+\-\w+"
RE_HYPHENATED_POSESSIVE_ALPHA_B = r"\b(" + RE_HYPHENATED_POSESSIVE_ALPHA + ")\\b"

# This will accept a lot of mispelled or nonsense "contractions" and mis some odd, but valid ones listed here:
#    https://en.wikipedia.org/wiki/Wikipedia:List_of_English_contractions
RE_UNHYPHENATED_CONTRACTED_ALPHA = r"['`’]tis|['`’]twas|\w+['`’][a-zA-Z]{1,2}|\w+"
RE_UNHYPHENATED_CONTRACTED_ALPHA_B = r"\b(" + RE_UNHYPHENATED_CONTRACTED_ALPHA + ")\\b"
RE_USD_DECIMAL_BMK = r"\$\d+[.]\d+[BMKk]"
RE_USD_DECIMAL_BMK_B = r"\b(" + RE_USD_DECIMAL_BMK + ")\\b"
RE_USD_BMK = r"\$[\d]+[BMKk]"
RE_USD_BMK_B = r"\b(" + RE_USD_BMK + ")\\b"
RE_USD_CENTS = r"\$\d+[.]\d\d"  # don't allow decidollars or millidollars?
RE_USD_CENTS_B = r"\b(" + RE_USD_CENTS + ")\\b"
RE_USD = r"\$[\d]+"
RE_USD_B = r"\b(" + RE_USD + ")\\b"
# TODO: add EU and Asian Currencies and decimal formats (swap comma and decimal)
RE_FLOAT = r"[\d]+[.]?\d*"
RE_FLOAT_B = r"\b(" + RE_FLOAT + ")\\b"
RE_FLOAT_E = r"[\d]+[.]?\d*[ ]?[eE][ ]?\d+"
RE_FLOAT_E_B = r"\b(" + RE_FLOAT_E + ")\\b"
RE_NONSPACE = r"\S+"
RE_NONSPACE_B = r"\b(" + RE_NONSPACE + ")\\b"
RE_NONWORD = r"[^\s\w]+"
RE_NONWORD_B = r"\b(" + RE_NONWORD + ")\\b"
RE_YEAR = r"\b19\d\d\b|\b20\d\d\b|\b[']?\d\d\b"
RE_YEAR_B = r"\b(" + RE_YEAR + ")\\b"
RE_DECADE = r"\b19\d0[']?s\b|\b20\d0[']?s\b|\b[']?\d0[']?s\b"
RE_DECADE_B = r"\b(" + RE_DECADE + ")\\b"

RE_ACRONYM = r"[A-Z0-9][A-Z0-9]{1,5}[0-9]{0,2}"
RE_ACRONYM_B = r"\b(" + RE_ACRONYM + ")\\b"
# only very narrow, but common examples fit: U.S., U.S.A., A., and B.
RE_DOTTED_ACRONYM_B = r"\b[A-Z][.][A-Z][.][A-Z][.][A-Z][.]\b|\b[A-Z][.][A-Z][.][A-Z][.]\b|\b[A-Z][.][A-Z][.]\b|\b[A-Z][.]\b"
# RE_DOT_NET = r"\b[.]\w[.][A-Z][.][A-Z][.]\b|\b[A-Z][.][A-Z][.][A-Z][.]\b|\b[A-Z][.][A-Z][.]\b|\b[A-Z][.]\b"

# # Wrap token RE w/ parens (in case it contains ORs) and add nonconsuming word break (\b) at the end
# for name in ('WORD_CAPITALIZED', 'WORD_LOWERCASE', 'ACRONYM', 'USD_BMK', 'USD_CENTS', 'USD_DECIMAL_BMK',
#              'POSESSIVE_ALPHA', 'HYPHENATED_POSESSIVE_ALPHA'
#              'FLOAT_E', 'FLOAT_E', 'NONSPACE'):
#     name = 'RE_' + name
#     # this will hose up flake8
#     locals()[name + '_B'] = r'(' + locals()[name] + ')\\b'

# RE_CAMEL_CASE = ('(((' + RE_WORD_CAPITALIZED_B + ')|(' + RE_WORD_LOWERCASE + '))' + '(' + RE_ACRONYM + '))|' +
#                  '((' + RE_ACRONYM + '|' + RE_WORD_CAPITALIZED + '|' + RE_WORD_LOWERCASE + ')(' +
#                  RE_WORD_CAPITALIZED + ')+)' + r'\b')
# RE_CAMEL_CASE = CRE_CAMEL_CASE = re.compile(RE_CAMEL_CASE)

# always list RE's from most greedy to least greedy []+, []*, []?, then [], supersets before subsets in char groups []
RE_TOKEN = r"|".join(
    [
        "[.]" + RE_HYPHENATED_ALPHANUM,
        RE_HYPHENATED_ALPHA,
        RE_HYPHENATED_ALPHANUM,
        RE_UNHYPHENATED_CONTRACTED_ALPHA_B,
        RE_USD_DECIMAL_BMK,
        RE_USD_BMK_B,
        RE_USD_CENTS,
        RE_USD,
        RE_DECADE,
        RE_YEAR,
        RE_ACRONYM,
        RE_FLOAT_E,
        RE_FLOAT,
        RE_NONWORD,
    ]
)
CRE_TOKEN = CRE_TOKEN_GROUPS = re.compile(RE_TOKEN)
