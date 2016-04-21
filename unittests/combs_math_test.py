import unittest
from combs_math import *


class TestCombsMath(unittest.TestCase):
    def test_subtract_combs(self):
        pack_case = [
            ([], [], []),
            ([], [(2, )], []),
            ([(1, ), (3, )], [(2, )], [(1, ), (3, )]),
            ([(1, ), (2, ), (3, )], [(2, )], [(1, ), (3, )])
        ]
        for minuend, subtrahend, diff in pack_case:
            self.assertEqual(subtract_combs(minuend, subtrahend), diff)

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

    def test_sort_items_in_comb(self):
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
            self.assertEqual(sort_items_in_comb(income, dups), out_tuple)

    def test_sort_items_in_all_combs(self):
        sort_items_in_all_combs_case = [
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
        for in_combs_list, dups, out_combs_list in sort_items_in_all_combs_case:
            self.assertEqual(sort_items_in_all_combs(in_combs_list, dups), out_combs_list)

    def test_remove_dups(self):
        remove_dups_case = [
            ([], []),
            ([('1', ), ('2', ), ('1', ), ('3', )], [('1', ), ('2', ), ('3', )]),
            ([('1', ), ('2', ), ('1', ), ('3', ), ('1', )], [('1', ), ('2', ), ('3', )]),
            ([('1', '2'), ('1', '2'), ('3', )], [('1', '2'), ('3', )]),
            ([('1', '2'), ('1', '2'), ('3', '3')], [('1', '2'), ('3', '3')]),
            ([['1', '2'], ['1', '2'], ['3', '3']], [['1', '2'], ['3', '3']]),
        ]
        for sequence, out_sequence in remove_dups_case:
            self.assertEqual(remove_dups(sequence), out_sequence)

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
            ((1, 2, 3), 3, True, 6),
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

    def test_get_items_from_combs(self):
        used_items_case = [
            ([], [], 2, []),
            (['1', '2', '3', '4'], [('1', ), ('2', ), ('3', )], 1, ['1', '2', '3']),
            (['1', '2', '3', '4'], [('1', ), ('2', ), ('3', ), ('5', )], 1, ['1', '2', '3']),
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
            self.assertEqual(get_items_from_combs(items, combs_list, comb_size), out_list)

        remaining_items_case = [
            ([], [], 2, False, []),
            (['1', '2', '3', '4'], [('1', '2'), ('2', '3'), ('2', '4')], 2, False, ['1', '3', '4']),
            (['1', '2', '3', '4'], [('1', '2'), ('2', '3'), ('2', '4'), ('3', '4')], 2, False, ['1', '3', '4']),
            (['1', '2', '3', '4'], [('1', '2'), ('1', '3'), ('2', '3'), ('2', '4'), ('3', '4')], 2, False, ['1', '4']),
            (['1', '2', '3', '4'], [('1', '2'), ('1', '3'), ('2', '3'), ('2', '4'), ('3', '4')], 3, False, ['1', '2', '3', '4']),
            (['1', '2', '4'], [('1', '2'), ('1', '3'), ('2', '3'), ('2', '4'), ('3', '4')], 2, False, ['1', '4']),
            (['1', '2', '3', '4'], [], 2, False, ['1', '2', '3', '4']),
            (['1', '2', '3', '4', '5'], [], 2, False, ['1', '2', '3', '4', '5']),
            (['1', '2', '3', '4', '5'], [('1', '2'), ('1', '3'), ('4', '1'), ('1', '5'), ('4', '2'), ('5', '2')], 2, False, ['2', '3', '4', '5']),
            (['1', '2', '3', '4', '5'], [('1',), ('2',)], 1, False, ['3', '4', '5'])
        ]
        for items, combs_list, comb_size, remain, out_list in remaining_items_case:
            self.assertEqual(get_items_from_combs(items, combs_list, comb_size, remain), out_list)

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
        for in_combs_list, comb_size, output in uniformity_case:
            self.assertEqual(check_uniformity(in_combs_list, comb_size), output)

    def test_get_hist(self):
        dummy = lambda x: x
        get_hist_case = [
            ((), dummy, dummy, {}),
            ([[], [], []], len, dummy, {0: [[], [], []]}),
            (([], [], []), len, dummy, {0: [[], [], []]}),
            ((1, 2, 3, 3, 2), dummy, dummy, {1: [1], 2: [2, 2], 3: [3, 3]}),
            ((-1, 1, -1, 10, 2, 3, 3, 2), dummy, len, {-1: 2, 1: 1, 2: 2, 3: 2, 10: 1}),
            ([1, 2, 3, 3, 2], dummy, len, {1: 1, 2: 2, 3: 2}),
            ([[1, 2], [1, 2], [1], [1, 2, 3]], len, dummy, {1: [[1]], 2: [[1, 2], [1, 2]], 3: [[1, 2, 3]]})
        ]
        count = 0
        for sequence, axis_x, axis_y, hist in get_hist_case:
            count += 1
            self.assertEqual(get_hist(sequence, axis_x, axis_y), hist, 'CASE %s' % count)


if __name__ == '__main__':
    unittest.main()

