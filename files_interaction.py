import re


def data_reader(filename):
    text = open(filename).read()
    text = correct_text(text)
    print(text)
    print(get_names(text))
    print(get_whitelist(text))
    print(get_blacklist(text))


def correct_text(text):
    while True:
        res = re.search('[ ]{2,}', text)
        if res:
            text = text.replace('\n', ' ').replace(res.group(), ' ')
        else:
            break
    return text


def get_names(text):
    names = re.search('names: ([ ,a-zA-Z]*) whitelist', text)
    return names.group(1)


def get_whitelist(text):
    whitelist = re.search('whitelist: ([ ,a-zA-Z()]*) blacklist', text)
    return whitelist.group(1)


def get_blacklist(text):
    blacklist = re.search('blacklist: ([ ,a-zA-Z()]*)', text)
    return blacklist.group(1)


if __name__ == '__main__':
    filename = 'names.txt'
    data_reader(filename)
