from tkinter import *
from groups_maker import GroupsMaker

#root.resizable(width=FALSE, height=FALSE)
#root.geometry('600x400')


class MainLogic:
    def __init__(self):
        self.root = Tk()
        self.root.title('GroupsMaker')
        self.ent_frame = Frame(self.root)
        self.ent_frame.pack(side=TOP, fill=X)
        Label(self.ent_frame, text='Entry students names').pack(side=TOP, fill=X)
        self.names_input = Entry(self.ent_frame)
        self.names_input.insert(0, 'misha, kate, yula, serega, dasha, sasha')
        self.names_input.pack(side=TOP, fill=X)
        self.names_input.focus()
        Button(self.ent_frame, text='add', command=(lambda: self.add())).pack(side=LEFT)
        Button(self.ent_frame, text='combine', command=(lambda: self.get_calendar())).pack(side=RIGHT)
        self.tab_frame = Frame(self.root)
        self.tab_frame.pack(side=TOP, anchor=W)
        self.all_names = []

    def start(self):
        self.root.mainloop()

    @staticmethod
    def get_names_from_string(names_string):
        seps = '.,;'
        for sep in seps:
            names_string = names_string.replace(sep, ' ')
        return names_string.split()

    def get_calendar(self):
        pass
        """
            g = GroupsMaker(names, 3)
            calendar = g.get_calendar()
            with open('calendar', 'w') as f:
                idx = 0
                for day in calendar:
                    idx += 1
                    f.write('%s: ' % idx)
                    for pare in day:
                        f.write('%20s ' % str(pare))
                    f.write('\n')
        """

    def add(self):
        pass
        """
            new_names = get_names_from_string(names_input.get())
            print(new_names)
            all_names.extend(new_names)
            print(all_names)
            for num, name in enumerate(all_names):
                lab = Label(tab, text=num + 1, relief=RIDGE, width=5)
                ent = Entry(tab, width=20)
                lab.grid(row=num % 15, column=((num // 15) * 2))
                ent.grid(row=num % 15, column=((num // 15) * 2 + 1))
                ent.insert(0, name)
        """

m = MainLogic()
m.start()
