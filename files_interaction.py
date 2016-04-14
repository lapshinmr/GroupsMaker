import re


def data_reader(filename):
    text = open(filename).read()
    text = correct_text(text)
    return text


def correct_text(text):
    text = text.replace('\n', ' ')
    text = text.strip()
    while True:
        res = re.search('[ ]{2,}', text)
        if res:
            text = text.replace(res.group(), ' ')
        else:
            break
    return text


def get_names(text):
    names = re.search('names: ([ ,.;_\w\d]*) whitelist', text)
    return names.group(1)


def get_whitelist(text):
    whitelist = re.search('whitelist: ([ ,.;_\w\d()]*) blacklist', text)
    return whitelist.group(1)


def get_blacklist(text):
    blacklist = re.search('blacklist: ([ ,.;_\w\d()]*)', text)
    return blacklist.group(1)


def split_names(names_string):
    return re.findall('[-_\w\d]+', names_string)


if __name__ == '__main__':
    filename = 'names.txt'

    text1 = """
    names: 1, 2, 3, 4, 5
    whitelist: (1, 2), (3, 4), (4, 5)
    blacklist: (1, 5), (3, 5)
    """
    print(correct_text(text1))

