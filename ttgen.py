import random
from combs_math import *
from gm_exceptions import *


class TimetableGenerator:
    def __init__(self, names, comb_size=2, lessons_total=1, whitelist=(), blacklist=(), repetitions=False):
        self.names = names
        self.comb_size = comb_size
        self.repetitions = repetitions
        self.lessons_total = lessons_total
        if len(self.names) < comb_size:
            raise NotEnoughStudents
        self.whitelist = sort_items_in_all_combs(whitelist, dups=False)
        self.blacklist = sort_items_in_all_combs(blacklist, dups=False)
        self.uniq_combs = gen_sorted_combs(self.names, comb_size, uniq=True)
        self.uniq_combs_outblack = subtract_combs(self.uniq_combs, self.blacklist)
        self.uniq_combs_outblack = subtract_combs(self.uniq_combs, self.blacklist)
        # self.limit_attempts = self.les_total * attempts_factor

    def get_lesson(self, in_combs_list):
        names = self.names[:]
        combs_list = in_combs_list[:]
        output_combs = []
        remainder = len(names) % self.comb_size
        while len(names) > remainder:
            comb = combs_list.pop(0)
            output_combs.append(comb)
            for name in comb:
                combs_list = remove_combs_by_item(name, combs_list)
                names.remove(name)
        for comb in output_combs:
            in_combs_list.remove(comb)
        for idx, item in enumerate(names):
            output_combs[idx] += (item,)
        return output_combs, in_combs_list

    def get_lessons(self, in_combs_list):
        combs = in_combs_list[:]
        calendar = []
        for attempt in range(self.lessons_total):
            try:
                lesson, combs = self.get_lesson(combs)
            except IndexError:
                return calendar
            if lesson:
                calendar.append(lesson)
        return calendar

    def get_les_versions(self, in_combs_list):
        combs = in_combs_list[:]
        versions = []
        for dummy in range(1000):
            random.shuffle(combs)
            versions.append(self.get_lessons(combs))
        return versions

    """
    def get_timetable(self):
        timetable = []
        parts = []
        timetable.extend(self.get_part_without_whitelist())
        if not self.repetitions:
            return timetable, parts
        while len(timetable) < self.les_total:
            next_tt_part = self.get_lessons(self.uniq_combs)
            if next_tt_part:
                parts.append(len(timetable))
                timetable.extend(next_tt_part)
            self.attempts += 1
            if self.attempts > self.limit_attempts:
                raise NotEnoughStudents
        else:
            cur_ttlen = len(timetable)
            extra_ttlen = cur_ttlen - self.les_total
            if extra_ttlen:
                timetable = timetable[:-extra_ttlen]
        return timetable, parts

    def get_attempts(self):
        return self.attempts
    """


if __name__ == '__main__':
    tt = TimetableGenerator([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 2, 10)
    count = {}
    versions = tt.get_les_versions()
    for vers in versions:
        key = len(vers)
        count[key] = count.get(key, []) + [vers]
    for idx, key in enumerate(sorted(count.keys())):
        print(idx + 1, len(count[key]))
