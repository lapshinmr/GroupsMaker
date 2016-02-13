"""
You can find main logic here.
"""


class GroupsMaker:
    def __init__(self, student_names, total_lessons):
        self.student_names = student_names
        self.total_lessons = total_lessons

    def combine(self):
        print(self.student_names)

if __name__ == '__main__':
    students = ['misha', 'kate', 'yula']
    g = GroupsMaker(students, 6)
    g.combine()

