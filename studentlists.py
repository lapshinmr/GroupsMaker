from tkinter import *
from widgets import TipButton


class ListsEditor(Frame):
    def __init__(self, parent=None, name='', names=(), whitelist=(), blacklist=()):
        Frame.__init__(self, parent)
        self.pack()
        # INPUT DATA
        self.parent = parent
        self.name = StringVar()
        self.name.set(name)
        self.names = list(names)
        if self.name in self.names:
            self.names.remove(self.name)
        self.white = list(whitelist)
        self.black = list(blacklist)
        # FRAMES
        self.name_fr = None
        self.names_fr = None
        self.exclists_fr = None
        self.white_fr = None
        self.black_fr = None
        self.listbox = None
        # DRAW WIDGETS
        self.make_widgets()

    def make_widgets(self):
        self.show_name()
        self.show_listbox()
        self.exclists = Frame(self)
        self.exclists.pack(side=TOP, expand=YES, fill=BOTH)
        self.white_fr = Frame(self.exclists)
        self.white_fr.pack(side=LEFT, expand=YES, fill=BOTH)
        self.show_white()
        self.black_fr = Frame(self.exclists)
        self.black_fr.pack(side=LEFT, expand=YES, fill=BOTH)
        self.show_black()
        self.show_accept()

    def show_name(self):
        self.name_fr = Frame(self.parent, bd=2, relief=RIDGE)
        self.name_fr.pack(side=TOP, expand=YES, fill=X)
        Label(self, textvariable=self.name).pack(side=TOP, expand=YES, fill=X)

    def show_listbox(self):
        self.names_fr = Frame(self, bd=2, relief=RIDGE)
        self.names_fr.pack(side=TOP, expand=YES, fill=BOTH)
        self.listbox = Listbox(self.names_fr)
        sbar = Scrollbar(self.names_fr)
        sbar.config(command=self.listbox.yview)
        sbar.pack(side=RIGHT, fill=Y)
        self.listbox.config(yscrollcommand=sbar.set)
        self.listbox.pack(side=LEFT, expand=YES, fill=BOTH)
        self.listbox.bind('<Double-1>', lambda event: self.white_add())
        self.listbox.bind('<Double-3>', lambda event: self.black_add())
        self.fill_listbox()

    def fill_listbox(self):
        self.listbox.delete(0, END)
        for name in self.names:
            self.listbox.insert(END, name)

    def listbox_pop(self):
        select_idx = self.listbox.curselection()
        name = self.listbox.get(select_idx)
        self.listbox.delete(select_idx)
        self.names.remove(name)
        return name

    def white_add(self):
        try:
            name = self.listbox_pop()
        except TclError as e:
            print('Listbox is empty (%s)' % e.__class__.__name__)
        else:
            self.white.append(name)
            self.show_white()

    def black_add(self):
        try:
            name = self.listbox_pop()
        except TclError as e:
            print('Listbox is empty (%s)' % e.__class__.__name__)
        else:
            self.black.append(name)
            self.show_black()

    def white_pop(self, event):
        name = event.widget.cget('text')
        self.white.remove(name)
        self.names.append(name)
        self.fill_listbox()
        event.widget.destroy()

    def show_white(self):
        ids = list(self.white_fr.children.keys())
        for id in ids:
            self.white_fr.children[id].destroy()
        for name in self.white:
            lab = Label(self.white_fr, text=name)
            lab.pack(side=TOP, fill=X)
            lab.bind('<Double-1>', self.white_pop)
        TipButton(self.white_fr, text='Whitelist', command=self.white_add,
                  tip='Press to add selected name to the whitelist. Or left double click on the selected name.'
                  ).pack(side=TOP, expand=YES, fill=X)

    def black_pop(self, event):
        name = event.widget.cget('text')
        self.black.remove(name)
        self.names.append(name)
        self.fill_listbox()
        event.widget.destroy()

    def show_black(self):
        ids = list(self.black_fr.children.keys())
        for id in ids:
            self.black_fr.children[id].destroy()
        for name in self.black:
            lab = Label(self.black_fr, text=name)
            lab.pack(side=TOP, fill=X)
            lab.bind('<Double-1>', self.black_pop)
        TipButton(self.black_fr, text='Blacklist', command=self.black_add,
                  tip='Press to add selected name to the blacklist. Or left double click on the selected name.'
                  ).pack(side=TOP, expand=YES, fill=X)

    def accept_command(self):
        if self.parent is None:
            self.quit()
        else:
            self.parent.destroy()

    def show_accept(self):
        Button(self, text='Accept', command=self.accept_command).pack(side=TOP, expand=YES, fill=X)

    def get_whitelist_combs(self):
        return [(self.name.get(), stud) for stud in self.white]

    def get_blacklist_combs(self):
        return [(self.name.get(), stud) for stud in self.black]


if __name__ == '__main__':
    ListsEditor(None, 'misha',('kate', 'yula', 'dasha'), ('serega',), ('sasha',)).mainloop()

