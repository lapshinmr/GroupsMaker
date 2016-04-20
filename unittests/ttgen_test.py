import unittest
from ttgen import *


class TestTimetableGenerator(unittest.TestCase):
    def test_init_tt(self):
        init_error_case = [
            ([], 2),
            ([], 3),
            ([1, 2], 3),
        ]
        for items, comb_size in init_error_case:
            with self.assertRaises(NotEnoughStudents):
                TimetableGenerator(items, comb_size)

    def test_get_lesson(self):
        lesson_case = [
            ([1, 2, 3], [(1, 2), (2, 3), (1, 3)], 2, ([(1, 2, 3)], [(2, 3), (1, 3)])),
            ([1, 2, 3], [(1, 3), (2, 3), (1, 2)], 2, ([(1, 3, 2)], [(2, 3), (1, 2)])),
            ([1, 2, 3, 4], [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)], 2, ([(1, 2), (3, 4)], [(1, 3), (1, 4), (2, 3), (2, 4)])),
            ([1, 2, 3, 4], [(1, 4), (2, 3), (2, 4), (3, 4)], 2, ([(1, 4), (2, 3)], [(2, 4), (3, 4)])),
            ([1, 2, 3, 4], [(2, 3), (1, 4), (2, 4), (3, 4)], 2, ([(2, 3), (1, 4)], [(2, 4), (3, 4)])),
            ([1, 2, 3, 4], [(2, 3), (1, 4), (2, 4), (3, 4)], 2, ([(2, 3), (1, 4)], [(2, 4), (3, 4)])),
        ]
        for items, uniq_combs, comb_size, output in lesson_case:
            self.assertEqual(TimetableGenerator(items, comb_size).get_lesson(uniq_combs), output)

        lesson_error_case = [
            ([1, 2, 3, 4], [(2, 3), (2, 4), (3, 4)], 2),
            ([1, 2, 3, 4], [(3, 4), (2, 3), (1, 4), (2, 4)], 2)
        ]
        for items, uniq_combs, comb_size in lesson_error_case:
            with self.assertRaises(IndexError):
                TimetableGenerator(items, comb_size).get_lesson(uniq_combs)

    def test_get_lessons(self):
        get_lessons_case = [
            ([1, 2], 1, 1, [[(1, ), (2, )]]),
            ([1, 2], 1, 2, [[(1, 2)]]),
            ([1, 2, 3], 1, 2, [[(1, 2, 3)]]),
            ([1, 2, 3], 2, 2, [[(1, 2, 3)], [(1, 3, 2)]]),
            ([1, 2, 3], 3, 2, [[(1, 2, 3)], [(1, 3, 2)], [(2, 3, 1)]]),
            ([1, 2, 3, 4], 1, 2, [[(1, 2), (3, 4)]]),
            ([1, 2, 3, 4], 2, 2, [[(1, 2), (3, 4)], [(1, 3), (2, 4)]]),
            ([1, 2, 3, 4], 3, 2, [[(1, 2), (3, 4)], [(1, 3), (2, 4)], [(1, 4), (2, 3)]]),
            ([1, 2, 3], 1, 3, [[(1, 2, 3)]]),
            ([1, 2, 3, 4], 1, 3, [[(1, 2, 3, 4)]]),
            ([1, 2, 3, 4], 2, 3, [[(1, 2, 3, 4)], [(1, 2, 4, 3)]]),
            ([1, 2], 2, 2, [[(1, 2)]]),
            ([1, 2, 3], 2, 3, [[(1, 2, 3)]]),
            ([1, 2, 3], 3, 3, [[(1, 2, 3)]]),
        ]
        for items, lessons_total, comb_size, output in get_lessons_case:
            tt = TimetableGenerator(items, comb_size, lessons_total)
            self.assertEqual(tt.get_lessons(tt.combs), output)

    def test_get_les_versions(self):
        get_les_verdioins_case = [
            ([1, 2], 2, 3, 1000),
        ]
        for items, comb_size, lessons_total, output in get_les_verdioins_case:
            tt = TimetableGenerator(items, comb_size, lessons_total)
            self.assertEqual(len(tt.get_les_versions([])), output)

    def test_version_length_counter(self):
        version_length_counter_case = [
            ([[], [], []], {0: [[], [], []]}),
            ([[1, 2], [1, 2], [1], [1, 2, 3]], {1: [[1]], 2: [[1, 2], [1, 2]], 3: [[1, 2, 3]]})
        ]
        for versions, count in version_length_counter_case:
            tt = TimetableGenerator([1, 2, 3])
            self.assertEqual(tt.version_length_counter(versions), count)


if __name__ == '__main__':
    unittest.main()
