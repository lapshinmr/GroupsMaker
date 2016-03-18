import os
from tkinter import *
from groups_maker import GroupsMaker
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import *
from gm_exceptions import *
from imglib import ImageHandler
from tkinter import ttk
import math
from PIL import Image, ImageTk
from widgets import EntryPM


imgdir = 'pict'


class University(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.duration = None
        self.size_group = IntVar()
        self.input_names = None
        self.stud_canv = None
        self.tt = None
        self.ttcanv = None
        self.paned_win = None
        self.dean = Dean()
        self.imghand = ImageHandler('pict')
        self.add_widgets()
        self.timetable = []

    def add_widgets(self):
        self.add_menu()
        self.add_toolbar()
        self.paned_win = PanedWindow(self, orient=VERTICAL)
        self.paned_win.pack(side=TOP, fill=BOTH, expand=YES)
        self.add_input_field()
        self.add_canvas()
        self.add_timetable()

    def add_menu(self):
        top = Menu(self.parent)
        self.parent.config(menu=top)
        file = Menu(top, tearoff=False)
        file.add_command(label='Load names', command=self.open_names_from_file,  underline=0)
        file.add_command(label='Save names', command=self.save_names_as_text,  underline=0)
        file.add_command(label='Save timetable', command=self.save_calendar_as_plain_text)
        file.add_command(label='Quit', command=self.quit, underline=1)
        top.add_cascade(label='File', menu=file, underline=0)

    def add_toolbar(self):
        but_frame = Frame(self)
        but_frame.pack(side=TOP, fill=X)
        self.add_img = ImageTk.PhotoImage(Image.open(self.imghand.get('enroll')))
        self.clean_img = ImageTk.PhotoImage(Image.open(self.imghand.get('expel_all')))
        self.timetable_img = ImageTk.PhotoImage(Image.open(self.imghand.get('tt')))
        self.quit_img = ImageTk.PhotoImage(Image.open(self.imghand.get('quit')))
        self.save_tt = ImageTk.PhotoImage(Image.open(self.imghand.get('save_tt')))
        Button(but_frame, image=self.add_img, command=self.add).pack(side=LEFT)
        Button(but_frame, image=self.clean_img, command=self.dean.expel_all_students).pack(side=LEFT)
        Button(but_frame, image=self.timetable_img, command=self.show_timetable).pack(side=LEFT)
        Button(but_frame, image=self.save_tt, command=self.save_calendar_as_plain_text).pack(side=LEFT)
        Button(but_frame, image=self.quit_img, command=self.quit).pack(side=RIGHT)

        self.size_group = EntryPM(
            but_frame, 'size', self.imghand.get('minus', img_size=24), self.imghand.get('plus', img_size=24))
        self.size_group.pack(side=RIGHT)

        self.duration = EntryPM(
            but_frame, 'lessons', self.imghand.get('minus', img_size=24), self.imghand.get('plus', img_size=24))
        self.duration.pack(side=RIGHT)

    def add_input_field(self):
        ent_frame = LabelFrame(self.paned_win, text='input names here', padx=5, pady=0)
        ent_frame.config(height=70)
        ent_frame.pack(side=TOP, fill=X)
        ent_frame.pack_propagate(False)
        text = Text(ent_frame)
        scroll_bar = ttk.Scrollbar(ent_frame)
        scroll_bar.config(command=text.yview)
        text.config(yscrollcommand=scroll_bar.set)
        scroll_bar.pack(side=RIGHT, fill=Y)
        text.insert(1.0, '1, 2, 3, 4')
        text.pack(side=LEFT, expand=YES, fill=BOTH)
        text.focus()
        self.input_names = text
        self.paned_win.add(ent_frame)
        self.input_names.bind('<Return>', lambda event: self.add())

    def add_canvas(self):
        canv_frame = LabelFrame(self.paned_win, text='current names', padx=5, pady=0)
        canv_frame.pack(side=TOP, expand=YES, fill=BOTH)
        canv = Canvas(canv_frame, highlightthickness=0)
        canv.config(height=150)
        canv.bind('<Configure>', self.resize_canvas)
        sbar = ttk.Scrollbar(canv_frame)
        sbar.config(command=canv.yview)
        canv.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        canv.pack(side=LEFT, expand=YES, fill=BOTH)
        self.stud_canv = canv
        self.dean.set_canvas(self.stud_canv)
        self.paned_win.add(canv_frame)

    def resize_canvas(self, event):
        self.stud_canv.config(width=event.width, height=event.height)
        self.dean.move_students()

    def add_timetable(self):
        self.tt = LabelFrame(self.paned_win, text='timetable', padx=5, pady=0)
        self.tt.pack(side=LEFT, expand=YES, fill=BOTH)
        self.ttcanv = Canvas(self.tt)
        vsbar = ttk.Scrollbar(self.tt)
        hsbar = ttk.Scrollbar(self.tt)
        vsbar.config(command=self.ttcanv.yview, orient=VERTICAL)
        hsbar.config(command=self.ttcanv.xview, orient=HORIZONTAL)
        self.ttcanv.config(yscrollcommand=vsbar.set)
        self.ttcanv.config(xscrollcommand=hsbar.set)
        hsbar.pack(side=BOTTOM, fill=X)
        vsbar.pack(side=RIGHT, fill=Y)
        self.paned_win.add(self.tt)
        self.ttcanv.pack(side=TOP, expand=YES, fill=BOTH)

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
            new_stud = Student(stud_name, self.dean, self.stud_canv)
            self.dean.enroll_student(new_stud)
            new_students.append(new_stud)
        self.dean.move_students()
        self.dean.place_students(new_students)
        self.input_names.delete(1.0, END)
        self.dean.paint_dup_names()

    def gen_timetable(self):
        dups = self.dean.find_duplicates()
        if dups:
            showwarning('Warning', warnings['dups'])
            return
        duration = int(self.duration.get())
        size_group = int(self.size_group.get())
        students_names = self.dean.get_students_names()
        group = GroupsMaker(students_names, duration, size_group=size_group)
        try:
            self.timetable = group.get_timetable()
        except NotEnoughCombinations:
            showwarning('Warning', warnings['not_enough'])

    def show_timetable(self):
        les_fr_margin_x, les_fr_margin_y = 5, 5
        comb_margin_x, comb_margin_y = 10, 10
        les_fr_border_thikness = 2
        space_between_les = 5
        python_offset = 1
        left_corner_x, left_corner_y = 0, 0
        self.gen_timetable()
        self.ttcanv.delete('all')
        les_count = 0
        right_corner_x, right_corner_y = left_corner_x, left_corner_y
        for lesson in self.timetable:
            les_fr = Frame(self.ttcanv, bd=les_fr_border_thikness, relief=RIDGE,
                           padx=les_fr_margin_x, pady=les_fr_margin_y)
            les_fr.pack()
            les_lab = Label(les_fr, text='%s %s' % (les_count + python_offset, 'lesson'))
            les_lab.pack(side=TOP)
            sep = ttk.Separator(les_fr, orient=HORIZONTAL)
            sep.pack(side=TOP, fill=X)
            les_count += 1
            for combs in lesson:
                comb_fr = Frame(les_fr, padx=comb_margin_x, pady=comb_margin_y)
                comb_fr.pack(side=TOP)
                for name in combs:
                    lab = Label(comb_fr, text=name)
                    lab.pack(side=TOP)
            les_fr.update()
            self.ttcanv.create_window(right_corner_x, right_corner_y, window=les_fr, anchor=NW)
            right_corner_x += les_fr.winfo_width() + space_between_les
            self.ttcanv.config(scrollregion=(0, 0, right_corner_x, les_fr.winfo_height()))

    def generate_txt(self):
        text = ''
        lesson_count = 1
        for lesson in self.timetable:
            text += '%s неделя: ' % lesson_count
            lesson_count += 1
            for combs in lesson:
                text += ('(' + ', '.join(list(combs)) + ') ')
            text += '\n'
        return text

    def generate_tex(self):
        start = (
            r'\documentclass[a4paper]{article}' + '\n'
            r'\usepackage[landscape]{geometry}' + '\n'
            r'\usepackage[utf8]{inputenc}' + '\n'
            r'\usepackage[russian]{babel}' + '\n'
            r'\begin{document}' + '\n'
            r'\thispagestyle{empty}' + '\n'
            r'\mbox{}' + '\n'
            r'\vfill' + '\n'
            r'\begin{center}' + '\n'
        )
        end = (
            r'\end{center}' + '\n'
            r'\vfill' + '\n'
            r'\end{document}' + '\n'
        )
        main_table = r'\begin{tabular}'
        main_table += '{' + '|'.join('c' * (len(self.timetable[0]) + 1)) + r'}\hline'
        lesson_count = 1
        for lesson in self.timetable:
            main_table += str(lesson_count)
            lesson_count += 1
            for comb in lesson:
                main_table += '&' + r'\begin{tabular}{c}'
                main_table += r'\\'.join(list(comb))
                main_table += r'\end{tabular}'
            main_table += r'\\\hline' + '\n'
        main_table += r'\end{tabular}' + '\n'
        return start + main_table + end

    def save_calendar_as_plain_text(self):
        filename = asksaveasfilename(filetypes=[('txt', '.txt')])
        if filename:
            filename = os.path.splitext(filename)[0]
            open(filename + '.txt', 'w', encoding='utf-8').write(self.generate_txt())
            open(filename + '.tex', 'w', encoding='utf-8').write(self.generate_tex())


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

    def get_students_names(self):
        return [student.get_name() for student in self.students]

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
        self.paint_dup_names()

    def expel_all_students(self):
        while self.students:
            self.expel_student(self.students[-1])

    def find_duplicates(self):
        dups = {}
        for name in self.get_students_names():
            if name in dups:
                dups[name] += 1
            else:
                dups[name] = 1
        name_to_remove = []
        for name, count in dups.items():
            if count == 1:
                name_to_remove.append(name)
        for name in name_to_remove:
            del dups[name]
        return dups

    def paint_dup_names(self):
        dups = self.find_duplicates()
        for student in self.students:
            if student.get_name() in dups:
                student.set_font_color('red')
            else:
                student.set_font_color('black')


class Student:
    lab_width = 3  # in letter
    ent_width = 20  # in letter
    win_width = 250  # in px
    win_height = 26  # in px

    def __init__(self, name, dean, parent=None):
        self.dean = dean
        self.name = StringVar()
        self.set_name(name)
        self.name.trace('w', self.check_dups)
        self.idx = IntVar()
        self.parent = parent
        self.ent = None
        self.stud_fr = None
        self.cur_coord = None
        self.imghand = ImageHandler('pict')

    def set_idx(self, idx):
        self.idx.set(idx)

    def get_idx(self):
        return self.idx.get()

    def set_name(self, name):
        self.name.set(name)

    def get_name(self):
        return self.name.get()

    def place(self, coord):
        stud_fr = Frame(self.parent)
        stud_fr.pack(side=TOP)
        Label(stud_fr, textvariable=self.idx, width=self.lab_width).pack(side=LEFT, anchor=W)
        self.expel_img = ImageTk.PhotoImage(Image.open(self.imghand.get('expel', img_size=20)))
        Button(stud_fr, image=self.expel_img, command=lambda: self.dean.expel_student(self)).pack(side=RIGHT, anchor=E)
        self.ent = Entry(stud_fr, textvariable=self.name, width=self.ent_width, font=1)
        self.ent.pack(side=LEFT)
        self.stud_fr_win = self.parent.create_window(
            coord[1] * self.win_width, coord[0] * self.win_height, anchor=NW, window=stud_fr,
            width=self.win_width, height=self.win_height)
        self.stud_fr = stud_fr
        self.cur_coord = coord

    def set_font_color(self, color):
        self.ent.config(fg=color)

    def check_dups(self, *args):
        self.dean.paint_dup_names()

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
    root.geometry('%sx%s' % (round(0.35 * width), round(0.5 * height)))
    University(root).pack(side=TOP, expand=YES, fill=BOTH)
    root.mainloop()

