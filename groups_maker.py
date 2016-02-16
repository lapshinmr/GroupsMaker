"""
You can find main logic here.
"""
import random
from gm_exceptions import *


class GroupsMaker:
    def __init__(self, student_names, total_lessons, group_amount=2, unwanted_combs=[]):
        self.student_names = student_names
        self.total_lessons = total_lessons
        self.group_amount = group_amount
        self.unique_combs = []
        self.used_combs = []

    def combine(self):
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
        combs_with_name = []
        for comb in combs:
            if name in comb:
                combs_with_name.append(comb)
        return combs_with_name

    def get_lesson_groups(self, combs):
        names = self.student_names[:]
        tmp_combs = combs[:]
        lesson_groups = []
        while any(names):
            group = random.choice(tmp_combs)
            lesson_groups.append(group)
            combs_to_del = set()
            for name in group:
                for group in self.get_combs_with_name(name, tmp_combs):
                    if group not in combs_to_del:
                        combs_to_del.add(group)
                names.remove(name)
            tmp_combs = list(set(tmp_combs) - combs_to_del)
        return lesson_groups

    def get_calendar(self):
        self.combine()
        all_combs = self.unique_combs[:]
        calendar = []
        total_attempts = 0
        while len(calendar) < self.total_lessons:
            while True:
                try:
                    groups = self.get_lesson_groups(all_combs)
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
    students = ['misha', 'kate', 'serega', 'yula', 'dasha', 'sasha']
    g = GroupsMaker(students, 5, group_amount=2)
    # print(g.get_lesson_groups(g.unique_combs))
    total_groups = set()
    for lesson in g.get_calendar():
        total_groups.update(set(lesson))

