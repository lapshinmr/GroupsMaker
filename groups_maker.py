"""
You can find main logic here.
"""


class GroupsMaker:
    def __init__(self, student_names, total_lessons, group_amount=2):
        self.student_names = student_names
        self.total_lessons = total_lessons
        self.group_amount = group_amount

    def combine(self):
        combs = [(name, ) for name in self.student_names]
        while len(combs[0]) < self.group_amount:
            output = []
            for name in self.student_names:
                for comb in combs:
                    if name not in comb:
                        comb += (name,)
                        output.append(comb)
            else:
                combs = output[:]
        unique_combs = set([tuple(sorted(comb)) for comb in combs])
        return unique_combs
        # output = set([tuple(sorted(comb)) for comb in combs])

if __name__ == '__main__':
    students = ['misha', 'kate', 'yula', 'serega', 'dasha', 'sasha']
    g = GroupsMaker(students, 5, group_amount=4)
    print(g.combine())

