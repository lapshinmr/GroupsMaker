

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


def subtract_combs(minuend, subtrahend):
    minued_sorted = sort_items_in_all_combs(minuend, dups=False)
    subtrahend_sorted = sort_items_in_all_combs(subtrahend, dups=False)
    return sorted(list(set(minued_sorted) - set(subtrahend_sorted)))


def remove_dups(sequence):
    """Save order in list"""
    unique_list = []
    while sequence:
        item, *sequence = sequence
        while item in sequence:
            sequence.remove(item)
        unique_list.append(item)
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
    return sorted(list(set(sort_items_in_all_combs(combs))))


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


def get_hist(sequence, axis_x=lambda x: x, axis_y=lambda x: x):
    hist = {}
    for item in sequence:
        key = axis_x(item)
        hist[key] = hist.get(key, []) + [item]
    else:
        for key, value in hist.items():
            hist[key] = axis_y(value)
    return hist


if __name__ == '__main__':
    pass
