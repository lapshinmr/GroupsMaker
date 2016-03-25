"""
In this module you can find math logic for program.
"""
import random
from gm_exceptions import *


class GroupsMaker:
    """
    les - lesson;
    st - student;
    exclist - exclude list
    """
    def __init__(self, st_names, les_total, size_group=2, whitelist=(), blacklist=()):
        self.st_names = st_names
        self.les_total = les_total
        self.size_group = size_group
        self.whitelist = self.sort_exclist(whitelist)
        self.blacklist = self.sort_exclist(blacklist)
        self.wrong_whitelist = None
        self.wrong_blacklist = None
        self.uniq_combs, self.wrong_blacklist = self.subtract_exclist(self.make_uniq_combs(), self.blacklist)
        self.uniq_combs_total = len(self.uniq_combs)
        self.st_total = len(self.st_names)
        self.les_groups_total = self.st_total // self.size_group
        self.first_ttpart_total = 0
        self.middle_ttpart_total = 0
        self.last_ttpart_total = 0

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

    def lesson_possibility(self):
        if not self.st_total // self.size_group >= 2:
            raise NotEnoughCombinations

    def get_lesson_combs(self, combs):
        """
        Method choose combs for one lesson/day so combs has no repetitions of names.
        Quantity of names may be add or even.
        """
        self.lesson_possibility()
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

    def get_unique_lessons(self, number, unique_combs):
        timetable_attempt = 0
        while True:
            try:
                all_combs = unique_combs[:]
                calendar = []
                day_attempts = 0
                while len(calendar) < number:
                    while True:
                        try:
                            groups = self.get_lesson_combs(all_combs)
                            break
                        except IndexError:
                            day_attempts += 1
                            if day_attempts > 30:
                                raise AttemptsExceeded(day_attempts)
                            continue
                    all_combs = list(set(all_combs) - set(groups))
                    calendar.append(groups)
                return calendar
            except AttemptsExceeded:
                timetable_attempt += 1
                if timetable_attempt > 30:
                    print("Sorry, I can't generate timetable")
                    raise GenerateTimetableException

    def first_ttpart(self):
        uniq_combs, self.wrong_whitelist = self.subtract_exclist(self.uniq_combs, self.whitelist)
        uniq_combs_total = len(uniq_combs)
        uniq_les_total = uniq_combs_total // self.les_groups_total
        if self.les_total < uniq_les_total:
            self.first_ttpart_total = self.les_total
        else:
            self.first_ttpart_total = uniq_les_total
        return self.get_unique_lessons(self.first_ttpart_total, uniq_combs)

    def middle_ttpart(self):
        timetable = []
        uniq_les_total = self.uniq_combs_total // self.les_groups_total
        whole_les_uniq_sets_total = (self.les_total - self.first_ttpart_total) // uniq_les_total
        for uniq_set in range(whole_les_uniq_sets_total):
            timetable.append(self.get_unique_lessons(uniq_les_total, self.uniq_combs))
        self.middle_ttpart_total = whole_les_uniq_sets_total * uniq_les_total
        return timetable

    def last_ttpart(self):
        remainder = self.les_total - self.first_ttpart_total - self.middle_ttpart_total
        return self.get_unique_lessons(remainder, self.uniq_combs)

    def get_timetable(self):
        timetable = []
        timetable.append(self.first_ttpart())
        if self.first_ttpart_total < self.les_total:
            timetable.extend(self.middle_ttpart())
        if self.first_ttpart_total + self.middle_ttpart_total < self.les_total:
            timetable.append(self.last_ttpart())
        return timetable

    def get_wrong_whitelist(self):
        return self.wrong_whitelist

    def get_wrong_blacklist(self):
        return self.wrong_blacklist


if __name__ == '__main__':
    # students = ['misha', 'kate', 'serega', 'yula', 'dasha', 'sasha', 'dima', 'stas', 'masha', 'kolya']
    # students = [str(item) for item in list(range(10))]
    students = list(range(12))
    whitelist = ()
    blacklist = ()
    g = GroupsMaker(students, 20, size_group=2, blacklist=blacklist, whitelist=whitelist)
    timetable = g.get_timetable()
    print(timetable)
    part_count = 1
    for part in timetable:
        print('Part %s:' % part_count)
        part_count += 1
        for lesson in part:
            print('\t%s' % lesson)

    print(g.get_wrong_whitelist())
    print(g.get_wrong_blacklist())
