# coding=utf-8
from time import time
from uuid import uuid4


def create_alphabet_from_ascii(ascii_start=33, ascii_end=126):
    # Ascii-Printable = 33-126
    toAscii = lambda x: str(chr(x))
    ascii_end = ascii_end + 1
    referenceAlphabet = list(map(toAscii, range(ascii_start, ascii_end)))
    return referenceAlphabet


def get_alphanum_alphabet():
    return create_alphabet_from_ascii(48, 57) + create_alphabet_from_ascii(65, 90) + create_alphabet_from_ascii(97, 122)


def hex_to_string(hex, reference_alphabet=create_alphabet_from_ascii()):
    decimal_value = int(hex, 16)
    string_representation = ''
    current = decimal_value
    while current:
        remainder = int(current) % len(reference_alphabet)
        remainder_string = reference_alphabet[int(remainder)]
        string_representation = remainder_string + string_representation
        current = int(current) / len(reference_alphabet)
    return string_representation


def gen_token(alphabet=get_alphanum_alphabet()):
    return "".join(map(lambda x: hex_to_string(x, alphabet), str(uuid4()).split("-")[1:-2]))


def unique_prefix(alphabet=get_alphanum_alphabet()):
    unixtimestamp = int(time())
    # noinspection PyPep8Naming
    randomUUID = uuid4()
    prefix = hex_to_string(hex(unixtimestamp), alphabet)
    for part in str(randomUUID).split("-"):
        prefix += "_"
        prefix += hex_to_string(part, alphabet)
    return prefix
