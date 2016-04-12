from tkinter import *
from combs_math import *


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
        self.listbox.bind('<Double-1>', lambda event: self.double_click_event())
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, END)
        for comb in self.combs:
            self.listbox.insert(END, ', '.join(comb))

    def remove_last_comb_if_dup(self):
        try:
            last_consumer_comb = self.consumer.combs[-1]
        except IndexError as e:
            print('Consumer has not any combs (%s)' % e.__class__.__name__)
        else:
            if self.get_consumers_combs().count(last_consumer_comb) > 1:
                self.consumer.combs.pop(-1)

    def update_combs(self):
        self.combs = molder(self.combs, self.comb_size)
        self.combs = sort_combs_in_list(self.combs, dups=False)
        self.combs = remove_dup_combs(self.combs)

    def get_consumers_combs(self):
        consumers_combs = []
        for consumer in self.consumers:
            consumers_combs.extend(consumer.combs)
        return consumers_combs

    def get_selected_item(self):
        try:
            select_idx = self.listbox.curselection()
            select_item = self.listbox.get(select_idx)
        except TclError as e:
            print('Listbox is empty (%s)' % e.__class__.__name__)
        else:
            return tuple(select_item.split(', '))

    def double_click_event(self):
        comb = self.get_selected_item()
        if comb:
            self.consumer.combs.append(comb)
            self.consumer.update_combs()
            self.remove_last_comb_if_dup()
            if self.role == 'consumer':
                self.combs.remove(comb)
            elif self.role == 'producer':
                names = unpack(self.combs)
                used_names = get_used_items(names, self.get_consumers_combs(), self.consumer.comb_size)
                while used_names:
                    name, *used_names = used_names
                    self.combs.remove((name,))
            self.update_listbox()
            self.consumer.update_listbox()


class ListsEditor(Frame):
    def __init__(self, parent=None, name='', names=(), whitelist=(), blacklist=(), comb_size=1):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack(side=TOP, expand=YES, fill=BOTH)
        self.name = name
        self.names = self.prepare_names(names)
        self.whitelist = self.prepare_exclist(whitelist)
        self.blacklist = self.prepare_exclist(blacklist)
        self.compare_exclists()
        self.comb_size = comb_size
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

    def compare_exclists(self):
        for comb in self.blacklist:
            if comb in self.whitelist:
                self.whitelist.remove(comb)

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
        self.white_listbox = NamesBox(exclists_fr, self.whitelist, self.main_listbox, comb_size=self.comb_size - 1)
        self.white_listbox.pack(side=LEFT, expand=YES, fill=BOTH)
        self.black_listbox = NamesBox(exclists_fr, self.blacklist, self.main_listbox, comb_size=self.comb_size - 1)
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

    def add_name(self, combs):
        return [((self.name,) + comb) for comb in combs]

    def get_names(self):
        return self.add_name(self.main_listbox.get_combs())

    def get_whitelist(self):
        return self.add_name(self.white_listbox.get_combs())

    def get_blacklist(self):
        return self.add_name(self.black_listbox.get_combs())

if __name__ == '__main__':
    ListsEditor(None, 'misha', ['misha', 'kate', 'yula', 'dasha', 'sasha', 'serega'],
                whitelist=[], blacklist=[], comb_size=2).mainloop()


