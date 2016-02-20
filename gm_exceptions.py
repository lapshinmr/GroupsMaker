

class GroupMakerException(Exception):
    pass

class AttemptsExceeded(GroupMakerException):
    pass

class NotEnoughCombinations(GroupMakerException):
    pass