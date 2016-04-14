import unittest
from files_interaction import *


text1 = """
names: 1, 2, 3, 4, 5
whitelist: (1, 2), (3, 4), (4, 5)
blacklist: (1, 5), (3, 5)
"""

text2 = """
names: 1, 2,
3, 4, 5
whitelist: (1, 2), (3, 4),
           (4, 5)
blacklist: (1, 5), (3, 5)
"""

text3 = """
names: 1 2 3 4 5
whitelist: (1 2) (3 4) (4 5)
blacklist: (1 5) (3 5)
"""


class TestStringMethods(unittest.TestCase):
    def test_correct_text(self):
        correct_case = [
            (text1, 'names: 1, 2, 3, 4, 5 whitelist: (1, 2), (3, 4), (4, 5) blacklist: (1, 5), (3, 5)'),
            (text2, 'names: 1, 2, 3, 4, 5 whitelist: (1, 2), (3, 4), (4, 5) blacklist: (1, 5), (3, 5)'),
            (text3, 'names: 1 2 3 4 5 whitelist: (1 2) (3 4) (4 5) blacklist: (1 5) (3 5)'),
        ]
        for input, output in correct_case:
            self.assertEqual(correct_text(input), output)

    def test_get_names(self):
        names_case = [
            (text1, '1, 2, 3, 4, 5'),
            (text2, '1, 2, 3, 4, 5'),
            (text3, '1 2 3 4 5')
        ]
        for input, output in names_case:
            self.assertEqual(get_names(correct_text(input)), output)

    def test_get_whitelist(self):
        whitelist_case = [
            (text1, '(1, 2), (3, 4), (4, 5)'),
            (text2, '(1, 2), (3, 4), (4, 5)'),
            (text3, '(1 2) (3 4) (4 5)')
        ]
        for input, output in whitelist_case:
            self.assertEqual(get_whitelist(correct_text(input)), output)

    def test_get_blacklist(self):
        blacklist_case = [
            (text1, '(1, 5), (3, 5)'),
            (text2, '(1, 5), (3, 5)'),
            (text3, '(1 5) (3 5)'),
        ]
        for input, output in blacklist_case:
            self.assertEqual(get_blacklist(correct_text(input)), output)

    def test_split(self):
        split_case = [
            ('', []),
            ('1, 2, 3, 4', ['1', '2', '3', '4']),
            ('1 2 3 4', ['1', '2', '3', '4']),
            ('1; 2; 3; 4', ['1', '2', '3', '4']),
            ('1 2, 3;         4', ['1', '2', '3', '4']),
            ('misha, kate, ruslan, vika', ['misha', 'kate', 'ruslan', 'vika']),
            ('misha_1, kate-38, ruslan, vika', ['misha_1', 'kate-38', 'ruslan', 'vika']),
        ]
        for input, output in split_case:
            self.assertEqual(split_names(input), output)

if __name__ == '__main__':
    unittest.main()
