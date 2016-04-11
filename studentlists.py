from tkinter import *
from combsmath import *


class NamesBox(Frame):
    def __init__(self, parent=None, combs=(), consumer=None, comb_size=1, role='consumer'):
        Frame.__init__(self, parent)
        self.combs = combs
        self.consumer = consumer
        self.consumers = [consumer]
        self.role = role
        self.comb_size = comb_size
        self.listbox = None
        self.show()

    def get_combs(self):
        return self.combs

    def connect(self, consumer):
        self.consumer = consumer

    def set_consumers(self, consumer_list):
        self.consumers = consumer_list

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
        self.combs = molder(self.combs, self.comb_size)
        self.combs = sort_combs_in_list(self.combs, dups=False)
        self.combs = remove_dup_combs(self.combs)
        for comb in self.combs:
            self.listbox.insert(END, ', '.join(comb))

    def pop(self):
        try:
            select_idx = self.listbox.curselection()
            comb = tuple(self.listbox.get(select_idx).split(', '))
            self.consumer.combs.append(comb)
            self.consumer.fill()
        except TclError as e:
            print('Listbox is empty (%s)' % e.__class__.__name__)
        else:
            if self.role == 'consumer':
                self.listbox.delete(select_idx)
                self.combs.remove(comb)
            else:
                names = unpack(self.combs)
                consumers_combs = []
                for consumer in self.consumers:
                    consumers_combs.extend(consumer.combs)
                used_names = get_used_items(names, consumers_combs, self.consumer.comb_size)
                while used_names:
                    name, *used_names = used_names
                    listbox_elements = self.listbox.get(0, END)
                    if name in listbox_elements:
                        name_idx = listbox_elements.index(name)
                        self.listbox.delete(name_idx)
                        self.combs.remove((name,))


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
        self.main_listbox = NamesBox(self, self.names, role='producer')
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
        self.main_listbox.set_consumers([self.white_listbox, self.black_listbox])

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


