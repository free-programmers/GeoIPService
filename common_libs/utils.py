"""
* geoIPservice
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2024 - ali sharifi
* https://github.com/free-programmers/GeoIPService
"""


import base64
import hashlib
import random
import string

SysRandom = random.SystemRandom()

def generate_random_string(length: int = 6, punctuation: bool = True) -> str:
    """generate strong random strings

    :param length: length of random string - default is 6
    :type length: int

    :param punctuation: if this flag is set to `true`, punctuation will be added to random strings
    :type punctuation: bool

     :return: str: random string
    """
    letters = string.ascii_letters
    if punctuation:
        letters += string.punctuation
    random_string = SysRandom.choices(letters, k=length)

    return "".join(random_string)


class CryptoMethodUtils:
    """cryptography utils class"""

    def to_base64(self, data: str) -> str:
        """Converts a string to base64 encoding.

        Args:
          data: The string to be encoded.

        Returns:
          The base64 encoded string.
        """

        encoded_bytes = base64.b64encode(data.encode("utf-8"))
        return encoded_bytes.decode("utf-8")

    def to_sha256(self, data: str) -> str:
        """Converts a string to md5.

        Args:
          data: The string to be encoded.

        Returns:
          The md5 encoded string.
        """
        return hashlib.sha256(data.encode("utf-8")).hexdigest()