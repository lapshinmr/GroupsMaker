from tkinter import *
from widgets import TipButton


class NamesBox(Frame):
    def __init__(self, parent, names):
        Frame.__init__(self, parent)
        self.names = list(names)
        self.show()
        self.exclist_objs = None

    def connect(self, exclist_objs):
        self.exclist_objs = exclist_objs

    def show(self):
        names_fr = Frame(self, bd=2, relief=RIDGE)
        names_fr.pack(side=TOP, expand=YES, fill=BOTH)
        self.listbox = Listbox(names_fr)
        sbar = Scrollbar(names_fr)
        sbar.config(command=self.listbox.yview)
        sbar.pack(side=RIGHT, fill=Y)
        self.listbox.config(yscrollcommand=sbar.set)
        self.listbox.pack(side=LEFT, expand=YES, fill=BOTH)
        but_frame = Frame(self)
        but_frame.pack(side=TOP, expand=YES, fill=X)
        tip_white = 'Add selected name to the %s. Or left double click on the selected name.' % 'white'
        tip_black = 'Add selected name to the %s. Or left double click on the selected name.' % 'black'
        TipButton(but_frame, text='white', command=lambda: self.pop(0), tip=tip_white).pack(side=LEFT, expand=YES, fill=X)
        TipButton(but_frame, text='black', command=lambda: self.pop(1), tip=tip_black).pack(side=RIGHT, expand=YES, fill=X)
        self.listbox.bind('<Double-1>', lambda event: self.pop(0))
        self.listbox.bind('<Double-3>', lambda event: self.pop(1))
        self.fill()

    def fill(self):
        self.listbox.delete(0, END)
        for name in self.names:
            self.listbox.insert(END, name)

    def add(self, name):
        self.names.append(name)
        self.fill()

    def pop(self, exclist_type):
        try:
            select_idx = self.listbox.curselection()
            name = self.listbox.get(select_idx)
            self.listbox.delete(select_idx)
            self.names.remove(name)
            self.exclist_objs[exclist_type].add(name)
        except TclError as e:
            print('Listbox is empty (%s)' % e.__class__.__name__)


class ExcList(Frame):
    def __init__(self, parent, exclist, names_obj, exclist_name):
        Frame.__init__(self, parent)
        self.exclist = list(exclist)
        self.names_obj = names_obj
        self.exclist_name = exclist_name
        self.frame = Frame(self)
        self.frame.pack(side=TOP, expand=YES, fill=BOTH)
        self.show()

    def add(self, name):
        self.exclist.append(name)
        self.show()

    def clean_frame(self):
        label_ids = list(self.frame.children.keys())
        for label_id in label_ids:
            self.frame.children[label_id].destroy()

    def show(self):
        self.clean_frame()
        for name in self.exclist:
            lab = Label(self.frame, text=name)
            lab.pack(side=TOP, fill=X)
            lab.bind('<Double-1>', self.pop)

    def pop(self, event):
        name = event.widget.cget('text')
        self.exclist.remove(name)
        event.widget.destroy()
        self.names_obj.add(name)


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
        Label(self, text=self.name).pack(side=TOP, expand=YES, fill=X)
        self.names = NamesBox(self, self.names)
        self.names.pack(side=TOP, expand=YES, fill=BOTH)
        self.exclists_fr = Frame(self)
        self.exclists_fr.pack(side=TOP, expand=YES, fill=BOTH)
        self.whitelist = ExcList(self.exclists_fr, self.whitelist, self.names, 'white')
        self.blacklist = ExcList(self.exclists_fr, self.blacklist, self.names, 'black')
        self.names.connect([self.whitelist, self.blacklist])
        self.whitelist.pack(side=LEFT, expand=YES, fill=BOTH)
        self.blacklist.pack(side=RIGHT, expand=YES, fill=BOTH)
        Button(self, text='Accept', command=self.accept).pack(side=BOTTOM, expand=YES, fill=X)

    def accept(self):
        if self.parent is None:
            self.quit()
        else:
            self.parent.destroy()


if __name__ == '__main__':
    # ListsEditor(None, 'misha', ('kate', 'yula', 'dasha'), ('serega',), ('sasha',)).mainloop()
    ListsEditor(None, 'misha', ('kate', 'yula', 'dasha')).mainloop()

