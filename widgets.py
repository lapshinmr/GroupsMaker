from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


class EntryPM(Frame):
    start_count = 1

    def __init__(self, parent=None, labeltext='', path_dec=None, path_inc=None):
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


class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None
        self.id = None
        self.x = 0
        self.y = 0
        self.text = None

    def showtip(self, text):
        self.text = text
        if self.tip_window or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tip_window = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT, background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()


def create_tool_tip(widget, text):
    tool_tip = ToolTip(widget)

    def enter(event):
        tool_tip.showtip(text)

    def leave(event):
        tool_tip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


if __name__ == '__main__':
    root = Tk()
    EntryPM(root, labeltext='text').pack(side=TOP)
    root.mainloop()
