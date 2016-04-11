import random
from gm_exceptions import *


def subtract_combs(combs_list, exclist):
    uniq_combs = combs_list[:]
    for comb in exclist:
        try:
            uniq_combs.remove(comb)
        except ValueError:
            print('No such comb %s in unique combs' % str(comb))
    return uniq_combs


def unpack(combs_list):
    unpacked = []
    for comb in combs_list:
        for name in comb:
            unpacked.append(name)
    return unpacked


def pack(names, comb_size):
    packed = []
    while names:
        comb, names = names[:comb_size], names[comb_size:]
        packed.append(tuple(comb))
    return packed


def molder(combs_list, comb_size=1):
    unpacked = unpack(combs_list)
    packed = pack(unpacked, comb_size)
    return packed


def sort_comb(comb, dups=True):
    comb = list(comb)
    if not dups:
        comb = list(set(comb))
    return tuple(sorted(comb))


def sort_combs_in_list(combs_list, dups=True):
    return [sort_comb(comb, dups) for comb in combs_list]


def remove_dup_combs(combs_list):
    unique_list = []
    while combs_list:
        comb, *combs_list = combs_list
        while comb in combs_list:
            combs_list.remove(comb)
        unique_list.append(comb)
    return unique_list


def gen_combs(items_list, comb_size=1, uniq=False):
    combs = list(zip(items_list))
    for dummy in range(comb_size - 1):
        tmp_combs = set()
        for comb in combs:
            for item in items_list:
                if uniq and item in comb:
                    continue
                tmp_combs.add(comb + (item, ))
        combs = tmp_combs
    return combs


def gen_sorted_combs(items_list, comb_size, uniq=False):
    combs = gen_combs(items_list, comb_size, uniq)
    return set(sort_combs_in_list(combs))


def get_used_items(items, combs, comb_size):
    possible_combs = gen_sorted_combs(items, comb_size, uniq=True)
    sorted_combs = sort_combs_in_list(combs)
    unused_combs = set(possible_combs) - set(sorted_combs)
    unused_items = set(unpack(unused_combs))
    return sorted(list(set(items) - unused_items))


class GroupsMaker:
    """
    les - lesson;
    st - student;
    exclist - exclude list
    """
    def __init__(self, st_names, les_total, size_group=2, attempts_factor=10,
                 whitelist=(), blacklist=(), repetitions=False):
        self.st_names = st_names
        self.les_total = les_total
        self.size_group = size_group
        self.whitelist = sort_combs_list(whitelist)
        self.blacklist = sort_combs_list(blacklist)
        self.repetitions = repetitions
        self.uniq_combs = gen_sorted_combs(self.st_names, size_group, uniq=True)
        self.uniq_combs = subtract_combs(self.uniq_combs, self.blacklist)
        self.uniq_combs_total = len(self.uniq_combs)
        self.st_total = len(self.st_names)
        self.les_groups_total = self.st_total // self.size_group
        self.first_ttpart_total = 0
        self.middle_ttpart_total = 0
        self.last_ttpart_total = 0
        self.attempts = 0
        self.limit_attempts = self.les_total * attempts_factor

    def get_module(self):
        return self.st_total - (self.st_total // self.size_group) * self.size_group

    def get_lesson(self, combs):
        """
        Method choose combs for one lesson/day so combs has no repetitions of names.
        Quantity of names may be add or even.
        """
        names = self.st_names[:]
        unique_combs = combs[:]
        lesson_combs = []
        while len(names) > self.get_module():
            random_comb = random.choice(unique_combs)
            lesson_combs.append(random_comb)
            combs_to_del = set()
            # delete all combs with names that already chosen by getting random combination
            for name in random_comb:
                for comb in find_combs_by_item(name, unique_combs):
                    if comb not in combs_to_del:
                        combs_to_del.add(comb)
                names.remove(name)
            unique_combs = list(set(unique_combs) - combs_to_del)
        # add remaining names to the random combs
        else:
            if len(names) > 0:
                idxs = list(range(len(lesson_combs)))
                random.shuffle(idxs)
                random_idxs = idxs[:len(names)]
                for name, idx in zip(names, random_idxs):
                    lesson_combs[idx] += (name,)
        return lesson_combs

    def get_lessons(self, unique_combs):
        all_combs = unique_combs[:]
        calendar = []
        while True:
            try:
                lesson = self.get_lesson(all_combs)
            except IndexError:
                break
            else:
                all_combs = list(set(all_combs) - set(lesson))
                calendar.append(lesson)
        return calendar

    def get_part_without_whitelist(self):
        uniq_combs = subtract_combs(self.uniq_combs, self.whitelist)
        return self.get_lessons(uniq_combs)

    def get_timetable(self):
        timetable = []
        parts = []
        timetable.extend(self.get_part_without_whitelist())
        if not self.repetitions:
            return timetable, parts
        while len(timetable) < self.les_total:
            next_tt_part = self.get_lessons(self.uniq_combs)
            if next_tt_part:
                parts.append(len(timetable))
                timetable.extend(next_tt_part)
            self.attempts += 1
            if self.attempts > self.limit_attempts:
                raise NotEnoughStudents
        else:
            cur_ttlen = len(timetable)
            extra_ttlen = cur_ttlen - self.les_total
            if extra_ttlen:
                timetable = timetable[:-extra_ttlen]
        return timetable, parts

    def get_attempts(self):
        return self.attempts


if __name__ == '__main__':
    import unittest

    pack_case = [
        ([], 0, []),
        ([], 1, []),
        ([], 2, []),
        (['1', '2', '3', '4'], 1, [('1', ), ('2', ), ('3', ), ('4', )]),
        (['1', '2', '3', '4', '5', '6'], 2, [('1', '2'), ('3', '4'), ('5', '6')]),
        (['1', '2', '3', '4', '5', '6'], 3, [('1', '2', '3'), ('4', '5', '6')]),

    ]

    unpack_case = [
        ([], []),
        ([('1', )], ['1']),
        ([('1', ), ('2', ), ('3', ), ('4', )], ['1', '2', '3', '4']),
        ([('1', '2'), ('3', '4'), ('5', '6')], ['1', '2', '3', '4', '5', '6']),
        ([('1', '2', '3'), ('4', '5', '6')], ['1', '2', '3', '4', '5', '6']),
        ([('1', '2'), ('3', ), ('4', '5', '6')], ['1', '2', '3', '4', '5', '6'])
    ]

    molder_case = [
        ([], 1, []),
        ([('1', ), ('2', ), ('3', )], 1, [('1', ), ('2', ), ('3', )]),
        ([('1', ), ('2', '3')], 1, [('1', ), ('2', ), ('3', )]),
        ([('1', '2'), ('3', '4')], 2, [('1', '2'), ('3', '4')]),
        ([('1', '2'), ('3', ), ('4', )], 2, [('1', '2'), ('3', '4')]),
        ([('1', ), ('2', ), ('3', )], 2, [('1', '2'), ('3', )]),
        ([('1', '2', '3')], 2, [('1', '2'), ('3', )]),
        ([('1', '2'), ('3', ), ('4', )], 2, [('1', '2'), ('3', '4')])
    ]

    sort_comb_case = [
        ([], True, ()),
        ((), True, ()),
        ([], False, ()),
        (('1', '2'), True, ('1', '2')),
        (('2', '1'), True, ('1', '2')),
        (('2', '1', '1'), True, ('1', '1', '2')),
        (('2', '1', '1'), False, ('1', '2'))
    ]

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

    dups_case = [
        ([], []),
        ([('1', ), ('2', ), ('1', ), ('3', )], [('1', ), ('2', ), ('3', )]),
        ([('1', ), ('2', ), ('1', ), ('3', ), ('1', )], [('1', ), ('2', ), ('3', )]),
        ([('1', '2'), ('1', '2'), ('3', )], [('1', '2'), ('3', )]),
        ([('1', '2'), ('1', '2'), ('3', '3')], [('1', '2'), ('3', '3')]),
    ]

    all_combs_case = [
        ((), 1, 0),
        ((1, 2), 1, 2),
        ((1, 2), 2, 4),
        ((1, 2, 3), 2, 9),
        ((1, 2, 3), 3, 27)
    ]

    unique_combs_case = [
        ((), 1, 0),
        ((1, 2), 1, 2),
        ((1, 2), 2, 1),
        ((1, 2, 3), 2, 3),
        ((1, 2, 3), 3, 1),
        ((1, 2, 3, 4), 2, 6),
    ]

    used_items_case = [
        ([], [], 2, []),
        (['1', '2', '3', '4'], [('1', '2'), ('2', '3'), ('2', '4')], 2, ['2']),
        (['1', '2', '3', '4'], [('1', '2'), ('2', '3'), ('2', '4'), ('3', '4')], 2, ['2']),
        (['1', '2', '3', '4'], [('1', '2'), ('1', '3'), ('2', '3'), ('2', '4'), ('3', '4')], 2, ['2', '3']),
        (['1', '2', '3', '4'], [('1', '2'), ('1', '3'), ('2', '3'), ('2', '4'), ('3', '4')], 3, []),
        (['1', '2', '4'], [('1', '2'), ('1', '3'), ('2', '3'), ('2', '4'), ('3', '4')], 2, ['2']),
        (['1', '2', '3', '4'], [], 2, []),
        (['1', '2', '3', '4', '5'], [], 2, []),
        (['2', '3', '4', '5', '6'], [('2', '3'), ('2', '4'), ('5', '2'), ('2', '6'), ('5', '3'), ('6', '3')], 2, ['2'])
    ]

    class TestStringMethods(unittest.TestCase):
        def test_pack(self):
            for value, opt, res in pack_case:
                self.assertEqual(pack(value, opt), res)

        def test_unpack(self):
            for value, res in unpack_case:
                self.assertEqual(unpack(value), res)

        def test_molder(self):
            for value, opt, res in molder_case:
                self.assertEqual(molder(value, opt), res)

        def test_sort_comb(self):
            for value, dups_flag, res in sort_comb_case:
                self.assertEqual(sort_comb(value, dups_flag), res)

        def test_sort_combs_in_list(self):
            for value, dups_flag, res in sort_combs_in_list_case:
                self.assertEqual(sort_combs_in_list(value, dups_flag), res)

        def test_remove_dups(self):
            for value, res in dups_case:
                self.assertEqual(remove_dup_combs(value), res)

        def test_gen_posib_combs(self):
            for value, opt, res in all_combs_case:
                self.assertEqual(len(gen_combs(value, opt)), res)

        def test_gen_uniq_combs(self):
            for value, opt, res in unique_combs_case:
                self.assertEqual(len(gen_sorted_combs(value, opt, True)), res)

        def test_get_used_items(self):
            for items, cur_combs, size, res in used_items_case:
                self.assertEqual(get_used_items(items, cur_combs, size), res)

    unittest.main()

