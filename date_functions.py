import validation


def get_max_day_in_month(month:int, year:int):
    if month in (4, 6, 9, 11):
        return 30
    if month == 2:
        if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
            return 29
        return 28
    return 31


@validation.is_valid
def is_month_day(*value):
    day = value[0]
    month = value[1]
    year = value[2]
    if month in (4, 6, 9, 11) and day == 31:
        raise ValueError
    if month == 2:
        if day == 30:
            raise ValueError
        if not (year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)):
            if day == 29:
                raise ValueError


def date_plus_date(date_1: str, date_2: str):
    date_1 = list(map(int, date_1.split('.')))
    date_2 = list(map(int, date_2.split('.')))
    for i in range(3):
        date_2[i] += date_1[i]

    while date_2[0] > get_max_day_in_month(date_1[1], date_1[2]):
        date_2[0] -= get_max_day_in_month(date_1[1], date_1[2])
        date_1[1] += 1
        date_2[1] += 1

    while date_2[1] > 12:
        date_2[1] -= 12
        date_2[2] += 1

    return '.'.join(map(str, date_2))


def comparison(date_1: str, date_2 : str):
    date_1 = list(map(int, date_1.split('.')))
    date_2 = list(map(int, date_2.split('.')))
    for i in range(len(date_1) - 1, -1, -1):
        if date_1[i] != date_2[i]:
            return date_1[i] < date_2[i]
    return True
