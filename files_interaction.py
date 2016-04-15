import re


def read_names(filename):
    text = open(filename, encoding='utf-8-sig').read()
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
    names = re.search('names: ([ ,.;_\w\d]*)( [\w]+:|$| \()', text)
    if names:
        return names.group(1)
    else:
        return ''


def split_names(names_string):
    return re.findall('[-_\w\d]+', names_string)


def get_exclist(text, exclist_name='whitelist'):
    string = re.search(exclist_name + ': ([ ,.;()\w\d]*)( [\w]+:|$)', text)
    if string:
        string = string.group(1)
    else:
        return []
    strings = re.findall('\((.+?)\)', string)
    exclist = []
    for string in strings:
        exclist.append(tuple(split_names(string)))
    return exclist


def exclist_to_string(exclist, comb_size, exclist_name):
    output_string = ''
    if exclist:
        form = '(' + ', '.join(['%s'] * int(comb_size)) + ')'
        output = [form % comb for comb in exclist]
        output_string = '%s: %s' % (exclist_name, ', '.join(output))
    return output_string


if __name__ == '__main__':
    filename = 'names.txt'

    text1 = """
    names: 1, 2, 3, 4, 5
    whitelist: (1, 2), (3, 4), (4, 5)
    blacklist: (1, 5), (3, 5)
    """
    string = '(1, 5), (3, 5)'
    print(get_exclist(correct_text(text1), 'whitelist'))

