import os
from tkinter import *
from groups_maker import GroupsMaker
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import *
from gm_exceptions import *
from tkinter import ttk
import math


class Univercity(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.dean = Dean()
        self.add_widgets()
        self.calendar = []

    def add_widgets(self):
        self.add_menu()
        self.add_toolbar()
        self.paned_win = PanedWindow(orient=VERTICAL)
        self.paned_win.pack(fill=BOTH, expand=YES)
        self.add_input_field()
        self.add_canvas()

    def add_menu(self):
        top = Menu(self.parent)
        self.parent.config(menu=top)
        file = Menu(top, tearoff=False)
        file.add_command(label='load names', command=self.open_names_from_file,  underline=0)
        file.add_command(label='save names', command=self.save_names_as_text,  underline=0)
        top.add_cascade(label='File', menu=file, underline=0)

    def add_toolbar(self):
        but_frame = Frame(self)
        but_frame.pack(side=TOP, fill=X)
        Button(but_frame, text='add', command=self.add).pack(side=LEFT)
        Button(but_frame, text='clean', command=self.dean.expel_all_students).pack(side=LEFT)
        Button(but_frame, text='show timetable', command=self.show_calendar).pack(side=LEFT)

        size_fr = LabelFrame(but_frame, text='size', padx=5, pady=0)
        size_fr.pack(side=RIGHT)
        self.size_group = Spinbox(size_fr, from_=2, to_=5, justify=CENTER, width=6)
        self.size_group.pack(side=TOP)

        dur_fr = LabelFrame(but_frame, text='lessons', padx=5, pady=0)
        dur_fr.pack(side=RIGHT)
        self.duration = Spinbox(dur_fr, from_=1, to_=10, justify=CENTER, width=6)
        self.duration.pack(side=TOP)

    def add_input_field(self):
        ent_frame = Frame(self.paned_win)
        self.paned_win.add(ent_frame)
        ent_frame.config(height=50)
        ent_frame.pack(side=TOP, fill=X)
        ent_frame.pack_propagate(False)
        text = Text(ent_frame)
        scroll_bar = ttk.Scrollbar(ent_frame)
        scroll_bar.config(command=text.yview)
        text.config(yscrollcommand=scroll_bar.set)
        scroll_bar.pack(side=RIGHT, fill=Y)
        #text.insert(1.0, 'Please, entry names of your students here.')
        text.insert(1.0, '1, 2, 3, 4')
        text.pack(side=LEFT, expand=YES, fill=BOTH)
        text.focus()
        self.input_names = text
        # self.input_names.bind('<Return>', lambda event: self.add())

    def add_canvas(self):
        canv_frame = Frame(self.paned_win)
        self.paned_win.add(canv_frame)
        canv_frame.pack(side=TOP, expand=YES, fill=BOTH)
        canv = Canvas(canv_frame, highlightthickness=0)
        canv.bind('<Configure>', self.resize_canvas)
        sbar = ttk.Scrollbar(canv_frame)
        sbar.config(command=canv.yview)
        canv.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        canv.pack(side=LEFT, expand=YES, fill=BOTH)
        self.canvas = canv
        self.dean.set_canvas(self.canvas)

    def resize_canvas(self, event):
        self.canvas.config(width=event.width, height=event.height)
        self.dean.move_students()

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
        stud_names = self.split_names(self.input_names.get(1.0, END))
        new_students = []
        for stud_name in stud_names:
            new_stud = Student(stud_name, self.dean, self.canvas)
            self.dean.enroll_student(new_stud)
            new_students.append(new_stud)
        self.dean.move_students()
        self.dean.place_students(new_students)
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
        self.canvas = None

    def set_canvas(self, canvas):
        self.canvas = canvas

    def get_canvas_size(self):
        return self.canvas.winfo_width(), self.canvas.winfo_height()

    def get_students_count(self):
        return len(self.students)

    def enroll_student(self, student):
        student.set_idx(len(self.students) + 1)
        self.students.append(student)

    def get_grid(self):
        col_count = self.get_canvas_size()[0] // Student.win_width
        if col_count == 0:
            col_count = 1
        row_count = math.ceil(self.get_students_count() / col_count)
        grid = []
        for col in [[(row, col) for row in range(row_count)] for col in range(col_count)]:
            grid.extend(col)
        self.canvas.config(scrollregion=(0, 0, col_count * Student.win_width, row_count * Student.win_height))
        return grid

    def place_students(self, new_students):
        grid = self.get_grid()
        for (stud, coord) in list(zip(self.students, grid))[-len(new_students):]:
            stud.place(coord)

    def move_students(self):
        grid = self.get_grid()
        for (stud, coord) in zip(self.students, grid):
            stud.move_frame(coord)

    def update_students_idx(self):
        for student, idx in zip(self.students, range(1, len(self.students) + 1)):
            student.set_idx(idx)

    def expel_student(self, stud):
        stud.stud_fr.destroy()
        self.students.remove(stud)
        self.update_students_idx()
        self.move_students()

    def expel_all_students(self):
        while self.students:
            self.expel_student(self.students[-1])

    def get_students_names(self):
        return [student.name for student in self.students]


class Student:
    lab_width = 3  # in letter
    ent_width = 20  # in letter
    win_width = 250  # in px
    win_height = 20  # in px

    def __init__(self, name, dean, parent=None):
        self.name = name
        self.dean = dean
        self.idx = IntVar()
        self.parent = parent
        self.ent = None
        self.stud_fr = None
        self.cur_coord = None

    def set_idx(self, idx):
        self.idx.set(idx)

    def get_idx(self):
        return self.idx.get()

    def place(self, coord):
        stud_fr = Frame(self.parent)
        stud_fr.pack(side=TOP)
        Label(stud_fr, textvariable=self.idx, width=self.lab_width).pack(side=LEFT, anchor=W)
        Button(stud_fr, text='x', command=lambda: self.dean.expel_student(self)).pack(side=RIGHT, anchor=E)
        ent = Entry(stud_fr, width=self.ent_width, font=1)
        ent.pack(side=LEFT)
        ent.insert(0, self.name)
        ent.bind('<KeyPress>', self.change_name)
        self.stud_fr_win = self.parent.create_window(
            coord[1] * self.win_width, coord[0] * self.win_height, anchor=NW, window=stud_fr,
            width=self.win_width, height=self.win_height)
        self.ent = ent
        self.stud_fr = stud_fr
        self.cur_coord = coord

    def set_font_color(self, color):
        self.ent.config(fg=color)

    def change_name(self, event):
        if event.keysym == 'Return':
            new_name = self.ent.get()
            self.name = new_name
            return
        self.ent.event_generate('<Return>', when='tail')

    def move_frame(self, new_coord):
        if self.cur_coord:
            diff_x = (new_coord[1] - self.cur_coord[1]) * self.win_width
            diff_y = (new_coord[0] - self.cur_coord[0]) * self.win_height
            self.parent.move(self.stud_fr_win, diff_x, diff_y)
            self.cur_coord = new_coord


if __name__ == '__main__':
    root = Tk()
    #root.resizable(width=FALSE, height=FALSE)
    #root.wm_geometry("")
    root.title('GroupsMaker')
    width, height = root.maxsize()
    root.geometry('%sx%s' % (round(0.25 * width), round(0.25 * height)))
    Univercity(root).pack(side=TOP, expand=YES, fill=BOTH)
    root.mainloop()

