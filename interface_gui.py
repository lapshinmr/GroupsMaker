import os
import math
from groups_maker import GroupsMaker
from studentlists import *
from interface_functions import *
from gm_exceptions import *
from widgets import EntryPM, TipButton
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import *
from imglib import ImageHandler
from PIL import Image, ImageTk
from tkinter import ttk


imgdir = 'pict'


class University(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.duration = None
        self.size_group = IntVar()
        self.input_names = None
        self.stcanv = None
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
        TipButton(but_frame, image=self.add_img, tip='Add student(s)', command=self.add).pack(side=LEFT)
        TipButton(but_frame, image=self.clean_img, tip='Expel student(s)', command=self.dean.expel_all_students).pack(side=LEFT)
        TipButton(but_frame, image=self.timetable_img, tip='Generate timetable', command=self.show_timetable).pack(side=LEFT)
        TipButton(but_frame, image=self.save_tt, tip='Save timetable', command=self.save_calendar_as_plain_text).pack(side=LEFT)
        TipButton(but_frame, image=self.quit_img, tip='Quit', command=self.quit).pack(side=RIGHT)
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
        scroll_bar = Scrollbar(ent_frame)
        scroll_bar.config(command=text.yview)
        text.config(yscrollcommand=scroll_bar.set)
        scroll_bar.pack(side=RIGHT, fill=Y)
        text.insert(1.0, '1, 2, 3, 4')
        text.pack(side=LEFT, expand=YES, fill=BOTH)
        text.focus()
        self.input_names = text
        self.paned_win.add(ent_frame)
        self.input_names.bind('<Return>', lambda event: self.add())
        self.input_names.bind('<Shift-Return>', lambda event: self.add_return())
        self.input_names.bind('<Enter>', lambda event: bind_scroll_canv(self.input_names))
        self.input_names.bind('<Leave>', lambda event: unbind_scroll_canv(self.input_names))

    def add_return(self):
        self.input_names.insert(END, '')

    def add_canvas(self):
        canv_frame = LabelFrame(self.paned_win, text='current names', padx=5, pady=0)
        canv_frame.pack(side=TOP, expand=YES, fill=BOTH)
        sbar = Scrollbar(canv_frame)
        sbar.pack(side=RIGHT, fill=Y)
        canv = Canvas(canv_frame, highlightthickness=0)
        canv.config(height=150)
        canv.bind('<Configure>', self.resize_canvas)
        canv.config(yscrollcommand=sbar.set)
        canv.pack(side=LEFT, expand=YES, fill=BOTH)
        canv.bind('<Enter>', lambda event: bind_scroll_canv(canv))
        canv.bind('<Leave>', lambda event: unbind_scroll_canv(canv))
        sbar.config(command=canv.yview)
        self.sbar = sbar
        self.stcanv = canv
        self.dean.set_canvas(self.stcanv)
        self.paned_win.add(canv_frame)

    def resize_canvas(self, event):
        self.stcanv.config(width=event.width, height=event.height)
        self.dean.move_students()

    def add_timetable(self):
        self.tt = LabelFrame(self.paned_win, text='timetable', padx=5, pady=0)
        self.tt.pack(side=LEFT, expand=YES, fill=BOTH)
        ttcanv = Canvas(self.tt)
        vsbar = Scrollbar(self.tt)
        hsbar = Scrollbar(self.tt)
        vsbar.config(command=ttcanv.yview, orient=VERTICAL)
        hsbar.config(command=ttcanv.xview, orient=HORIZONTAL)
        ttcanv.config(yscrollcommand=vsbar.set)
        ttcanv.config(xscrollcommand=hsbar.set)
        hsbar.pack(side=BOTTOM, fill=X)
        vsbar.pack(side=RIGHT, fill=Y)
        ttcanv.bind('<Enter>', lambda event: bind_scroll_canv(ttcanv, 'X'))
        ttcanv.bind('<Leave>', lambda event: unbind_scroll_canv(ttcanv))
        self.ttcanv = ttcanv
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
            new_stud = Student(stud_name, self.dean, self.stcanv)
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
        group = GroupsMaker(
            students_names, duration, size_group=size_group, whitelist=self.dean.whitelist, blacklist=self.dean.blacklist
        )
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
        nw_x, nw_y = 0, 0
        self.gen_timetable()
        self.ttcanv.delete('all')
        les_count = 0
        for part in self.timetable:
            for lesson in part:
                les_fr = Frame(self.ttcanv, bd=les_fr_border_thikness, relief=RIDGE,
                               padx=les_fr_margin_x, pady=les_fr_margin_y)
                les_fr.pack(expand=YES, fill=Y)
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
                les_fr.update_idletasks()
                self.ttcanv.create_window(nw_x, nw_y, window=les_fr, anchor=NW)
                nw_x += les_fr.winfo_width() + space_between_les
                les_height = les_fr.winfo_height()
                self.ttcanv.config(scrollregion=(0, 0, nw_x, les_height))
            self.ttcanv.create_line(nw_x, 0, nw_x, les_height, fill='red')
            nw_x += space_between_les

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
        self.whitelist = []
        self.blacklist = []

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

    def push_whitelist(self, name):
        whitelist = []
        for comb in self.whitelist:
            if name in comb:
                comb = list(comb)
                comb.remove(name)
                whitelist.extend(comb)
        return whitelist

    def push_blacklist(self, name):
        blacklist = []
        for comb in self.blacklist:
            if name in comb:
                comb = list(comb)
                comb.remove(name)
                blacklist.extend(comb)
        return blacklist

    def pull_whitelist(self, combs):
        for comb in combs:
            comb = sorted(comb)
            if tuple(comb) not in self.whitelist:
                self.whitelist.extend(combs)
        print('Whitelist in dean %s' % self.whitelist)

    def pull_blacklist(self, combs):
        for comb in combs:
            comb = sorted(comb)
            if tuple(comb) not in self.blacklist:
                self.blacklist.extend(combs)
        print('Blacklist in dean %s' % self.blacklist)


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

    def get_whitelist(self):
        return self.whitelist

    def get_blacklist(self):
        return self.blacklist

    def place(self, coord):
        stud_fr = Frame(self.parent)
        stud_fr.pack(side=TOP)
        Label(stud_fr, textvariable=self.idx, width=self.lab_width).pack(side=LEFT, anchor=W)
        self.expel_img = ImageTk.PhotoImage(Image.open(self.imghand.get('expel', img_size=20)))
        TipButton(stud_fr, image=self.expel_img, tip='delete', command=lambda: self.dean.expel_student(self)).pack(side=RIGHT, anchor=E)
        self.ent = Entry(stud_fr, textvariable=self.name, width=self.ent_width, font=1)
        self.ent.pack(side=LEFT)
        self.ent.bind('<Button-3>', lambda event: self.edit_exclist())
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

    def edit_exclist(self):
        class StLists(ListsEditor):
            def __init__(self, dean, parent=None, name='', names=(), whitelist=(), blacklist=()):
                ListsEditor.__init__(self, parent, name, names, whitelist, blacklist)
                self.dean = dean

            def accept_command(self):
                self.dean.pull_whitelist(self.get_whitelist_combs())
                self.dean.pull_blacklist(self.get_blacklist_combs())
                self.parent.destroy()

        editor_win = Toplevel()
        editor_win.title('Lists editor')
        names = self.dean.get_students_names()
        whitelist = self.dean.push_whitelist(self.name.get())
        blacklist = self.dean.push_blacklist(self.name.get())
        print('white: %s' % whitelist)
        print('black: %s' % blacklist)
        print('names: %s' % names)
        for name in whitelist + blacklist:
            names.remove(name)
        editor = StLists(self.dean, editor_win, name=self.name.get(), names=names, whitelist=whitelist, blacklist=blacklist)
        editor.pack()
        editor_win.focus_set()
        editor_win.wait_visibility(editor)
        editor_win.grab_set()
        editor_win.wait_window()


if __name__ == '__main__':
    root = Tk()
    #root.resizable(width=FALSE, height=FALSE)
    #root.wm_geometry("")
    root.title('GroupsMaker')
    width, height = root.maxsize()
    root.geometry('%sx%s' % (round(0.35 * width), round(0.5 * height)))
    University(root).pack(side=TOP, expand=YES, fill=BOTH)
    root.mainloop()

