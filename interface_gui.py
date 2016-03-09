import os
from tkinter import *
from groups_maker import GroupsMaker
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import *
from gm_exceptions import *


class Univercity(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self.dean = Dean()
        self.add_widgets()
        self.calendar = []

    def add_widgets(self):
        self.add_menu()
        self.add_toolbar()
        self.add_input_field()
        self.add_table()

    def add_menu(self):
        top = Menu(self.parent)
        self.parent.config(menu=top)
        file = Menu(top, tearoff=False)
        file.add_command(label='load names', command=self.open_names_from_file,  underline=0)
        file.add_command(label='save names', command=self.save_names_as_text,  underline=0)
        top.add_cascade(label='File', menu=file, underline=0)

    def add_toolbar(self):
        but_frame = Frame(self)
        but_frame.pack(side=TOP, expand=YES, fill=X)
        Button(but_frame, text='add', command=self.add).pack(side=LEFT)
        Button(but_frame, text='clean', command=self.delete_all).pack(side=LEFT)
        Button(but_frame, text='show timetable', command=self.show_calendar).pack(side=LEFT)

        Label(but_frame, text='group size', width=10).pack(side=LEFT)
        self.size_group = Entry(but_frame, width=10, justify=CENTER)
        self.size_group.insert(0, '2')
        self.size_group.pack(side=LEFT)

        Label(but_frame, text='lessons', width=10).pack(side=LEFT)
        self.duration = Entry(but_frame, width=10, justify=CENTER)
        self.duration.insert(0, '5')
        self.duration.pack(side=LEFT)

    def add_input_field(self):
        ent_frame = Frame(self)
        ent_frame.config(height=50)
        ent_frame.pack(side=TOP, expand=YES, fill=X)
        ent_frame.pack_propagate(False)
        text = Text(ent_frame)
        scroll_bar = Scrollbar(ent_frame)
        scroll_bar.config(command=text.yview)
        text.config(yscrollcommand=scroll_bar.set)
        scroll_bar.pack(side=RIGHT, fill=Y)
        text.insert(1.0, 'Please, entry names of your students here.')
        text.pack(side=LEFT, expand=YES, fill=BOTH)
        text.focus()
        self.input_names = text
        # self.input_names.bind('<Return>', lambda event: self.add())

    def add_table(self):
        canvas = Canvas(self, borderwidth=0)# , width=300, height=400)
        canvas.pack(side=LEFT, anchor=W)
        canvas.config(height=300, width=300)
        self.canvas = canvas

    def open_names_from_file(self):
        filename = askopenfilename()
        if filename:
            self.input_names.delete(1.0, END)
            self.input_names.insert(1.0, open(filename, encoding='utf-8-sig').read())

    def save_names_as_text(self):
        filename = asksaveasfilename(filetypes=[('txt', '.txt')])
        if filename:
            filename = os.path.splitext(filename)[0]
            names = self.dean.get_students_names()
            open(filename + '.txt', 'w', encoding='utf-8').write(', '.join(names))

    @staticmethod
    def split_names(names_string):
        names = names_string.split(',')
        return [name.strip() for name in names]

    def add(self):
        # self.canvas.destroy()
        new_students_names = self.split_names(self.input_names.get(1.0, END))
        for student_name in new_students_names:
            student = Student(student_name, self.dean, self.canvas)
            self.dean.enroll_student(student)
        self.input_names.delete(1.0, END)

    def check_duplicates(self):
        duplicates = False
        count = {}
        for name in self.dean.get_students_names():
            if name in count:
                count[name] += 1
            else:
                count[name] = 1
        for student in self.dean.students:
            if count[student.name] > 1:
                student.set_font_color('red')
                duplicates = True
            else:
                student.set_font_color('black')
        return duplicates

    def delete_all(self):
        while self.dean.students:
            self.dean.students[-1].delete_student()

    def show_calendar(self):
        duplicates = self.check_duplicates()
        if not duplicates:
            g = GroupsMaker(self.dean.get_students_names(), int(self.duration.get()), size_group=int(self.size_group.get()))
            try:
                self.calendar = g.get_timetable()
                time_table = Toplevel(self)
                time_table.title('Timetable')
                Button(time_table, text='save timetable', command=self.save_calendar_as_plain_text).pack(side=BOTTOM, fill=X)
                lesson_count = 1
                for lesson in self.calendar:
                    lesson_frame = Frame(time_table)
                    lesson_frame.pack(side=LEFT, fill=Y)
                    Label(lesson_frame, text='%s %s' % (lesson_count, 'lesson')).pack(side=TOP)
                    lesson_count += 1
                    for combs in lesson:
                        comb_frame = Frame(lesson_frame, bd=2, relief=RAISED)
                        comb_frame.pack(side=TOP)
                        for name in combs:
                            Label(comb_frame, width=10, text=name).pack(side=TOP)
            except NotEnoughCombinations:
                showwarning('Warning', 'The number of students is not enough to form the groups')
        else:
            showwarning('Warning', 'The timetable is not created. Please change duplicated the names.')

    def save_calendar_as_plain_text(self):
        filename = asksaveasfilename(filetypes=[('txt', '.txt')])
        if filename:
            filename = os.path.splitext(filename)[0]
            open(filename + '.txt', 'w', encoding='utf-8').write(self.generate_txt())
            open(filename + '.tex', 'w', encoding='utf-8').write(self.generate_tex())

    def generate_txt(self):
        text = ''
        lesson_count = 1
        for lesson in self.calendar:
            text += '%s неделя: ' % lesson_count
            lesson_count += 1
            for combs in lesson:
                text += ('(' + ', '.join(list(combs)) + ') ')
            text += '\n'
        return text

    def generate_tex(self):
        start = (r'\documentclass[a4paper]{article}' + '\n'
                 r'\usepackage[landscape]{geometry}' + '\n'
                 r'\usepackage[utf8]{inputenc}' + '\n'
                 r'\usepackage[russian]{babel}' + '\n'
                 r'\begin{document}' + '\n'
                 r'\thispagestyle{empty}' + '\n'
                 r'\mbox{}' + '\n'
                 r'\vfill' + '\n'
                 r'\begin{center}' + '\n'
                 )
        end = (r'\end{center}' + '\n'
                  r'\vfill' + '\n'
                  r'\end{document}' + '\n')

        main_table = r'\begin{tabular}'
        main_table += '{' + '|'.join('c' * (len(self.calendar[0]) + 1)) + r'}\hline'
        lesson_count = 1
        for lesson in self.calendar:
            main_table += str(lesson_count)
            lesson_count += 1
            for comb in lesson:
                main_table += '&' + r'\begin{tabular}{c}'
                main_table += r'\\'.join(list(comb))
                main_table += r'\end{tabular}'
            main_table += r'\\\hline' + '\n'
        main_table += r'\end{tabular}' + '\n'
        return start + main_table + end


class Dean:
    def __init__(self):
        self.students = []

    def enroll_student(self, student):
        self.students.append(student)

    def update_students_idx(self):
        for student, idx in zip(self.students, range(1, len(self.students) + 1)):
            student.idx.set(idx)

    def expel_student(self, student):
        self.students.remove(student)
        self.update_students_idx()

    def get_students_names(self):
        return [student.name for student in self.students]


class Student:
    def __init__(self, name, dean, parent=None):
        self.name = name
        self.dean = dean
        self.idx = IntVar()
        self.idx.set(len(self.dean.students) + 1)
        self.parent = parent
        self.make_student_frame()

    def make_student_frame(self):
        #student_fr = Frame()
        #student_fr.pack(side=TOP)
        #Label(student_fr, textvariable=self.idx, width=3).pack(side=LEFT, anchor=W)
        # but = Button(student_fr, text='x', command=self.delete_student).pack(side=RIGHT, anchor=E)
        ent = Entry(self.parent, width=20, font=1)
        ent.pack(side=LEFT)
        # ent.insert(0, self.name)
        # ent.bind('<KeyPress>', self.change_name)
        self.parent.create_window(0, self.idx.get() * 20, window=ent, width=100, height=20)
        self.ent = ent
        # self.student_fr = student_fr

    def set_font_color(self, color):
        self.ent.config(fg=color)

    def change_name(self, event):
        if event.keysym == 'Return':
            new_name = self.ent.get()
            self.name = new_name
            return
        self.ent.event_generate('<Return>', when='tail')

    def delete_student(self):
        self.student_fr.destroy()
        self.dean.expel_student(self)


root = Tk()
#root.resizable(width=FALSE, height=FALSE)
#root.wm_geometry("")
root.title('GroupsMaker')
width, height = root.maxsize()
root.geometry('%sx%s' % (round(0.25 * width), round(0.25 * height)))
Univercity(root).pack(side=TOP, fill=X)
root.mainloop()
