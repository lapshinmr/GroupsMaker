from tkinter import *
from groups_maker import GroupsMaker

#root.resizable(width=FALSE, height=FALSE)
#root.geometry('600x400')


class MainLogic:
    def __init__(self):
        self.root = Tk()
        self.root.title('GroupsMaker')
        self.ent_frame = Frame(self.root)
        self.ent_frame.pack(side=TOP, fill=X)
        Label(self.ent_frame, text='Entry students names').pack(side=TOP, fill=X)
        self.names_input = Entry(self.ent_frame)
        self.names_input.insert(0, 'misha, kate, yula, serega, dasha, sasha')
        self.names_input.pack(side=TOP, fill=X)
        self.names_input.focus()
        Button(self.ent_frame, text='add', command=(lambda: self.add())).pack(side=LEFT)
        Button(self.ent_frame, text='combine', command=(lambda: self.get_calendar())).pack(side=RIGHT)
        Button(self.ent_frame, text='show names', command=(lambda: self.show_names())).pack(side=RIGHT)
        self.tab_frame = Frame(self.root)
        self.tab_frame.pack(side=TOP, anchor=W)
        self.all_students = []

    def start(self):
        self.root.mainloop()

    @staticmethod
    def split_names(names_string):
        seps = '.,;'
        for sep in seps:
            names_string = names_string.replace(sep, ' ')
        return names_string.split()

    def get_calendar(self):
        pass
        """
            g = GroupsMaker(names, 3)
            calendar = g.get_calendar()
            with open('calendar', 'w') as f:
                idx = 0
                for day in calendar:
                    idx += 1
                    f.write('%s: ' % idx)
                    for pare in day:
                        f.write('%20s ' % str(pare))
                    f.write('\n')
        """

    def add(self):
        new_names = self.split_names(self.names_input.get())
        for name in new_names:
            student = Student(name, self.tab_frame)
            self.all_students.append(student)

    def show_names(self):
        for student in self.all_students:
            print(student.name)


class Student:
    students_id = 0

    @staticmethod
    def rice_id():
        Student.students_id += 1
        return Student.students_id

    def __init__(self, name, parent=None):
        self.name = name
        self.student_id = self.rice_id()
        self.row = (self.student_id - 1) % 15
        self.col_lab = ((self.student_id - 1)// 15) * 2
        self.col_ent = ((self.student_id - 1)// 15) * 2 + 1
        self.lab = Label(parent, text=self.students_id, relief=RIDGE, width=5)
        self.ent = Entry(parent, width=20)
        self.lab.grid(row=self.row, column=self.col_lab)
        self.ent.grid(row=self.row, column=self.col_ent)
        self.ent.insert(0, self.name)
        self.ent.bind('<Return>', self.change_name)

    def change_name(self, event):
        self.name = self.ent.get()
        print(self.name)


m = MainLogic()
m.start()
