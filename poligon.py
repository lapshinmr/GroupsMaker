def weird():
    spam = 42
    handler = (lambda: spam * 2)
    spam = 50
    print(handler())
    spam = 60
    print(handler())

def odd():
    funcs = []
    for c in 'abcdefg':
        funcs.append((lambda c=c: c))
    return funcs

for func in odd():
    print(func(), end=' ')
