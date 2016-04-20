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

    def test_get_course(self):
        get_course_case = [
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
        for items, lessons_total, comb_size, output in get_course_case:
            tt = TimetableGenerator(items, comb_size, lessons_total)
            self.assertEqual(tt.get_course(tt.combs), output)

    def test_get_course_versions(self):
        get_course_versions_case = [
            ([1, 2], 2, 3, 1000),
        ]
        for items, comb_size, lessons_total, output in get_course_versions_case:
            tt = TimetableGenerator(items, comb_size, lessons_total)
            self.assertEqual(len(tt.get_course_versions([])), output)

    def test_get_courses_hist(self):
        get_courses_hist_case = [
            ([[], [], []], {0: [[], [], []]}),
            ([[1, 2], [1, 2], [1], [1, 2, 3]], {1: [[1]], 2: [[1, 2], [1, 2]], 3: [[1, 2, 3]]})
        ]
        for courses, hist in get_courses_hist_case:
            self.assertEqual(TimetableGenerator.get_courses_hist(courses), hist)

    def test_choose_version(self):
        choose_version_case = [
            ({}, 0, []),
            ({}, 1, []),
            ({}, 2, []),
            ({1: [[1]], 2: [[1, 2], [1, 2]], 3: [[1, 2, 3]]}, 0, []),
            ({1: [[1]], 2: [[1, 2], [1, 2]], 3: [[1, 2, 3]]}, 2, [1, 2]),
            ({1: [[1]], 2: [[1, 2], [1, 2]], 3: [[1, 2, 3]]}, 3, [1, 2, 3]),
            ({1: [[1]], 2: [[1, 2], [1, 2]], 3: [[1, 2, 3]]}, 4, [])
        ]
        for key, lesson_total, version in choose_version_case:
            self.assertEqual(TimetableGenerator.choose_version(key, lesson_total), version)


if __name__ == '__main__':
    unittest.main()
