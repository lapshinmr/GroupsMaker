
warnings = {
    'dups': 'The timetable is not created. Please change duplicated names.',
    'not_enough': 'The number of students is not enough to form the groups'
}

class GroupsMakerException(Exception):
    pass


class AttemptsExceeded(GroupsMakerException):
    pass


class GenerateTimetableException(GroupsMakerException):
    pass


class NotEnoughCombinations(GroupsMakerException):
    pass