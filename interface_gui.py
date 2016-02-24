from tkinter import *
from groups_maker import GroupsMaker
from tkinter.filedialog import askopenfilename, asksaveasfilename
import random


#root.resizable(width=FALSE, height=FALSE)

class Univercity(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        self.dean = Dean()
        self.add_widgets()

    def add_widgets(self):
        # Input names frame
        ent_frame = Frame(self)
        ent_frame.pack(side=TOP, expand=YES, fill=X)
        Label(ent_frame, text='Entry students names').pack(side=TOP, fill=X)
        self.names_input = Entry(ent_frame)
        self.names_input.insert(0, 'misha, kate, dasha, sasha, serega, yula')
        self.names_input.pack(side=TOP, expand=YES, fill=X)
        self.names_input.focus()

        # Table frame
        self.tab_frame = Frame(self)
        self.tab_lab = Label(self.tab_frame, text='Your table will be here')
        self.tab_lab.pack(expand=YES)
        self.tab_frame.pack(side=LEFT, anchor=W)
        self.colors = ['red', 'blue', 'green', 'yellow']

        # Action frame
        but_frame = Frame(self)
        but_frame.pack(side=RIGHT, expand=YES, fill=Y)
        Button(but_frame, text='add',     command=lambda: self.add()).pack(side=TOP, fill=X)
        Button(but_frame, text='clean',   command=lambda: self.delete_all()).pack(side=TOP, fill=X)
        self.size_group = Entry(but_frame)
        self.size_group.insert(0, '2')
        self.size_group.pack(side=TOP)
        self.duration = Entry(but_frame)
        self.duration.insert(0, '5')
        self.duration.pack(side=TOP)
        Button(but_frame, text='load',    command=lambda: self.open_filenames()).pack(side=TOP, fill=X)
        Button(but_frame, text='save',    command=lambda: self.save_filenames()).pack(side=TOP, fill=X)
        Button(but_frame, text='combine', command=lambda: self.get_calendar()).pack(side=BOTTOM, fill=X)

    def open_filenames(self):
        filename = askopenfilename()
        self.names_input.delete(0, END)
        self.names_input.insert(0, open(filename).read())

    def save_filenames(self):
        filename = asksaveasfilename()
        names = self.get_names()
        open(filename, 'w').write(', '.join(names))

    @staticmethod
    def split_names(names_string):
        names = names_string.split(',')
        return [name.strip() for name in names]

    def add(self):
        self.tab_lab.destroy()
        new_students_names = self.split_names(self.names_input.get())
        for student_name in new_students_names:
            student = Student(student_name, self.dean, self.tab_frame)
            self.dean.enroll_student(student)

    def check_duplicates(self):
        self.refresh()
        duplicates = False
        all_names = self.get_names()
        count = {}
        for name in all_names:
            if name in count:
                count[name] += 1
            else:
                count[name] = 1
        for name, value in count.items():
            if value > 1:
                duplicates = True
                color = random.choice(self.colors)
                for student in self.all_students:
                    if student.name == name:
                        student.set_bg_color(color)
        return duplicates

    def refresh(self):
        student_to_remove = []
        for student in self.all_students:
            if not student.name:
                student_to_remove.append(student)
        for student in student_to_remove:
            self.all_students.remove(student)
        for student, idx in zip(self.all_students, range(1, len(self.all_students) + 1)):
            student.update_widgets()

    def delete_all(self):
        for student in self.all_students:
            student.remove()
        self.refresh()

    def get_names(self):
        return [student.name for student in self.all_students]

    def get_calendar(self):
        duplicates = self.check_duplicates()
        if not duplicates:
            g = GroupsMaker(self.get_names(), int(self.duration.get()), size_group=int(self.size_group.get()))
            calendar = g.get_timetable()
            time_table = Toplevel(self)
            lesson_count = 1
            for lesson in calendar:
                lesson_frame = Frame(time_table)
                lesson_frame.pack(side=LEFT, fill=Y)
                Label(lesson_frame, text=str(lesson_count)).pack(side=TOP)
                lesson_count += 1
                for combs in lesson:
                    comb_frame = Frame(lesson_frame, bd=3, relief=RAISED)
                    comb_frame.pack(side=TOP)
                    for name in combs:
                        Label(comb_frame, width=10, text=name).pack(side=TOP)


class Student:
    def __init__(self, name, dean, parent=None):
        self.name = name
        self.dean = dean
        self.idx = len(self.dean.students) + 1
        self.parent = parent
        self.make_student_frame()

    def ask_idx(self):
        return self.dean.give_student_idx(self)

    def make_student_frame(self):
        self.student_fr = Frame(self.parent)
        self.student_fr.pack(side=TOP)
        self.lab = Label(self.student_fr, text=self.idx, relief=RIDGE, width=5)
        self.ent = Entry(self.student_fr, width=20)
        self.but = Button(self.student_fr, text='x', command=lambda: self.delete_student())
        self.lab.pack(side=LEFT)
        self.ent.pack(side=LEFT)
        self.but.pack(side=RIGHT)
        self.ent.insert(0, self.name)
        self.ent.bind('<Return>', self.change_name)

    def set_bg_color(self, color):
        self.ent.config(bg=color)

    def update_widgets(self):
        self.student_fr.destroy()
        self.make_student_frame()

    def change_name(self, event):
        old_name = self.name
        new_name = self.ent.get()
        self.name = new_name
        print('Name %s successufully change to %s' % (old_name, new_name))
        if not self.name:
            self.lab.grid_remove()
            self.ent.grid_remove()

    def delete_student(self):
        self.student_fr.destroy()
        self.dean.expel_student(self)


class Dean:
    def __init__(self):
        self.students = []

    def enroll_student(self, student):
        self.students.append(student)

    def update_student_idx(self):
        for student, idx in zip(self.students, range(1, len(self.students) + 1)):
            student.idx = idx
            student.update_widgets()

    def expel_student(self, student):
        self.students.remove(student)
        self.update_student_idx()




root = Tk()
#root.wm_geometry("")
root.title('GroupsMaker')
# width, height = root.maxsize()
# root.geometry('%sx%s' % (round(0.5 * width), round(0.5 * height)))
Univercity(root).pack(side=TOP, fill=X)
root.mainloop()
