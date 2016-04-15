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

text4 = """
names: 1 2 3 4 5
"""

text5 = """
names: 1 2 3 4 5
blacklist: (1 5) (3 5)
"""

text6 = """
names: 1 2 3 4 5
whitelist: (1 2) (3 4) (4 5)
"""

text7 = ''

text8 = """
naems: 1 2 3 4 5
whietlist: (1 2) (3 4) (4 5)
blakclist: (1 5) (3 5)
"""

text9 = """
names: 1 2 3 4 5
(1 2) (3 4) (4 5)
blakclist: (1 5) (3 5)
"""

text10 = """
names: 1 2 3 4 5
blacklist: (1 5) (3 5)
whitelist: (1 2) (3 4) (4 5)
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
            (text3, '1 2 3 4 5'),
            (text4, '1 2 3 4 5'),
            (text7, ''),
            (text8, ''),
            (text9, '1 2 3 4 5'),
            (text10, '1 2 3 4 5'),
        ]
        for input, output in names_case:
            self.assertEqual(get_names(correct_text(input)), output)

    def test_get_exclist(self):
        exclist_case = [
            (text1, 'whitelist', [('1', '2'), ('3', '4'), ('4', '5')]),
            (text2, 'whitelist', [('1', '2'), ('3', '4'), ('4', '5')]),
            (text3, 'whitelist', [('1', '2'), ('3', '4'), ('4', '5')]),
            (text8, 'whitelist', []),
            (text4, 'whitelist', []),
            (text5, 'whitelist', []),
            (text7, 'whitelist', []),
            (text6, 'whitelist', [('1', '2'), ('3', '4'), ('4', '5')]),
            (text10, 'whitelist', [('1', '2'), ('3', '4'), ('4', '5')]),
            (text1, 'blacklist', [('1', '5'), ('3', '5')]),
            (text2, 'blacklist', [('1', '5'), ('3', '5')]),
            (text3, 'blacklist', [('1', '5'), ('3', '5')]),
            (text8, 'blacklist', []),
            (text4, 'blacklist', []),
            (text5, 'blacklist', [('1', '5'), ('3', '5')]),
            (text7, 'blacklist', []),
            (text10, 'blacklist', [('1', '5'), ('3', '5')]),
        ]
        for input, exclist, output in exclist_case:
            self.assertEqual(get_exclist(correct_text(input), exclist), output)

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

    def test_exclist_to_string(self):
        exclist_to_string_case = [
            ([], 2, 'whitelist', ''),
            ([('1', '2'), ('3', '4')], '2', 'whitelist', 'whitelist: (1, 2), (3, 4)'),
            ([('1', '2', '3'), ('2', '3', '4')], 3, 'whitelist', 'whitelist: (1, 2, 3), (2, 3, 4)'),
            ([('misha', 'sasha', 'dasha'), ('kate', 'ruslan', 'vika')], '3', 'whitelist',
             'whitelist: (misha, sasha, dasha), (kate, ruslan, vika)'),
        ]
        for input, size, exclist, output in exclist_to_string_case:
            self.assertEqual(output, exclist_to_string(input, size, exclist))

if __name__ == '__main__':
    unittest.main()
