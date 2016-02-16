from tkinter import *
from groups_maker import GroupsMaker


class StudentInfoButton(Button):
    def __init__(self, parent=None, **config):
        Button.__init__(self, parent, **config)
        self.pack()
        self.config(command=self.callback)

    def callback(self):
        print('hello')


# def fetch():
#     var = StringVar()
#     var.set(ent.get())
#     button_box = Frame(root)
#     button_box.pack(side=LEFT)
#     for name in var.get().split(','):
#         name_button = StudentInfoButton(button_box, text=name.strip())
#         name_button.pack(side=TOP)
#         name_button.config(width=10)

def get_names_from_string(names_string):
    names_string = names_string.split(',')
    return [name.strip() for name in names_string]

def combine():
    names = get_names_from_string(ent.get())
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


root = Tk()
sub = Frame(root)
sub.pack(side=TOP, expand=YES, fill=X)
Label(sub, text='Entry students names or copy/paste it').pack(side=TOP, expand=YES, fill=X)
ent = Entry(sub)
ent.insert(0, 'misha, kate, yula, serega, dasha, sasha')
ent.pack(side=TOP, expand=YES, fill=X)
ent.focus()
ent.bind('<Return>', (lambda event: combine()))
but = Button(sub, text='combine', command=(lambda:  combine()))
but.pack(side=RIGHT)


root.mainloop()