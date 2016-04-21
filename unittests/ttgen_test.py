import unittest
from ttgen import *


class TestTimetableGenerator(unittest.TestCase):
    def test_init_tt(self):
        init_wo_black_case = [
            ([1, 2, 3, 4], 2, [(1, 2), (1, 3)], [(1, 4), (2, 3), (2, 4), (3, 4)]),
        ]
        for items, comb_size, black, wo_black in init_wo_black_case:
            tt = TimetableGenerator(items, comb_size, blacklist=black)
            self.assertEqual(tt.combs_wo_black, wo_black)

        init_wo_black_white_case = [
            ([1, 2, 3, 4], 2, [(2, 3)], [(1, 2), (1, 3)], [(1, 4), (2, 4), (3, 4)]),
        ]
        for items, comb_size, white, black, wo_black_white in init_wo_black_white_case:
            tt = TimetableGenerator(items, comb_size, whitelist=white, blacklist=black)
            self.assertEqual(tt.combs_wo_black_white, wo_black_white)

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
            ([1, 2, 3, 4], [(2, 3), (1, 4), (2, 4), (3, 4)], 2, ([(1, 4), (2, 3)], [(2, 4), (3, 4)])),
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
            ([1, 2], 10, 2, [[(1, 2)]]),
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

        get_course_not_sorted_case = [
            ([1, 2, 3, 4], 3, 2, [[(1, 4), (2, 3)], [(1, 2), (3, 4)], [(1, 3), (2, 4)]]),
        ]
        for items, lessons_total, comb_size, output in get_course_not_sorted_case:
            tt = TimetableGenerator(items, comb_size, lessons_total)
            self.assertNotEqual(tt.get_course(tt.combs), output)

    def test_get_course_versions(self):
        get_course_versions_case = [
            ([1, 2], 2, 3, 1000),
        ]
        for items, comb_size, lessons_total, output in get_course_versions_case:
            tt = TimetableGenerator(items, comb_size, lessons_total)
            self.assertEqual(len(tt.get_course_versions([])), output)

    def test_choose_version(self):
        choose_courses_case = [
            ({}, 0, []),
            ({}, 1, []),
            ({}, 2, []),
            ({1: [[1]], 2: [[1, 2], [1, 2]], 3: [[1, 2, 3]]}, 0, []),
            ({1: [[1]], 2: [[1, 2], [1, 2]], 3: [[1, 2, 3]]}, 2, [1, 2]),
            ({1: [[1]], 2: [[1, 2], [1, 2]], 3: [[1, 2, 3]]}, 3, [1, 2, 3]),
            ({1: [[1]], 2: [[1, 2], [1, 2]], 3: [[1, 2, 3]]}, 4, [1, 2, 3])
        ]
        count = 0
        for key, lesson_total, version in choose_courses_case:
            count += 1
            tt = TimetableGenerator([1, 2, 3, 4])
            self.assertEqual(tt.choose_course(key, lesson_total), version, 'CASE %s' % count)

    def test_generate(self):
        generate_case = [
            ([1, 2, 3, 4], 2, 3, [[(1, 2), (3, 4)], [(1, 3), (2, 4)], [(1, 4), (2, 3)]]),
        ]
        count = 0
        for items, size, duration, course in generate_case:
            count += 1
            tt = TimetableGenerator(items, size, duration)
            self.assertEqual(tt.generate(), course, 'CASE %s' % count)


if __name__ == '__main__':
    unittest.main()
