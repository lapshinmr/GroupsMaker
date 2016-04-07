"""
In this module you can find math logic for program.
"""
import random
from gm_exceptions import *


def molder(combs_list, comb_size=1):
    unpacked = []
    for comb in combs_list:
        for name in comb:
            unpacked.append(name)
    packed = []
    while unpacked:
        comb, unpacked = unpacked[:comb_size], unpacked[comb_size:]
        packed.append(tuple(comb))
    return packed


def unique_sorter(combs_list):
    sorted_combs_list = []
    for comb in combs_list:
        comb = sorted(list(comb))
        sorted_combs_list.append(tuple(comb))
    return set(sorted_combs_list)


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
        self.whitelist = self.sort_exclist(whitelist)
        self.blacklist = self.sort_exclist(blacklist)
        self.repetitions = repetitions
        self.wrong_whitelist = None
        self.wrong_blacklist = None
        self.uniq_combs, self.wrong_blacklist = self.subtract_exclist(self.make_uniq_combs(), self.blacklist)
        self.uniq_combs_total = len(self.uniq_combs)
        self.st_total = len(self.st_names)
        self.les_groups_total = self.st_total // self.size_group
        self.first_ttpart_total = 0
        self.middle_ttpart_total = 0
        self.last_ttpart_total = 0
        self.attempts = 0
        self.limit_attempts = self.les_total * attempts_factor

    @staticmethod
    def sort_exclist(exclist):
        return list(set([tuple(sorted(comb)) for comb in exclist]))

    def make_uniq_combs(self):
        """
        Make unique combinations with names
        """
        combs = [(name, ) for name in self.st_names]
        while len(combs[0]) < self.size_group:
            tmp_combs = []
            for name in self.st_names:
                for comb in combs:
                    if name not in comb:
                        comb += (name, )
                        tmp_combs.append(comb)
            else:
                combs = tmp_combs[:]
        return list(set([tuple(sorted(comb)) for comb in combs]))

    @staticmethod
    def subtract_exclist(uniq_combs, exclist):
        wrong_exclist = []
        uniq_combs = uniq_combs[:]
        for comb in exclist:
            try:
                uniq_combs.remove(comb)
            except ValueError:
                print('No such comb %s in unique combs' % str(comb))
                wrong_exclist.append(comb)
        return uniq_combs, wrong_exclist

    @staticmethod
    def get_combs_with_name(name, combs):
        """
        This method gets all combinations with input name from input set of combinations
        :param name: string with name
        :param combs: list, tuple or set of combs
        :return:
        """
        return [comb for comb in combs if name in comb]

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
                for comb in self.get_combs_with_name(name, unique_combs):
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
        uniq_combs, self.wrong_whitelist = self.subtract_exclist(self.uniq_combs, self.whitelist)
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

    def get_wrong_whitelist(self):
        return self.wrong_whitelist

    def get_wrong_blacklist(self):
        return self.wrong_blacklist

    def get_attempts(self):
        return self.attempts


if __name__ == '__main__':
    """
    students = list(range(24))
    g = GroupsMaker(students, les_total=10, size_group=2)
    tt, parts = g.get_timetable()
    print(len(g.uniq_combs))
    for les in tt:
        print(les)
    """
    import unittest

    combs1 = []
    combs2 = [('misha', ), ('kate', ), ('yula', ), ('serega', ), ('dasha', ), ('sasha', )]
    combs3 = [('misha', ), ('kate', ), ('yula', ), ('serega', ), ('dasha', 'sasha')]
    combs4 = [('misha', 'kate'), ('yula', 'serega'), ('dasha', 'sasha')]
    combs5 = [('misha', 'kate'), ('yula', 'serega'), ('dasha', ), ('sasha', )]
    combs6 = [('misha', 'kate'), ('yula', 'serega'), ('dasha', ), ('sasha', ), ('ruslan', )]
    combs7 = [('misha', 'kate'), ('yula', 'serega'), ('dasha', 'sasha'), ('ruslan', )]
    combs8 = [('misha', 'kate'), ('yula', 'serega'), ('dasha', 'sasha', 'ruslan')]

    combs9 = {('misha', ), ('kate', ), ('misha', ), ('serega', ), ('dasha', ), ('sasha', )}
    combs10 = {('misha', ), ('kate', ), ('serega', ), ('dasha', ), ('sasha', )}
    combs11 = {('kate', 'misha'), ('serega', 'yula'), ('dasha', 'sasha')}
    combs12 = {('kate', 'misha'), ('yula', 'serega'), ('serega', 'yula'), ('dasha', 'sasha')}

    class TestStringMethods(unittest.TestCase):
        def test_molder(self):
            self.assertEqual(molder(combs1, 1), combs1)
            self.assertEqual(molder(combs2, 1), combs2)
            self.assertEqual(molder(combs3, 1), combs2)
            self.assertEqual(molder(combs4, 2), combs4)
            self.assertEqual(molder(combs5, 2), combs4)
            self.assertEqual(molder(combs6, 2), combs7)
            self.assertEqual(molder(combs8, 2), combs7)

        def test_unique_sorter(self):
            self.assertEqual(unique_sorter(combs1), set())
            self.assertEqual(unique_sorter(combs9), combs10)
            self.assertEqual(unique_sorter(combs12), combs11)

    unittest.main()
