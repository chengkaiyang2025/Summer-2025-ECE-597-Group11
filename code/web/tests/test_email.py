import unittest

import emoji
import unicodedata

from services.email_process import HuggingFaceModelProcess_1
from tests.test_case import *

COMMON_PUNCTUATION = set([
    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
    ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'
])


def detect_suspicious_non_latin(text):
    suspicious_chars = []

    for char in text:
        if char.isascii():
            if char in COMMON_PUNCTUATION or char.isalnum() or char.isspace():
                continue  # 合理ASCII内容：字母、数字、空格、常见标点
            else:
                suspicious_chars.append((char, 'Unusual ASCII'))
                continue

        try:
            name = unicodedata.name(char)
            if 'LATIN' not in name:
                suspicious_chars.append((char, name))
        except ValueError:
            suspicious_chars.append((char, 'No Unicode Name'))
    return len(suspicious_chars)
class MyTestCase(unittest.TestCase):

    from services.email_process import DumbEmailProcessTemplate
    dumb = DumbEmailProcessTemplate()

    def test_dumb_process(self):
        # print(self.dumb.process("Hello World", "Hello World"))
        print(self.dumb.process(message1, "Hello World"))
        print(self.dumb.process(message2, "Hello World"))
    def test_character(self):
        # detect_suspicious_non_latin(self.message1)
        # detect_suspicious_non_latin(self.message2)
        # detect_suspicious_non_latin(self.message3)
        # detect_suspicious_non_latin(self.message4)
        print(detect_suspicious_non_latin(message5))

    def test_emoji(self):
        print(emoji.emoji_count(messsage_emoji_1))


if __name__ == '__main__':
    unittest.main()
