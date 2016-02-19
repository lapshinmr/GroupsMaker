"""
In this module you can find math logic for program.
"""
import random
from gm_exceptions import *


class GroupsMaker:
    """
    Class work with set of names
    """
    def __init__(self, student_names, total_lessons, group_amount=2, unwanted_combs=None):
        self.student_names = student_names
        self.total_lessons = total_lessons
        self.group_amount = group_amount
        self.unique_combs = []
        self.used_combs = []
        self.unwanted_combs = unwanted_combs

    def make_unique_combs(self):
        """
        Make unique combinations with names
        """
        combs = [(name, ) for name in self.student_names]
        while len(combs[0]) < self.group_amount:
            tmp_combs = []
            for name in self.student_names:
                for comb in combs:
                    if name not in comb:
                        comb += (name,)
                        tmp_combs.append(comb)
            else:
                combs = tmp_combs[:]
        self.unique_combs = list(set([tuple(sorted(comb)) for comb in combs]))

    @staticmethod
    def get_combs_with_name(name, combs):
        """
        This method gets all combinations with input name from input set of combinations
        :param name: string with name
        :param combs: list, tuple or set of combs
        :return:
        """
        return [comb for comb in combs if name in comb]

    def get_lesson_combs(self):
        """
        Method choose combs for one lesson/day so combs has no repetitions of names.
        Quantity of names may be add or even.
        """
        names = self.student_names[:]
        unique_combs = self.unique_combs[:]
        lesson_combs = []
        while len(names) > 1:
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
        # add odd name to the random combs
        else:
            if any(names):
                random_idx = random.randrange(len(lesson_combs))
                lesson_combs[random_idx] += tuple(names)
        return lesson_combs

    def get_calendar(self):
        """
        Makes from N students class groups with n students during m lessons/days
        """
        self.make_unique_combs()
        all_combs = self.unique_combs[:]
        calendar = []
        total_attempts = 0
        while len(calendar) < self.total_lessons:
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


if __name__ == '__main__':
    students = ['misha', 'kate', 'serega', 'yula', 'dasha', 'sasha', 'kolya']
    g = GroupsMaker(students, 5, group_amount=3)
    # print(g.get_lesson_groups(g.unique_combs))
    g.make_unique_combs()
    print(g.get_lesson_combs(g.unique_combs))

