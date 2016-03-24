"""
In this module you can find math logic for program.
"""
import random
from gm_exceptions import *


class GroupsMaker:
    """
    Class work with set of names
    """
    def __init__(self, student_names, lessons_total, size_group=2, whitelist=(), blacklist=()):
        self.student_names = student_names
        self.lessons_total = lessons_total
        self.size_group = size_group
        self.whitelist = whitelist
        self.blacklist = blacklist
        self.unique_combs = self.make_unique_combs()
        self.unique_combs = self.subtract_exclist(self.blacklist)
        self.unique_combs_total = len(self.unique_combs)
        self.students_total = len(self.student_names)

    def make_unique_combs(self):
        """
        Make unique combinations with names
        """
        combs = [(name, ) for name in self.student_names]
        while len(combs[0]) < self.size_group:
            tmp_combs = []
            for name in self.student_names:
                for comb in combs:
                    if name not in comb:
                        comb += (name, )
                        tmp_combs.append(comb)
            else:
                combs = tmp_combs[:]
        return list(set([tuple(sorted(comb)) for comb in combs]))

    def subtract_exclist(self, exclist):
        unique_combs = self.unique_combs[:]
        try:
            for comb in exclist:
                unique_combs.remove(comb)
        except ValueError:
            print('blacklist is wrong')
        finally:
            return unique_combs

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
        return self.students_total - (self.students_total // self.size_group) * self.size_group

    def lesson_possibility(self):
        if not self.students_total // self.size_group >= 2:
            raise NotEnoughCombinations

    def get_lesson_combs(self, combs):
        """
        Method choose combs for one lesson/day so combs has no repetitions of names.
        Quantity of names may be add or even.
        """
        self.lesson_possibility()
        names = self.student_names[:]
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
        while True:
            try:
                all_combs = unique_combs[:]
                calendar = []
                total_attempts = 0
                while len(calendar) < number:
                    while True:
                        try:
                            groups = self.get_lesson_combs(all_combs)
                            break
                        except IndexError:
                            total_attempts += 1
                            if total_attempts > 30:
                                raise AttemptsExceeded(total_attempts)
                            continue
                    all_combs = list(set(all_combs) - set(groups))
                    calendar.append(groups)
                return calendar
            except AttemptsExceeded:
                print('one more time')

    def get_crop_timetable(self):
        timetable = []
        if self.whitelist:
            unique_combs = self.subtract_exclist(self.whitelist)
            unique_lessons_count = len(unique_combs) // onelesson_combs_count
            timetable.extend(self.get_unique_lessons(unique_lessons_count, unique_combs))

    def get_timetable(self):
        """
        Makes from N students class groups with n students during m lessons/days
        """
        timetable = []
        les_groups_total = self.students_total // self.size_group
        unique_lessons_count = self.unique_combs_total // les_groups_total
        whole_lesson_sets = self.lessons_total // unique_lessons_count
        for dummy in range(whole_lesson_sets - 1):
            timetable.extend(self.get_unique_lessons(unique_lessons_count, self.unique_combs))
        else:
            remainder = self.lessons_total % unique_lessons_count
            timetable.extend(self.get_unique_lessons(remainder, self.unique_combs))
        return timetable


if __name__ == '__main__':
    # students = ['misha', 'kate', 'serega', 'yula', 'dasha', 'sasha', 'dima', 'stas', 'masha', 'kolya']
    # students = [str(item) for item in list(range(10))]
    students = list(range(6))
    g = GroupsMaker(students, 5, size_group=2, blacklist=((1, 2), (3, 5), (1, 3)))
    print(g.unique_combs)
