from tkinter import *


class WhiteList:
    def __init__(self, name, names):
        self.name = name
        self.names = names


class BlackList:
    def __init__(self, name, names):
        self.name = name
        self.names = names


class ListsEditor(Frame):
    def __init__(self, name='', names=(), whitelist=(), blacklist=(), parent=None):
        Frame.__init__(self, parent)
        self.name = StringVar()
        self.name.set(name)
        self.names = names
        self.whitelist = whitelist
        self.blacklist = blacklist
        self.exclude_lists = {'White': [], 'Black': []}
        self.cur_exclist = StringVar()
        self.cur_exclist.set('White')
        self.listbox = None
        self.whitelist = None
        self.blacklist = None
        self.make_widgets()

    def make_widgets(self):
        self.add_name()
        self.add_choice()
        self.add_listbox()
        self.add_exclists()
        self.add_buttons()

    def add_name(self):
        Label(self, textvariable=self.name, bd=2, relief=RIDGE).pack(side=TOP, fill=X)

    def add_choice(self):
        radio_fr = Frame(self)
        radio_fr.pack(side=TOP, fill=X)
        Radiobutton(radio_fr, text='White', variable=self.cur_exclist, value=self.whitelist).pack(
            side=LEFT, expand=YES, fill=X)
        Radiobutton(radio_fr, text='Black', variable=self.cur_exclist, value=self.blacklist).pack(
            side=RIGHT, expand=YES, fill=X)

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
        whitelist = Frame(exclists)
        blacklist = Frame(exclists)
        whitelist.pack(side=LEFT, expand=YES, fill=BOTH)
        blacklist.pack(side=LEFT, expand=YES, fill=BOTH)
        for exclist_name, exclist in self.exclude_lists.items():
            for name in exclist:
                if exclist_name == 'White':
                    Label(whitelist, text=name).pack(side=TOP, fill=X)
                else:
                    Label(blacklist, text=name).pack(side=TOP, fill=X)
        self.whitelist = whitelist
        self.blacklist = blacklist

    def append_exlist(self):
        cur_exclist = self.cur_exclist.get()
        select_idx = self.listbox.curselection()
        select_name = self.listbox.get(select_idx)
        self.exclude_lists[self.cur_exclist.get()].append(select_name)
        if cur_exclist == 'White':
            self.listbox.delete(select_idx)
            Label(self.whitelist, text=select_name).pack(side=TOP, fill=X)
        else:
            self.listbox.delete(select_idx)
            Label(self.blacklist, text=select_name).pack(side=TOP, fill=X)

    def add_buttons(self):
        Button(self, text='Add', command=self.append_exlist).pack(side=LEFT, expand=YES, fill=X)
        Button(self, text='Accept', command=self.destroy).pack(side=RIGHT, expand=YES, fill=X)

