import unittest
from combs_math import *


class TestCombsMath(unittest.TestCase):
    def test_pack(self):
        pack_case = [
            ([], 0, []),
            ([], 1, []),
            ([], 2, []),
            (['1', '2', '3', '4'], 1, [('1', ), ('2', ), ('3', ), ('4', )]),
            ([1, 2, 3, 4], 1, [(1, ), (2, ), (3, ), (4, )]),
            (['1', '2', '3', '4', '5', '6'], 2, [('1', '2'), ('3', '4'), ('5', '6')]),
            (['1', '2', '3', '4', '5', '6'], 3, [('1', '2', '3'), ('4', '5', '6')]),
            (['1', '2', '3', '4', '5', '6', '7'], 3, [('1', '2', '3'), ('4', '5', '6'), ('7', )]),
            (['1', '2', '3', '4', '5', '6', '7'], 0, []),
            (['1', '2', '3', '4', '5', '6', '7'], 100, [('1', '2', '3', '4', '5', '6', '7')])
        ]
        for in_list, comb_size, out_combs_list in pack_case:
            self.assertEqual(pack(in_list, comb_size), out_combs_list)

    def test_unpack(self):
        unpack_case = [
            ([], []),
            ([('1', )], ['1']),
            ([('1', ), ('2', ), ('3', ), ('4', )], ['1', '2', '3', '4']),
            ([('a', ), ('b', ), ('c', ), ('d', )], ['a', 'b', 'c', 'd']),
            ([(1, ), (2, ), (3, ), (4, )], [1, 2, 3, 4]),
            ([('1', '2'), ('3', '4'), ('5', '6')], ['1', '2', '3', '4', '5', '6']),
            ([('1', '2', '3'), ('4', '5', '6')], ['1', '2', '3', '4', '5', '6']),
            ([('1', '2'), ('3', ), ('4', '5', '6')], ['1', '2', '3', '4', '5', '6'])
        ]
        for in_combs_list, out_list in unpack_case:
            self.assertEqual(unpack(in_combs_list), out_list)

    def test_molder(self):
        molder_case = [
            ([], 1, []),
            ([('1', ), 0,  []]),
            ([('1', ), ('2', ), ('3', )], 1, [('1', ), ('2', ), ('3', )]),
            ([('1', ), ('2', ), ('3', )], 2, [('1', '2'), ('3', )]),
            ([('1', ), ('2', '3')], 1, [('1', ), ('2', ), ('3', )]),
            ([('1', '2', '3')], 2, [('1', '2'), ('3', )]),
            ([('1', '2'), ('3', '4')], 2, [('1', '2'), ('3', '4')]),
            ([('1', '2'), ('3', ), ('4', )], 2, [('1', '2'), ('3', '4')]),
            ([('1', '2'), ('3', ), ('4', )], 0, []),
            ([('1', '2'), ('3', ), ('4', )], 100, [('1', '2', '3', '4')]),
        ]
        for in_combs_list, comb_size, out_combs_list in molder_case:
            self.assertEqual(molder(in_combs_list, comb_size), out_combs_list)

    def test_sort_comb(self):
        sort_comb_case = [
            ([], True, ()),
            ((), True, ()),
            ([], False, ()),
            (('1', '2'), True, ('1', '2')),
            (('2', '1'), True, ('1', '2')),
            (('2', '1', 'a'), True, ('1', '2', 'a')),
            (('2', '1', '1'), True, ('1', '1', '2')),
            (('2', '1', '1'), False, ('1', '2'))
        ]
        for income, dups, out_tuple in sort_comb_case:
            self.assertEqual(sort_comb(income, dups), out_tuple)

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
        for in_combs_list, dups, out_combs_list in sort_combs_in_list_case:
            self.assertEqual(sort_combs_in_list(in_combs_list, dups), out_combs_list)

    def test_remove_dups(self):
        dups_case = [
            ([], []),
            ([('1', ), ('2', ), ('1', ), ('3', )], [('1', ), ('2', ), ('3', )]),
            ([('1', ), ('2', ), ('1', ), ('3', ), ('1', )], [('1', ), ('2', ), ('3', )]),
            ([('1', '2'), ('1', '2'), ('3', )], [('1', '2'), ('3', )]),
            ([('1', '2'), ('1', '2'), ('3', '3')], [('1', '2'), ('3', '3')]),
        ]
        for in_combs_list, out_combs_list in dups_case:
            self.assertEqual(remove_dup_combs(in_combs_list), out_combs_list)

    def test_gen_combs(self):
        combs_case = [
            ((), 1, False, 0),
            ((), 1, True, 0),
            ((1, 2), 1, False, 2),
            ((1, 2), 1, True, 2),
            ((1, 2), 2, False, 4),
            ((1, 2), 2, True, 2),
            ((1, 2, 3), 2, False, 9),
            ((1, 2, 3), 2, True, 6),
            ((1, 2, 3), 3, False, 27),
            ((1, 2, 3), 3, True, 6)
        ]
        for items, comb_size, uniq, out_combs_total in combs_case:
            self.assertEqual(len(gen_combs(items, comb_size, uniq)), out_combs_total)

    def test_gen_sorted_combs(self):
        gen_sorted_combs_case = [
            ((), 1, False, 0),
            ((), 1, True, 0),
            ((1, 2), 1, False, 2),
            ((1, 2), 1, True, 2),
            ((1, 2), 2, False, 3),
            ((1, 2), 2, True, 1),
            ((1, 2, 3), 2, False, 6),
            ((1, 2, 3), 2, True, 3),
            ((1, 2, 3), 3, False, 10),
            ((1, 2, 3), 3, True, 1),
            ((1, 2, 3, 4), 2, False, 10),
            ((1, 2, 3, 4), 2, True, 6),
        ]
        count = 0
        for items, comb_size, uniq, out_combs_total in gen_sorted_combs_case:
            count += 1
            self.assertEqual(len(gen_sorted_combs(items, comb_size, uniq)), out_combs_total,
                             'CASE %s: %s, %s, %s' % (count, items, comb_size, uniq))

    def test_get_used_items(self):
        used_items_case = [
            ([], [], 2, []),
            (['1', '2', '3', '4'], [('1', ), ('2', ), ('3', )], 2, ['1', '2', '3']),
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
        for items, combs_list, comb_size, out_list in used_items_case:
            self.assertEqual(get_used_items(items, combs_list, comb_size), out_list)

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

    def test_get_pack(self):
        pack_case = [
            ([], [], 2, []),
            ([1, 2, 3], [(1, 2), (2, 3), (1, 3)], 2, [(1, 2, 3)]),
            ([1, 2, 3], [(1, 3), (2, 3), (1, 2)], 2, [(1, 3, 2)]),
            ([1, 2, 3, 4], [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)], 2, [(1, 2), (3, 4)]),
            ([1, 2, 3, 4], [(1, 4), (2, 3), (2, 4), (3, 4)], 2, [(1, 4), (2, 3)]),
            ([1, 2, 3, 4], [(2, 3), (1, 4), (2, 4), (3, 4)], 2, [(2, 3), (1, 4)]),
        ]
        for items, uniq_combs, comb_size, output in pack_case:
            self.assertEqual(output, get_pack(items, uniq_combs, comb_size))

        pack_error_case = [
            ([1, 2, 3, 4], [(2, 3), (2, 4), (3, 4)], 2),
            ([1, 2, 3, 4], [(3, 4), (2, 3), (1, 4), (2, 4)], 2)
        ]
        for items, uniq_combs, combs_size in pack_error_case:
            with self.assertRaises(IndexError):
                get_pack(items, uniq_combs, combs_size)

    def test_get_packs(self):
        packs_case = [
            ([], 2, []),
            ([1, 2, 3], 2, [(1, 2, 3)]),
        ]
        for items, pack_total, output in packs_case:
            self.assertEqual(output, PacksGenerator(items).get_packs(pack_total))

if __name__ == '__main__':
    unittest.main()

