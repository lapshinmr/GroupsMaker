from tkinter import *
from PIL import Image, ImageTk


class EntryPM(Frame):
    def __init__(self, parent=None, path_dec=None, path_inc=None):
        """
        :param parent:
        :param path_inc: path to image for button that increment count
        :param path_dec: path to image for button that decrement count
        """
        Frame.__init__(self, parent)
        self.ent = None
        self.path_dec = path_dec
        self.path_inc = path_inc
        self.count = IntVar()
        self.count.set(1)
        self.add_widgets()

    def add_widgets(self):
        if self.path_inc:
            self.path_inc = ImageTk.PhotoImage(Image.open(self.path_inc))
            but_inc = Button(self, image=self.path_inc, command=self.inc_count)
        else:
            but_inc = Button(self, text='+', command=self.inc_count)
        but_inc.pack(side=RIGHT)
        ent = Entry(self, justify=CENTER, width=6, textvariable=self.count)
        ent.pack(side=RIGHT, expand=YES, fill=BOTH)
        self.ent = ent
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


if __name__ == '__main__':
    root = Tk()
    EntryPM(root).pack(side=TOP)
    root.mainloop()
