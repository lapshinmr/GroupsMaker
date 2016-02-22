from tkinter import *
from groups_maker import GroupsMaker
from tkinter.filedialog import askopenfilename, asksaveasfilename
import random


#root.resizable(width=FALSE, height=FALSE)

class MainLogic(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        self.all_students = []
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
        new_names = self.split_names(self.names_input.get())
        start_idx = len(self.all_students) + 1
        end_idx = start_idx + len(new_names)
        for name, idx in zip(new_names, range(start_idx, end_idx)):
            student = Student(name, idx, self.tab_frame)
            self.all_students.append(student)

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
    def __init__(self, name, student_id, parent=None):
        self.name = name
        self.student_id = student_id
        self.parent = parent
        self.make_widgets()

    def make_widgets(self):
        self.student_fr = Frame(self.parent)
        self.student_fr.pack(side=TOP)
        self.lab = Label(self.student_fr, text=self.student_id, relief=RIDGE, width=5)
        self.ent = Entry(self.student_fr, width=20)
        self.but = Button(self.student_fr, text='x', command=lambda: self.delete_student())
        self.lab.pack(side=LEFT)
        self.ent.pack(side=RIGHT)
        self.ent.insert(0, self.name)
        self.ent.bind('<Return>', self.change_name)

    def set_bg_color(self, color):
        self.ent.config(bg=color)

    def update_widgets(self):
        self.lab.destroy()
        self.ent.destroy()
        self.make_widgets()

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
        self.name = ''

    def remove(self):
        self.lab.grid_remove()
        self.ent.grid_remove()
        self.name = ''


root = Tk()
#root.wm_geometry("")
root.title('GroupsMaker')
# width, height = root.maxsize()
# root.geometry('%sx%s' % (round(0.5 * width), round(0.5 * height)))
MainLogic(root).pack(side=TOP, fill=X)
root.mainloop()
