from tkinter import *


class ListsEditor(Frame):
    def __init__(self, name='', names=(), whitelist=(), blacklist=(), parent=None):
        Frame.__init__(self, parent)
        self.pack()
        self.name = StringVar()
        self.name.set(name)
        self.names = names
        self.whitelist = list(whitelist)
        self.blacklist = list(blacklist)
        self.cur_exclist = BooleanVar()
        self.cur_exclist.set(0)
        self.listbox = None
        self.whitelist_fr = None
        self.blacklist_fr = None
        self.make_widgets()

    def make_widgets(self):
        self.add_name()
        self.add_listbox()
        self.add_choice()
        self.add_exclists()
        self.add_buttons()

    def add_name(self):
        Label(self, textvariable=self.name, bd=2, relief=RIDGE).pack(side=TOP, fill=X)

    def add_choice(self):
        radio_fr = Frame(self)
        radio_fr.pack(side=TOP, fill=X)
        Radiobutton(radio_fr, text='Whitelist', variable=self.cur_exclist, value=0,
                    command=lambda: self.cur_exclist.set(0)).pack(side=LEFT, expand=YES, fill=X)
        Radiobutton(radio_fr, text='Blacklist', variable=self.cur_exclist, value=1,
                    command=lambda: self.cur_exclist.set(1)).pack(side=RIGHT, expand=YES, fill=X)

    def add_listbox(self):
        list_fr = Frame(self)
        list_fr.pack(side=TOP, expand=YES, fill=BOTH)
        listbox = Listbox(list_fr)
        sbar = Scrollbar(list_fr)
        sbar.pack(side=RIGHT, fill=Y)
        sbar.config(command=listbox.yview)
        listbox.config(yscrollcommand=sbar.set)
        listbox.pack(side=LEFT, expand=YES, fill=BOTH)
        for name in self.names:
            if name != self.name.get():
                listbox.insert(END, name)
        self.listbox = listbox

    def add_exclists(self):
        but_fr = Frame(self)
        but_fr.pack(side=BOTTOM, fill=X)
        exclists = Frame(self)
        exclists.pack(side=TOP, expand=YES, fill=BOTH)
        whitelist_fr = Frame(exclists)
        blacklist_fr = Frame(exclists)
        whitelist_fr.pack(side=LEFT, expand=YES, fill=BOTH)
        blacklist_fr.pack(side=LEFT, expand=YES, fill=BOTH)
        for name in self.whitelist:
            Label(whitelist_fr, text=name).pack(side=TOP, fill=X)
        for name in self.blacklist:
            Label(blacklist_fr, text=name).pack(side=TOP, fill=X)
        self.whitelist_fr = whitelist_fr
        self.blacklist_fr = blacklist_fr

    def append_exclist(self):
        try:
            select_idx = self.listbox.curselection()
            select_name = self.listbox.get(select_idx)
        except TclError as e:
            print('Listbox is empty (%s)' % e.__class__.__name__)
        else:
            self.listbox.delete(select_idx)
            if not self.cur_exclist.get():
                self.whitelist.append(select_name)
                Label(self.whitelist_fr, text=select_name).pack(side=TOP, fill=X)
            else:
                self.blacklist.append(select_name)
                Label(self.blacklist_fr, text=select_name).pack(side=TOP, fill=X)

    def add_buttons(self):
        Button(self, text='Add', command=self.append_exclist).pack(side=LEFT, expand=YES, fill=X)
        Button(self, text='Accept', command=self.quit).pack(side=RIGHT, expand=YES, fill=X)

if __name__ == '__main__':
    ListsEditor('misha', ('kate', 'yula', 'dasha'), ('serega',), ('sasha',)).mainloop()

