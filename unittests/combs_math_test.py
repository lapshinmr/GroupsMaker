import unittest
from combs_math import *


class TestStringMethods(unittest.TestCase):
    def test_pack(self):
        pack_case = [
            ([], 0, []),
            ([], 1, []),
            ([], 2, []),
            (['1', '2', '3', '4'], 1, [('1', ), ('2', ), ('3', ), ('4', )]),
            (['1', '2', '3', '4', '5', '6'], 2, [('1', '2'), ('3', '4'), ('5', '6')]),
            (['1', '2', '3', '4', '5', '6'], 3, [('1', '2', '3'), ('4', '5', '6')])
        ]
        for value, opt, res in pack_case:
            self.assertEqual(pack(value, opt), res)

    def test_unpack(self):
        unpack_case = [
            ([], []),
            ([('1', )], ['1']),
            ([('1', ), ('2', ), ('3', ), ('4', )], ['1', '2', '3', '4']),
            ([('1', '2'), ('3', '4'), ('5', '6')], ['1', '2', '3', '4', '5', '6']),
            ([('1', '2', '3'), ('4', '5', '6')], ['1', '2', '3', '4', '5', '6']),
            ([('1', '2'), ('3', ), ('4', '5', '6')], ['1', '2', '3', '4', '5', '6'])
        ]
        for value, res in unpack_case:
            self.assertEqual(unpack(value), res)

    def test_molder(self):
        molder_case = [
            ([], 1, []),
            ([('1', ), 0,  []]),
            ([('1', ), ('2', ), ('3', )], 1, [('1', ), ('2', ), ('3', )]),
            ([('1', ), ('2', '3')], 1, [('1', ), ('2', ), ('3', )]),
            ([('1', '2'), ('3', '4')], 2, [('1', '2'), ('3', '4')]),
            ([('1', '2'), ('3', ), ('4', )], 2, [('1', '2'), ('3', '4')]),
            ([('1', ), ('2', ), ('3', )], 2, [('1', '2'), ('3', )]),
            ([('1', '2', '3')], 2, [('1', '2'), ('3', )]),
            ([('1', '2'), ('3', ), ('4', )], 2, [('1', '2'), ('3', '4')])
        ]
        for value, opt, res in molder_case:
            self.assertEqual(molder(value, opt), res)

    def test_sort_comb(self):
        sort_comb_case = [
            ([], True, ()),
            ((), True, ()),
            ([], False, ()),
            (('1', '2'), True, ('1', '2')),
            (('2', '1'), True, ('1', '2')),
            (('2', '1', '1'), True, ('1', '1', '2')),
            (('2', '1', '1'), False, ('1', '2'))
        ]
        for value, dups_flag, res in sort_comb_case:
            self.assertEqual(sort_comb(value, dups_flag), res)

    def test_sort_combs_in_list(self):
        sort_combs_in_list_case = [
            ([], True, []),
            ([], False, []),
            ([('1', ), ('2', ), ('3', ), ('4', )], True, [('1', ), ('2', ), ('3', ), ('4', )]),
            ([('1', ), ('2', ), ('3', ), ('4', ), ('1', )], True, [('1', ), ('2', ), ('3', ), ('4', ), ('1', )]),
            ([('1', ), ('2', ), ('3', ), ('4', ), ('1', )], False, [('1', ), ('2', ), ('3', ), ('4', ), ('1', )]),
            ([('1', '2'), ('3', '4')], True, [('1', '2'), ('3', '4')]),
            ([('1', '2', '1'), ('3', '3', '4')], True, [('1', '1', '2'), ('3', '3', '4')]),
            ([('1', '2', '1'), ('3', '3', '4')], False, [('1', '2'), ('3', '4')]),
            ([('1', '2'), ('4', '3'), ('5', )], True, [('1', '2'), ('3', '4'), ('5', )]),
            ([('1', '2'), ('4', '3'), ('5', )], False, [('1', '2'), ('3', '4'), ('5', )])
        ]
        for value, dups_flag, res in sort_combs_in_list_case:
            self.assertEqual(sort_combs_in_list(value, dups_flag), res)

    def test_remove_dups(self):
        dups_case = [
            ([], []),
            ([('1', ), ('2', ), ('1', ), ('3', )], [('1', ), ('2', ), ('3', )]),
            ([('1', ), ('2', ), ('1', ), ('3', ), ('1', )], [('1', ), ('2', ), ('3', )]),
            ([('1', '2'), ('1', '2'), ('3', )], [('1', '2'), ('3', )]),
            ([('1', '2'), ('1', '2'), ('3', '3')], [('1', '2'), ('3', '3')]),
        ]
        for value, res in dups_case:
            self.assertEqual(remove_dup_combs(value), res)

    def test_gen_posib_combs(self):
        all_combs_case = [
            ((), 1, 0),
            ((1, 2), 1, 2),
            ((1, 2), 2, 4),
            ((1, 2, 3), 2, 9),
            ((1, 2, 3), 3, 27)
        ]
        for value, opt, res in all_combs_case:
            self.assertEqual(len(gen_combs(value, opt)), res)

    def test_gen_uniq_combs(self):
        unique_combs_case = [
            ((), 1, 0),
            ((1, 2), 1, 2),
            ((1, 2), 2, 1),
            ((1, 2, 3), 2, 3),
            ((1, 2, 3), 3, 1),
            ((1, 2, 3, 4), 2, 6),
        ]
        for value, opt, res in unique_combs_case:
            self.assertEqual(len(gen_sorted_combs(value, opt, True)), res)

    def test_get_used_items(self):
        used_items_case = [
            ([], [], 2, []),
            (['1', '2', '3', '4'], [('1', '2'), ('2', '3'), ('2', '4')], 2, ['2']),
            (['1', '2', '3', '4'], [('1', '2'), ('2', '3'), ('2', '4'), ('3', '4')], 2, ['2']),
            (['1', '2', '3', '4'], [('1', '2'), ('1', '3'), ('2', '3'), ('2', '4'), ('3', '4')], 2, ['2', '3']),
            (['1', '2', '3', '4'], [('1', '2'), ('1', '3'), ('2', '3'), ('2', '4'), ('3', '4')], 3, []),
            (['1', '2', '4'], [('1', '2'), ('1', '3'), ('2', '3'), ('2', '4'), ('3', '4')], 2, ['2']),
            (['1', '2', '3', '4'], [], 2, []),
            (['1', '2', '3', '4', '5'], [], 2, []),
            (['2', '3', '4', '5', '6'], [('2', '3'), ('2', '4'), ('5', '2'), ('2', '6'), ('5', '3'), ('6', '3')], 2, ['2']),
            (['1', '2', '3', '4', '5'], [('1',), ('2',)], 1, ['1', '2'])
        ]
        for items, cur_combs, size, res in used_items_case:
            self.assertEqual(get_used_items(items, cur_combs, size), res)

    def test_get_remaining_items(self):
        remaining_items_case = [
            ([], [], 2, []),
            (['1', '2', '3', '4'], [('1', '2'), ('2', '3'), ('2', '4')], 2, ['1', '3', '4']),
            (['1', '2', '3', '4'], [('1', '2'), ('2', '3'), ('2', '4'), ('3', '4')], 2, ['1', '3', '4']),
            (['1', '2', '3', '4'], [('1', '2'), ('1', '3'), ('2', '3'), ('2', '4'), ('3', '4')], 2, ['1', '4']),
            (['1', '2', '3', '4'], [('1', '2'), ('1', '3'), ('2', '3'), ('2', '4'), ('3', '4')], 3, ['1', '2', '3', '4']),
            (['1', '2', '4'], [('1', '2'), ('1', '3'), ('2', '3'), ('2', '4'), ('3', '4')], 2, ['1', '4']),
            (['1', '2', '3', '4'], [], 2, ['1', '2', '3', '4']),
            (['1', '2', '3', '4', '5'], [], 2, ['1', '2', '3', '4', '5']),
            (['1', '2', '3', '4', '5'], [('1', '2'), ('1', '3'), ('4', '1'), ('1', '5'), ('4', '2'), ('5', '2')], 2, ['2', '3', '4', '5']),
            (['1', '2', '3', '4', '5'], [('1',), ('2',)], 1, ['3', '4', '5'])
        ]
        for items, cur_combs, size, res in remaining_items_case:
            self.assertEqual(get_remaining_items(items, cur_combs, size), res)

    def test_check_uniformity(self):
        uniformity_case = [
            ([], 1, True),
            ([], 2, True),
            ([('1', '2'), ('3', '4')], 2, True),
            ([('1', '2'), ('3', '4')], '2', True),
            ([('1', '2'), ('3', '4')], 3, False),
            ([('1', '2'), ('3', '4', '5')], 2, False),
            ([('1', '2'), ('3', '4', '5')], 3, False),
        ]
        for input, size, output in uniformity_case:
            self.assertEqual(output, check_uniformity(input, size))

    def test_uniq_items_combs(self):
        uniq_items_combs_case = [
            ([], [], 2, []),
            ([1, 2, 3], [(1, 2), (2, 3), (1, 3)], 2, [(1, 2, 3)]),
            ([1, 2, 3], [(1, 3), (2, 3), (1, 2)], 2, [(1, 3, 2)]),
            ([1, 2, 3, 4], [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)], 2, [(1, 2), (3, 4)]),
        ]
        for items, uniq_combs, comb_size, output in uniq_items_combs_case:
            self.assertEqual(output, uniq_item_combs(items, uniq_combs, comb_size))

        uniq_items_combs_error_case = [
            ([1, 2, 3, 4], [(2, 3), (2, 4), (3, 4)], 2),
        ]
        for items, uniq_combs, combs_size in uniq_items_combs_error_case:
            with self.assertRaises(IndexError):
                uniq_item_combs(items, uniq_combs, combs_size)


if __name__ == '__main__':
    unittest.main()

