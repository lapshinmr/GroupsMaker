

class GroupsMakerException(Exception):
    pass


class AttemptsExceeded(GroupsMakerException):
    pass


class NotEnoughCombinations(GroupsMakerException):
    pass