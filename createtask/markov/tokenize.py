import re
from typing import List


class Tokenizer:
    """
    English tokenizer adapted from NLTK implementation of Penn Treebank, except
    standard contractions are not split.
    """

    STARTING_QUOTES = [
        (re.compile(r"^\""), r"``"),
        (re.compile(r"(``)"), r" \1 "),
        (re.compile(r"([ \(\[{<])(\"|\'{2})"), r"\1 `` "),
    ]

    PUNCTUATION = [
        (re.compile(r"([:,])([^\d])"), r" \1 \2"),
        (re.compile(r"([:,])$"), r" \1 "),
        (re.compile(r"\.\.\."), r" ... "),
        (re.compile(r"[;@#$%&]"), r" \g<0> "),
        (
            re.compile(r'([^\.])(\.)([\]\)}>"\']*)\s*$'),
            r"\1 \2\3 ",
        ),  # Handles the final period.
        (re.compile(r"[?!]"), r" \g<0> "),
        (re.compile(r"([^'])' "), r"\1 ' "),
    ]

    PARENS_BRACKETS = (re.compile(r"[\]\[\(\)\{\}\<\>]"), r" \g<0> ")

    DOUBLE_DASHES = (re.compile(r"--"), r" -- ")

    ENDING_QUOTES = [
        (re.compile(r'"'), " '' "),
        (re.compile(r"(\S)(\'\')"), r"\1 \2 "),
    ]

    def tokenize(self, text: str) -> List[str]:
        for regexp, substitution in self.STARTING_QUOTES:
            text = regexp.sub(substitution, text)

        for regexp, substitution in self.PUNCTUATION:
            text = regexp.sub(substitution, text)

        regexp, substitution = self.PARENS_BRACKETS
        text = regexp.sub(substitution, text)

        regexp, substitution = self.DOUBLE_DASHES
        text = regexp.sub(substitution, text)

        text = " " + text + " "

        for regexp, substitution in self.ENDING_QUOTES:
            text = regexp.sub(substitution, text)

        return text.split(' ')
