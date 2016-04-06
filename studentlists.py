from tkinter import *
from widgets import TipButton


class NamesBox(Frame):
    def __init__(self, parent, names):
        Frame.__init__(self, parent)
        self.names = list(names)
        self.other_names_box = None
        self.listbox = None
        self.show()

    def connect(self, other_names_box):
        self.other_names_box = other_names_box

    def show(self):
        self.listbox = Listbox(self)
        sbar = Scrollbar(self)
        sbar.config(command=self.listbox.yview)
        sbar.pack(side=RIGHT, fill=Y)
        self.listbox.config(yscrollcommand=sbar.set)
        self.listbox.pack(side=LEFT, expand=YES, fill=BOTH)
        self.listbox.bind('<Double-1>', self.pop)
        self.listbox.bind('<Double-3>', self.pop)
        self.fill()

    def fill(self):
        self.listbox.delete(0, END)
        for name in self.names:
            self.listbox.insert(END, name)

    def add(self, name):
        self.names.append(name)
        self.fill()

    def pop(self):
        try:
            select_idx = self.listbox.curselection()
            name = self.listbox.get(select_idx)
            self.listbox.delete(select_idx)
            self.names.remove(name)
        except TclError as e:
            print('Listbox is empty (%s)' % e.__class__.__name__)
        else:
            return name


class ListsEditor(Frame):
    def __init__(self, parent=None, name='', names=(), whitelist=(), blacklist=()):
        Frame.__init__(self, parent)
        self.pack()
        # INPUT DATA
        self.parent = parent
        self.name = name
        self.names = names
        self.whitelist = whitelist
        self.blacklist = blacklist
        if self.name in names:
            names.remove(self.name)
        # FRAMES
        self.name_fr = None
        self.names_fr = None
        self.exclists_fr = None
        self.listbox = None
        # DRAW WIDGETS
        self.make_widgets()

    def make_widgets(self):
        self.show_name()
        self.show_names()
        self.show_lists_buttons()
        self.show_exclists()
        self.show_accept()

    def show_name(self):
        name_fr = Frame(self)
        name_fr.pack(side=TOP, expand=YES, fill=X)
        Label(name_fr, text=self.name).pack(side=TOP, expand=YES, fill=X)

    def show_names(self):
        names_fr = Frame(self)
        names_fr.pack(side=TOP, expand=YES, fill=BOTH)
        self.names = NamesBox(names_fr, self.names)
        self.names.pack(side=TOP, expand=YES, fill=BOTH)

    def show_lists_buttons(self):
        lists_buttons_fr = Frame(self)
        lists_buttons_fr.pack(side=TOP, expand=YES, fill=X)
        Button(lists_buttons_fr, text='white', command=lambda: 0).pack(side=LEFT, expand=YES, fill=X)
        Button(lists_buttons_fr, text='black', command=lambda: 0).pack(side=RIGHT, expand=YES, fill=X)

    def show_exclists(self):
        exclists_fr = Frame(self)
        exclists_fr.pack(side=TOP, expand=YES, fill=BOTH)
        NamesBox(exclists_fr, self.whitelist).pack(side=LEFT, expand=YES, fill=BOTH)
        NamesBox(exclists_fr, self.blacklist).pack(side=LEFT, expand=YES, fill=BOTH)

    def show_accept(self):
        accept_fr = Frame(self)
        accept_fr.pack(side=BOTTOM, expand=YES, fill=X)
        Button(accept_fr, text='Accept', command=self.accept).pack(side=BOTTOM, expand=YES, fill=X)

    def accept(self):
        if self.parent is None:
            self.quit()
        else:
            self.parent.destroy()


if __name__ == '__main__':
    ListsEditor(None, 'misha', ('kate', 'yula', 'dasha'), ('serega',), ('sasha',)).mainloop()

