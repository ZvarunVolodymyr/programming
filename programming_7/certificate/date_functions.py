def get_max_day_in_month(month: int, year: int):
    if month < 0 or year < 0:
        raise ValueError
    if month in (4, 6, 9, 11):
        return 30
    if month == 2:
        if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
            return 29
        return 28
    return 31


def is_month_day(*value):
    day = value[0]
    month = value[1]
    year = value[2]
    if day > get_max_day_in_month(month, year):
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


def comparison(date_1: str, date_2: str):
    date_1 = list(map(int, date_1.split('.')))
    date_2 = list(map(int, date_2.split('.')))
    for i in range(len(date_1) - 1, -1, -1):
        if date_1[i] != date_2[i]:
            return date_1[i] < date_2[i]
    return True


def is_date_after_term(this_date, start, term):
    n = this_date
    date = date_plus_date(start, term)
    if not comparison(n, date) or comparison(n, start):
        raise ValueError(str(n) + ' виходить за межі терміну')
    return n


def is_date_between(date, start, term_1, term_2):
    flag = False
    try:
        is_date_after_term(date, start, term_1)
        flag = True
        raise ValueError(str(date) + ': некоректна дата')
    except ValueError as error:
        if flag:
            raise ValueError(error)
    if is_date_after_term(date, start, term_2):
        return date


def is_date_in_range(date, start, end):
    if not comparison(start, date) or not comparison(start, end):
        raise ValueError(str(date) + ' : некоректна дата')
    return date


def ymd_to_dmy(date):
    return '.'.join(reversed(date.split('-')))


def dmy_to_ymd(date):
    return '-'.join(reversed(date.split('.')))
