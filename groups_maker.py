"""
You can find main logic here.
"""
import random


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

    def get_calendar(self):
        all_combs = self.unique_combs[:]

    def get_lesson_groups(self, combs):
        names = self.student_names[:]
        tmp_combs = combs[:]
        lesson_groups = []
        while names:
            random.shuffle(names)
            name = random.choice(names)
            group = random.choice(self.get_combs_with_name(name, tmp_combs))
            lesson_groups.append(group)
            combs_to_del = []
            for name in group:
                for group in self.get_combs_with_name(name, tmp_combs):
                    if group not in combs_to_del:
                        combs_to_del.append(group)
                names.remove(name)
            tmp_combs = list(set(tmp_combs) - set(combs_to_del))
        return lesson_groups





if __name__ == '__main__':
    students = ['misha', 'kate', 'serega', 'yula', 'dasha', 'sasha']
    g = GroupsMaker(students, 3, group_amount=3)
    g.combine()
    print(g.get_lesson_groups(g.unique_combs))

