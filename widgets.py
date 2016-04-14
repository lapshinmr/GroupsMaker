from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


class EntryPM(Frame):
    def __init__(self, parent=None, labeltext='', start_count=1, path_dec=None, path_inc=None):
        """
        :param parent:
        :param path_inc: path to image for button that increment count
        :param path_dec: path to image for button that decrement count
        """
        Frame.__init__(self, parent)
        self.parent = parent
        self.labeltext = labeltext
        self.ent = None
        self.path_dec = path_dec
        self.path_inc = path_inc
        self.start_count = start_count
        self.count = IntVar()
        self.count.set(self.start_count)
        self.add_widgets()

    def add_widgets(self):
        # LABEL
        lab_fr = Frame(self)
        lab_fr.pack(side=TOP, fill=X, expand=YES)
        Frame(lab_fr, width=5).pack(side=LEFT)
        ttk.Separator(lab_fr).pack(side=LEFT, fill=X, expand=YES)
        Label(lab_fr, text=self.labeltext, pady=0).pack(side=LEFT)
        ttk.Separator(lab_fr).pack(side=LEFT, fill=X, expand=YES)
        Frame(lab_fr, width=5).pack(side=LEFT)
        # FRAME for BUTTON and ENTRY
        ent_but_fr = Frame(self)
        ent_but_fr.pack(side=BOTTOM)
        ent_but_fr.config(pady=0)
        # MINUS BUTTON
        if self.path_inc:
            self.path_inc = ImageTk.PhotoImage(Image.open(self.path_inc))
            but_inc = Button(self, image=self.path_inc, command=self.inc_count)
        else:
            but_inc = Button(self, text='+', command=self.inc_count)
        but_inc.pack(side=RIGHT)
        # ENTRY
        ent = Entry(self, justify=CENTER, width=6, textvariable=self.count)
        ent.pack(side=RIGHT, expand=YES, fill=BOTH)
        self.ent = ent
        # PLUS BUTTON
        if self.path_dec:
            self.path_dec = ImageTk.PhotoImage(Image.open(self.path_dec))
            but_dec = Button(self, image=self.path_dec, command=self.dec_count)
        else:
            but_dec = Button(self, text='-', command=self.dec_count)
        but_dec.pack(side=LEFT)

    def inc_count(self):
        try:
            cur_count = self.count.get()
        except ValueError:
            print('Please, input a integer number')
        else:
            self.count.set(cur_count + 1)

    def dec_count(self):
        try:
            cur_count = self.count.get()
        except ValueError:
            print('Please, input a integer number')
        else:
            if cur_count > 1:
                self.count.set(cur_count - 1)

    def get(self):
        cur_count = self.count.get()
        if not isinstance(cur_count, int):
            cur_count = 1
        return cur_count


class Tip:
    cursor_width = 10
    cursor_height = 10

    def __init__(self, parent, tip=None):
        if tip:
            self.tip_text = tip
            self.tip_win = None
            self.x = None
            self.y = None
            self.bind('<Leave>', lambda event: self.hidetip())
            self.bind('<Motion>', lambda event: self.showtip())

    def showtip(self):
        self.x, self.y = self.winfo_pointerx() + self.cursor_width, self.winfo_pointery() + self.cursor_height
        if not self.tip_win and self.tip_text:
            self.tip_win = Toplevel(self)
            self.tip_win.wm_overrideredirect(True)
            label = Label(self.tip_win, text=self.tip_text, justify=LEFT, background="#ffffe0", relief=SOLID,
                          borderwidth=1, font=("tahoma", "8", "normal"))
            label.pack(ipadx=1)
        self.tip_win.wm_geometry("+%d+%d" % (self.x, self.y))

    def hidetip(self):
        if self.tip_win:
            self.tip_win.destroy()
            self.tip_win = None


class TipButton(Button, Tip):
    def __init__(self, parent, tip=None, **kwargs):
        Button.__init__(self, parent, **kwargs)
        Tip.__init__(self, parent, tip)


class TipCheckbutton(Checkbutton, Tip):
    def __init__(self, parent, tip=None, **kwargs):
        Checkbutton.__init__(self, parent, **kwargs)
        Tip.__init__(self, parent, tip)


class TipLabel(Label, Tip):
    def __init__(self, parent, tip=None, **kwargs):
        Label.__init__(self, parent, **kwargs)
        Tip.__init__(self, parent, tip)


if __name__ == '__main__':
    root = Tk()
    tt = TipButton(root, tip='tip', text='push me', command=root.quit)
    print(tt.__dict__)
    tt.pack()
    root.mainloop()
