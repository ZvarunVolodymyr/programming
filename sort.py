def comparison(a:str, b:str, comparator):
    if type(a) == str:
        a = a.lower()
    if type(b) == str:
        b = b.lower()
    return comparator(a, b)


def merge(list_1, list_2, comparator):
    new_list = []
    left_pointer = 0
    right_pointer = 0

    if not comparison(list_1[len(list_1) - 1], list_2[0], comparator):
        return list_1 + list_2

    if not comparison(list_2[len(list_2) - 1], list_1[0], comparator):
        return list_2 + list_1

    while left_pointer < len(list_1) or right_pointer < len(list_2):
        if left_pointer == len(list_1) or \
                right_pointer != len(list_2) and comparison(list_1[left_pointer], list_2[right_pointer], comparator):
            new_list.append(list_2[right_pointer])
            right_pointer += 1
            continue
        new_list.append(list_1[left_pointer])
        left_pointer += 1

    return new_list


def merge_sort(array: [], comparator):
    sz = len(array)
    if sz == 1:
        return array
    list_1 = merge_sort(array[:sz // 2], comparator)
    list_2 = merge_sort(array[sz // 2:], comparator)
    return merge(list_1, list_2, comparator)



