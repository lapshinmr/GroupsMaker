from tkinter import *
from combsmath import molder, unique_sorter


class NamesBox(Frame):
    def __init__(self, parent=None, names=(), consumer=None, remove=True, comb_size=1):
        Frame.__init__(self, parent)
        self.names = names
        self.consumer = consumer
        self.listbox = None
        self.remove = remove
        self.comb_size = comb_size
        self.show()

    def get_names(self):
        return self.names

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
        packed = molder(self.names, self.comb_size)
        print(packed)
        self.names = list(unique_sorter(packed, self.comb_size))
        print(self.names)
        for comb in sorted(self.names):
            self.listbox.insert(END, ', '.join(comb))

    def pop(self):
        try:
            select_idx = self.listbox.curselection()
            comb = tuple(self.listbox.get(select_idx).split(', '))
            if self.remove:
                self.listbox.delete(select_idx)
                self.names.remove(comb)
        except TclError as e:
            print('Listbox is empty (%s)' % e.__class__.__name__)
        else:
            if not self.consumer:
                return
            try:
                last_name = self.consumer.names[-1]
            except IndexError:
                self.consumer.names.append(comb)
                self.consumer.fill()
            else:
                if comb not in last_name:
                    self.consumer.names.append(comb)
                    self.consumer.fill()


class ListsEditor(Frame):
    def __init__(self, parent=None, name='', names=(), whitelist=(), blacklist=(), combs_size=1):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack(side=TOP, expand=YES, fill=BOTH)
        self.name = name
        self.names = self.prepare_names(names)
        self.whitelist = self.prepare_exclist(whitelist)
        self.blacklist = self.prepare_exclist(blacklist)
        self.combs_size = combs_size
        self.selector = BooleanVar()
        self.main_listbox = None
        self.white_listbox = None
        self.black_listbox = None
        self.listbox = None
        self.make_widgets()

    def prepare_names(self, names):
        names.remove(self.name)
        return list(zip(names))

    def prepare_exclist(self, exclist):
        out_list = []
        for comb in exclist:
            comb = list(comb)
            comb.remove(self.name)
            out_list.append(tuple(comb))
        return out_list

    def make_widgets(self):
        self.show_name()
        self.show_names()
        self.show_lists_buttons()
        self.show_exclists()
        self.show_accept()

    def show_name(self):
        Label(self, text=self.name).pack(side=TOP, fill=X)

    def show_names(self):
        self.main_listbox = NamesBox(self, self.names, remove=False)
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
        self.white_listbox = NamesBox(exclists_fr, self.whitelist, self.main_listbox, comb_size=self.combs_size - 1)
        self.white_listbox.pack(side=LEFT, expand=YES, fill=BOTH)
        self.black_listbox = NamesBox(exclists_fr, self.blacklist, self.main_listbox, comb_size=self.combs_size - 1)
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

    def get_names(self):
        return self.main_listbox.get_names()

    def get_whitelist(self):
        return self.white_listbox.get_names()

    def get_blacklist(self):
        return self.black_listbox.get_names()

if __name__ == '__main__':
    ListsEditor(None,
                'misha',
                ['misha', 'kate', 'yula', 'dasha', 'sasha', 'serega'],
                combs_size=3
                ).mainloop()


