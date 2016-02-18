from tkinter import *
from groups_maker import GroupsMaker

#root.resizable(width=FALSE, height=FALSE)
#root.geometry('600x400')


class MainLogic(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        self.all_students = []
        self.add_widgets()

    def add_widgets(self):
        self.ent_frame = Frame(self)
        self.ent_frame.pack(side=TOP, fill=X)
        Label(self.ent_frame, text='Entry students names').pack(side=TOP, fill=X)
        self.names_input = Entry(self.ent_frame)
        self.names_input.insert(0, 'misha, kate, yula, serega, dasha, sasha')
        self.names_input.pack(side=TOP, fill=X)
        self.names_input.focus()
        Button(self.ent_frame, text='add', command=(lambda: self.add())).pack(side=LEFT)
        Button(self.ent_frame, text='combine', command=(lambda: self.get_calendar())).pack(side=RIGHT)
        Button(self.ent_frame, text='show names', command=(lambda: self.show_names())).pack(side=RIGHT)
        self.tab_frame = Frame(self)
        self.tab_frame.pack(side=TOP, anchor=W)

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
        student_to_remove = []
        for student in self.all_students:
            if not student.name:
                student_to_remove.append(student)
        for student in student_to_remove:
            self.all_students.remove(student)
        for student in self.all_students:
            print(student.name)


class Student:
    def __init__(self, name, student_id, parent=None):
        self.name = name
        self.parent = parent
        self.student_id = student_id
        self.get_coordinates()
        self.make_widget()

    def make_widget(self):
        self.lab = Label(self.parent, text=self.student_id, relief=RIDGE, width=5)
        self.ent = Entry(self.parent, width=20)
        self.lab.grid(row=self.row, column=self.col_lab)
        self.ent.grid(row=self.row, column=self.col_ent)
        self.ent.insert(0, self.name)
        self.ent.bind('<Return>', self.change_name)
        self.ent.bind('<Delete>', self.delete_name)

    def get_coordinates(self):
        self.row = (self.student_id - 1) % 15
        self.col_lab = ((self.student_id - 1)// 15) * 2
        self.col_ent = ((self.student_id - 1)// 15) * 2 + 1

    def update_id(self, student_id):
        self.student_id = student_id

    def change_name(self, event):
        old_name = self.name
        new_name = self.ent.get()
        self.name = new_name
        print('Name %s successufully change to %s' % (old_name, new_name))
        if not self.name:
            self.lab.grid_remove()
            self.ent.grid_remove()

    def delete_name(self, event):
        self.lab.grid_remove()
        self.ent.grid_remove()
        self.name = ''


root = Tk()
root.title('GroupsMaker')
MainLogic(root)
root.mainloop()
