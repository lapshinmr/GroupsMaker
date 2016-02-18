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
        self.names_input.insert(0, ', '.join([str(item) for item in range(30)]))
        self.names_input.pack(side=TOP, fill=X)
        self.names_input.focus()
        Button(self.ent_frame, text='add', command=(lambda: self.add())).pack(side=LEFT)
        Button(self.ent_frame, text='combine', command=(lambda: self.get_calendar())).pack(side=RIGHT)
        Button(self.ent_frame, text='refresh', command=(lambda: self.refresh())).pack(side=RIGHT)
        Button(self.ent_frame, text='delete all', command=(lambda: self.delete_all())).pack(side=RIGHT)
        self.tab_frame = Frame(self)
        self.tab_frame.pack(side=TOP, anchor=W)

    @staticmethod
    def split_names(names_string):
        seps = '.,;'
        for sep in seps:
            names_string = names_string.replace(sep, ' ')
        return names_string.split()

    def get_coordinates(self, student_idx):
        row = (student_idx - 1) % 15
        col_lab = ((student_idx - 1)// 15) * 2
        col_ent = ((student_idx - 1)// 15) * 2 + 1
        return row, col_lab, col_ent

    def add(self):
        new_names = self.split_names(self.names_input.get())
        start_idx = len(self.all_students) + 1
        end_idx = start_idx + len(new_names)
        for name, idx in zip(new_names, range(start_idx, end_idx)):
            student = Student(name, idx, self.get_coordinates(idx), self.tab_frame)
            self.all_students.append(student)

    def update_students(self, student, idx):
        student.student_id = idx
        student.coords = self.get_coordinates(idx)

    def refresh(self):
        student_to_remove = []
        for student in self.all_students:
            if not student.name:
                student_to_remove.append(student)
        for student in student_to_remove:
            self.all_students.remove(student)
        for student, idx in zip(self.all_students, range(1, len(self.all_students) + 1)):
            self.update_students(student, idx)
            student.update_widgets()
            print(student.name, student.coords)

    def delete_all(self):
        for student in self.all_students:
            student.remove()
        self.refresh()



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


class Student:
    def __init__(self, name, student_id, coords, parent=None):
        self.name = name
        self.student_id = student_id
        self.coords = coords
        self.parent = parent
        self.make_widgets()

    def make_widgets(self):
        self.lab = Label(self.parent, text=self.student_id, relief=RIDGE, width=5)
        self.ent = Entry(self.parent, width=20)
        self.lab.grid(row=self.coords[0], column=self.coords[1])
        self.ent.grid(row=self.coords[0], column=self.coords[2])
        self.ent.insert(0, self.name)
        self.ent.bind('<Return>', self.change_name)
        self.ent.bind('<Delete>', self.delete_name)

    def update_widgets(self):
        self.lab.grid_remove()
        self.ent.grid_remove()
        self.make_widgets()

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

    def remove(self):
        self.lab.grid_remove()
        self.ent.grid_remove()
        self.name = ''


root = Tk()
#root.wm_geometry("")
root.title('GroupsMaker')
MainLogic(root)
root.mainloop()
