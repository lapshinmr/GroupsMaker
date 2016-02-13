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
        self.unique_combs = set([tuple(sorted(comb)) for comb in combs])
        return [set(comb) for comb in self.unique_combs]

    def get_random_comb(self, name):
        combs_with_name = []
        for comb in self.unique_combs:
            if name in comb:
                combs_with_name.append(comb)
        return random.choice(combs_with_name)

    def get_remain_names(self, names, all_names):
        comb = list(comb)
        for name in names:
            comb.remove(name)
        return tuple(comb)

    def get_calendar(self, unique_combs):
        while True:
            name, *other_names = random.shuffle(self.student_names)
            comb = self.get_random_comb(name)
            self.used_combs.append(comb)
            self.get_remain_names(name)


if __name__ == '__main__':
    students = ['misha', 'kate', 'serega', 'yula', 'dasha', 'sasha']
    g = GroupsMaker(students, 2, group_amount=3)
    print(g.combine())
    # print(g.get_remain_names(['misha'], g.get_random_comb('misha')))

