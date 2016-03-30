from tkinter import *


class ListsEditor(Frame):
    def __init__(self, parent=None, name='', names=(), whitelist=(), blacklist=()):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self.name = StringVar()
        self.name.set(name)
        self.names = list(names)
        self.whitelist = list(whitelist)
        self.blacklist = list(blacklist)
        self.listbox = None
        self.whitelist_fr = None
        self.blacklist_fr = None
        self.make_widgets()

    def make_widgets(self):
        self.add_name()
        self.add_listbox()
        self.add_exclists()
        self.add_choice()
        self.add_buttons()

    def add_name(self):
        Label(self, textvariable=self.name, bd=2, relief=RIDGE).pack(side=TOP, fill=X)

    def add_choice(self):
        radio_fr = Frame(self)
        radio_fr.pack(side=TOP, fill=X)
        Button(radio_fr, text='Whitelist', command=lambda: self.append_exclist(self.whitelist, 0)).pack(side=LEFT, expand=YES, fill=X)
        Button(radio_fr, text='Blacklist', command=lambda: self.append_exclist(self.blacklist, 1)).pack(side=RIGHT, expand=YES, fill=X)

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
            w_lab = Label(whitelist_fr, text=name)
            w_lab.pack(side=TOP, fill=X)
            w_lab.bind('<Double-1>', lambda event, exclist=self.whitelist: self.remove_name_from_exclist(event, exclist))
        for name in self.blacklist:
            b_lab = Label(blacklist_fr, text=name)
            b_lab.pack(side=TOP, fill=X)
            b_lab.bind('<Double-1>', lambda event, exclist=self.blacklist: self.remove_name_from_exclist(event, exclist))
        self.whitelist_fr = whitelist_fr
        self.blacklist_fr = blacklist_fr

    def append_exclist(self, exclist, list_type):
        try:
            select_idx = self.listbox.curselection()
            select_name = self.listbox.get(select_idx)
        except TclError as e:
            print('Listbox is empty (%s)' % e.__class__.__name__)
        else:
            self.listbox.delete(select_idx)
            self.names.remove(select_name)
            exclist.append(select_name)
            if not list_type:
                lab = Label(self.whitelist_fr, text=select_name)
            else:
                lab = Label(self.blacklist_fr, text=select_name)
            lab.pack(side=TOP, fill=X)
            lab.bind('<Double-1>', lambda event, exclist=exclist: self.remove_name_from_exclist(event, exclist))


    def remove_name_from_exclist(self, event, exclist):
        name = event.widget.cget('text')
        if name in exclist:
            exclist.remove(name)
            self.names.append(name)
        self.listbox.insert(END, name)
        event.widget.destroy()

    def accept_command(self):
        if self.parent is None:
            self.quit()
        else:
            self.parent.destroy()

    def add_buttons(self):
        Button(self, text='Accept', command=self.accept_command).pack(side=TOP, expand=YES, fill=X)

    def get_whitelist_combs(self):
        return [(self.name.get(), stud) for stud in self.whitelist]

    def get_blacklist_combs(self):
        return [(self.name.get(), stud) for stud in self.blacklist]


if __name__ == '__main__':
    ListsEditor(None, 'misha',('kate', 'yula', 'dasha'), ('serega',), ('sasha',)).mainloop()

