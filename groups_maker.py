"""
In this module you can find math logic for program.
"""
import random
from gm_exceptions import *


class GroupsMaker:
    """
    Class work with set of names
    """
    def __init__(self, student_names, lessons_total, size_group=2, unwanted_combs=None):
        self.student_names = student_names
        self.lessons_total = lessons_total
        self.size_group = size_group
        self.unwanted_combs = unwanted_combs
        self.unique_combs = self.make_unique_combs()
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
                        comb += (name,)
                        tmp_combs.append(comb)
            else:
                combs = tmp_combs[:]
        return list(set([tuple(sorted(comb)) for comb in combs]))

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

    def get_lesson_combs(self, combs):
        """
        Method choose combs for one lesson/day so combs has no repetitions of names.
        Quantity of names may be add or even.
        """
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

    def lesson_possibility(self):
        if self.students_total // self.size_group >= 2:
            return True
        else:
            return False

    def compare_combs_duration(self):
        available_lessons = self.unique_combs_total / (self.students_total // self.size_group)
        if available_lessons >= self.lessons_total:
            return True
        else:
            return False

    def make_attempt(self):
        all_combs = self.unique_combs[:]
        calendar = []
        total_attempts = 0
        while len(calendar) < self.lessons_total:
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

    def get_lessons(self):
        """
        Makes from N students class groups with n students during m lessons/days
        """
        while True:
            try:
                self.make_attempt()
            except AttemptsExceeded:
                print('one more time')


if __name__ == '__main__':
    # students = ['misha', 'kate', 'serega', 'yula', 'dasha', 'sasha', 'dima', 'stas', 'masha', 'kolya']
    # students = [str(item) for item in list(range(10))]
    students = list(range(10))
    g = GroupsMaker(students, 1, size_group=3)
    # g.get_lessons()
    print(g.get_lesson_combs(g.unique_combs))
    # print(len(g.unique_combs))
    # print(g.compare_combs_duration())
    # count = {}
    # for day in g.get_lessons():
    #     for comb in day:
    #         if comb in count:
    #             count[comb] += 1
    #         else:
    #             count[comb] = 1
    # for key in count:
    #     print(key, count[key])

