# tokenizers.py
from mathtext.utils.regexes import CRE_TOKEN_GROUPS, CRE_FINDALL_TOKENS


def tokenize_contractions(text, cre_token_groups=CRE_TOKEN_GROUPS):
    """Keep appostrophized suffixes (possessives/contractions) with root

    >>> tokenize_contractions("hundred's place")
    ["hundred's", 'place']
    >>> tokenize_contractions("tens' place")
    ['tens', "'", 'place']

    """
    return list(m.group() for m in cre_token_groups.finditer(text))


def tokenize_words(text, cre_findall_tokens=CRE_FINDALL_TOKENS):
    """Use regex tokenizer from chapter 2 of NLPiA 2nd Ed

    >>> tokenize_words("hundred's place")
    ["hundred's", 'place']
    >>> tokenize_words("tens' place")
    ['tens', "'", 'place']
    >>> tokenize_words("5 million, and 3 hundred forty-two.")
    ['5', 'million', ',', 'and', '3', 'hundred', 'forty', '-', 'two', '.']
    """
    return cre_findall_tokens.findall(text)
