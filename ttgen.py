import random
from combs_math import *
from gm_exceptions import *


class TimetableGenerator:
    versions_total = 1000

    def __init__(self, names, comb_size=2, lessons_total=1, whitelist=(), blacklist=(), repetitions=False):
        self.names = names
        self.comb_size = comb_size
        self.repetitions = repetitions
        self.lessons_total = lessons_total
        if len(self.names) < comb_size:
            raise NotEnoughStudents
        self.whitelist = sort_items_in_all_combs(whitelist, dups=False)
        self.blacklist = sort_items_in_all_combs(blacklist, dups=False)
        self.combs = gen_sorted_combs(self.names, comb_size, uniq=True)
        self.combs_wo_black = subtract_combs(self.combs, self.blacklist)
        self.combs_wo_black_white = subtract_combs(self.combs_wo_black, self.whitelist)

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

    def get_course(self, in_combs_list):
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

    def get_course_versions(self, in_combs_list):
        combs = in_combs_list[:]
        courses = []
        for dummy in range(self.versions_total):
            random.shuffle(combs)
            courses.append(self.get_course(combs))
        return courses

    @staticmethod
    def choose_version(versions_count, lessons_total, quantile=0.05):
        if lessons_total in versions_count:
            return random.choice(versions_count[lessons_total])
        elif lessons_total > max(versions_count.keys()):
            versions = []
            keys = sorted(versions_count.keys(), reverse=True)
            while len(versions) < int(quantile * self.versions_total):
                key, *keys = keys
                versions.extend(versions_count[key])
            print("quantile's versions", len(versions))
            return len(random.choice(versions))


if __name__ == '__main__':
    tt = TimetableGenerator([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 2, 10)
    versions = tt.get_course_versions(tt.combs)
    count = tt.get_courses_hist(versions)
    for idx, key in enumerate(sorted(count.keys())):
        print(idx + 1, len(count[key]))
    print(tt.choose_version(count, 11))
