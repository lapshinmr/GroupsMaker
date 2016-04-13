import re


def data_reader(filename):
    text = open(filename).read()
    print(re.search('[ ]{2}', text))
    text = text.replace('\n', ' ')
    return text

if __name__ == '__main__':
    filename = 'names.txt'
    print(data_reader(filename))
