
warnings = {
    'dups': 'The timetable is not created. Please change duplicated names.',
    'not_enough': 'The number of students is not enough to form the groups',
    'uniwhite': 'The size of combination(s) in whitelist not match to current combination size',
    'uniblack': 'The size of combination(s) in blacklist not match to current combination size',
    'uniall': 'The size of combinations in whitelist and blacklist not match to current combination size'
}

class GroupsMakerException(Exception):
    pass


class NotEnoughStudents(GroupsMakerException):
    pass

