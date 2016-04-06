from tkinter import *


class NamesBox(Frame):
    def __init__(self, parent, names, consumer=None):
        Frame.__init__(self, parent)
        self.names = list(names)
        self.consumer = consumer
        self.listbox = None
        self.show()

    def connect(self, consumer):
        self.consumer = consumer

    def show(self):
        self.listbox = Listbox(self)
        sbar = Scrollbar(self)
        sbar.config(command=self.listbox.yview)
        sbar.pack(side=RIGHT, fill=Y)
        self.listbox.config(yscrollcommand=sbar.set)
        self.listbox.pack(side=LEFT, expand=YES, fill=BOTH)
        self.listbox.bind('<Double-1>', lambda event: self.pop())
        self.fill()

    def fill(self):
        self.listbox.delete(0, END)
        for name in self.names:
            self.listbox.insert(END, name)

    def pop(self):
        try:
            select_idx = self.listbox.curselection()
            name = self.listbox.get(select_idx)
            self.listbox.delete(select_idx)
            self.names.remove(name)
        except TclError as e:
            print('Listbox is empty (%s)' % e.__class__.__name__)
        else:
            if self.consumer:
                self.consumer.names.append(name)
                self.consumer.fill()


class ListsEditor(Frame):
    def __init__(self, parent=None, name='', names=(), whitelist=(), blacklist=()):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack(side=TOP, expand=YES, fill=BOTH)
        self.name = name
        self.names = names.remove(name) if name in names else names
        self.whitelist = whitelist
        self.blacklist = blacklist
        self.selector = BooleanVar()
        self.main_listbox = None
        self.white_listbox = None
        self.black_listbox = None
        self.listbox = None
        self.make_widgets()

    def make_widgets(self):
        self.show_name()
        self.show_names()
        self.show_lists_buttons()
        self.show_exclists()
        self.show_accept()

    def show_name(self):
        Label(self, text=self.name).pack(side=TOP, fill=X)

    def show_names(self):
        self.main_listbox = NamesBox(self, self.names)
        self.main_listbox.pack(side=TOP, expand=YES, fill=BOTH)

    def show_lists_buttons(self):
        lists_buttons_fr = Frame(self)
        lists_buttons_fr.pack(side=TOP, fill=X)
        Radiobutton(lists_buttons_fr, text='white', command=self.connect_to_exclist, variable=self.selector, value=0
                    ).pack(side=LEFT, expand=YES, fill=X)
        Radiobutton(lists_buttons_fr, text='black', command=self.connect_to_exclist, variable=self.selector, value=1
                    ).pack(side=RIGHT, expand=YES, fill=X)

    def show_exclists(self):
        exclists_fr = Frame(self)
        exclists_fr.pack(side=TOP, expand=YES, fill=BOTH)
        self.white_listbox = NamesBox(exclists_fr, self.whitelist, self.main_listbox)
        self.white_listbox.pack(side=LEFT, expand=YES, fill=BOTH)
        self.black_listbox = NamesBox(exclists_fr, self.blacklist, self.main_listbox)
        self.black_listbox.pack(side=LEFT, expand=YES, fill=BOTH)
        self.selector.set(0)
        self.main_listbox.connect(self.white_listbox)

    def show_accept(self):
        Button(self, text='Accept', command=self.accept).pack(side=BOTTOM, fill=X)

    def connect_to_exclist(self):
        if self.selector.get() == 1:
            self.main_listbox.connect(self.black_listbox)
        else:
            self.main_listbox.connect(self.white_listbox)

    def accept(self):
        self.parent.destroy() if self.parent else self.quit()


if __name__ == '__main__':
    ListsEditor(None, 'misha', ('kate', 'yula', 'dasha'), ('serega',), ('sasha',)).mainloop()

