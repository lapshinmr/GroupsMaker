import random
from gm_exceptions import *


def subtract_combs(combs_list, exclist):
    uniq_combs = combs_list[:]
    for comb in exclist:
        try:
            uniq_combs.remove(comb)
        except ValueError:
            print('No such comb %s in unique combs' % str(comb))
    return uniq_combs


def unpack(combs_list):
    unpacked = []
    for comb in combs_list:
        for name in comb:
            unpacked.append(name)
    return unpacked


def pack(items, comb_size):
    packed = []
    if comb_size < 1:
        return []
    while items:
        comb, items = items[:comb_size], items[comb_size:]
        packed.append(tuple(comb))
    return packed


def molder(combs_list, comb_size=1):
    unpacked = unpack(combs_list)
    packed = pack(unpacked, comb_size)
    return packed


def sort_items_in_comb(comb, dups=True):
    comb = list(comb)
    if not dups:
        comb = list(set(comb))
    return tuple(sorted(comb))


def sort_items_in_all_combs(combs_list, dups=True):
    return [sort_items_in_comb(comb, dups) for comb in combs_list]


def remove_dup_combs(combs_list):
    unique_list = []
    while combs_list:
        comb, *combs_list = combs_list
        while comb in combs_list:
            combs_list.remove(comb)
        unique_list.append(comb)
    return unique_list


def gen_combs(items_list, comb_size=1, uniq=False):
    combs = list(zip(items_list))
    for dummy in range(comb_size - 1):
        tmp_combs = set()
        for comb in combs:
            for item in items_list:
                if uniq and item in comb:
                    continue
                tmp_combs.add(comb + (item, ))
        combs = tmp_combs
    return combs


def gen_sorted_combs(items_list, comb_size, uniq=False):
    combs = gen_combs(items_list, comb_size, uniq)
    return list(set(sort_items_in_all_combs(combs)))


def get_items_from_combs(items, combs, comb_size, used=True):
    possible_combs = gen_sorted_combs(items, comb_size, uniq=True)
    sorted_combs = sort_items_in_all_combs(combs)
    remaining_combs = set(possible_combs) - set(sorted_combs)
    remaining_items = set(unpack(remaining_combs))
    out_items = set(items) - remaining_items if used else remaining_items
    return sorted(list(out_items))


def check_uniformity(combs_list, comb_size):
    check_size = [len(combs) == int(comb_size) for combs in combs_list]
    return False if False in check_size else True


def choose_combs_by_item(item, combs_list):
    return [comb for comb in combs_list if item in comb]


def remove_combs_by_item(item, combs_list):
    exclist = choose_combs_by_item(item, combs_list)
    return list(set(combs_list) - set(exclist))


def get_pack(items, combs_list, comb_size):
    output_combs = []
    remainder = len(items) % comb_size
    while len(items) > remainder:
        comb = combs_list.pop(0)
        output_combs.append(comb)
        for name in comb:
            combs_list = remove_combs_by_item(name, combs_list)
            items.remove(name)
    for idx, item in enumerate(items):
        output_combs[idx] += (item,)
    return output_combs


class PacksGenerator:
    def __init__(self, st_names, comb_size=2, whitelist=(), blacklist=(), repetitions=False):
        self.st_names = st_names
        self.comb_size = comb_size
        self.whitelist = sort_items_in_all_combs(whitelist)
        self.blacklist = sort_items_in_all_combs(blacklist)
        self.repetitions = repetitions
        self.uniq_combs = gen_sorted_combs(self.st_names, comb_size, uniq=True)
        self.uniq_combs = subtract_combs(self.uniq_combs, self.blacklist)
        self.uniq_combs_total = len(self.uniq_combs)
        self.st_total = len(self.st_names)
        self.les_groups_total = self.st_total // self.comb_size
        self.attempts = 0
        # self.limit_attempts = self.les_total * attempts_factor

    def get_packs(self, pack_total):
        combs = self.uniq_combs[:]
        calendar = []
        for attempt in range(pack_total):
            names = self.st_names[:]
            pack = get_pack(names, combs, self.comb_size)
            combs = list(set(combs) - set(pack))
            if pack:
                calendar.append(pack)
        return calendar

    """

    def get_part_without_whitelist(self):
        uniq_combs = subtract_combs(self.uniq_combs, self.whitelist)
        return self.get_lessons(uniq_combs)

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
    pass
