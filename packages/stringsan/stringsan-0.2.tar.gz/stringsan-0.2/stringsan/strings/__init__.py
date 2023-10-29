import re 
import random 

from itertools import groupby

def occurrences(string: str, pattern) -> int:
    """
    Find all the occurrences of the given pattern in the string

    :param: `pattern` can be a string or a regular expression
    """
    _occurrences = re.findall(pattern, string)
    return len(_occurrences)

def first_occurrence(string: str) -> any:
    """
    Fetch the first occurrence from the given string.
    """
    _match = re.search(r"\w+", string)
    return _match.group() if _match else None


def last_occurrence(string: str) -> any:
    """
    Fetch the last occurrence from the given string.
    """
    _match = re.findall(r"\b\w+\b", string)
    return _match[-1] if _match else None

def random_occurrence(string: str) -> str:
    """
    Fetch a random occurrence from the given string.

    * BLANK SPACES are used as separators.
    """
    return random.choice(string.split(" ")) 

def is_zalgo(string: str) -> bool:
    """
    Check whether the string contains zalgo characters
    """
    chars = [chr(i) for i in range(768, 879)]
    return any(char in chars for char in string)

def compress_string(string: str) -> str:
    """
    Compress a string by representing repeated characters with a numerical value.
    """
    compressed = ''.join(char + str(len(list(group))) for char, group in groupby(string))
    return compressed if len(compressed) < len(string) else string
