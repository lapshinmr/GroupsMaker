from tkinter import *
from tkinter.scrolledtext import ScrolledText
from groups_maker import GroupsMaker


def get_names_from_string(names_string):
    seps = '.,;'
    for sep in seps:
        names_string = names_string.replace(sep, ' ')
    return names_string.split()


def get_calendar():
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


def add():
    names = get_names_from_string(ent.get())
    label_box = Frame(root)
    label_box.pack(side=LEFT)
    for name in names:
        name_label = Label(label_box, text=name)
        name_label.pack(side=TOP)
        name_label.config(width=10)


# Main window
root = Tk()
root.title('GroupsMaker')
root.resizable(width=FALSE, height=FALSE)
#root.geometry('600x400')

sub = Frame(root)
sub.pack(side=TOP, fill=X)
lab = Label(sub, text='Entry students names or copy/paste it')
lab.pack(side=TOP, expand=YES, fill=X)

ent = Entry(sub)
ent.insert(0, 'misha, kate, yula, serega, dasha, sasha')
ent.pack(side=TOP, fill=X)
ent.focus()
ent.bind('<Return>', (lambda event: add()))

Button(sub, text='add', command=(lambda: add())).pack(side=LEFT)
Button(sub, text='combine', command=(lambda: get_calendar())).pack(side=RIGHT)

names = list(range(1, 46))
tab = Frame(root)
tab.pack(side=TOP, anchor=W)
for num, name in enumerate(names):
    lab = Label(tab, text=num + 1, relief=RIDGE, width=5)
    ent = Entry(tab, width=20)
    lab.grid(row=num % 15, column=((num // 15) * 2))
    ent.grid(row=num % 15, column=((num // 15) * 2 + 1))
    # ent.insert(0, name)


root.mainloop()