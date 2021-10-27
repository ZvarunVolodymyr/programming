import validation
from validation import call_decorate, function_decorate, is_natural_number, is_int_number, many_decorator


@validation.many_decorator(validation.is_int_number, validation.is_int_number)
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


@validation.function_decorate
def is_month_day(*value):
    day = value[0]
    month = value[1]
    year = value[2]
    if day > get_max_day_in_month(month, year):
        raise ValueError


@call_decorate
def is_date_term(func=lambda x: x):
    @function_decorate
    def decorator(date):
        n = date.split('.')
        day = is_int_number(n[0])
        month = is_int_number(n[1])
        year = is_int_number(n[2])
        if day < 0 or month < 0 or year < 0:
            raise ValueError(str(date) + ' не коректний термін ')
        return func(date)
    return decorator


@validation.many_decorator(is_date_term, is_date_term)
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


@validation.many_decorator(is_date_term, is_date_term)
def comparison(date_1: str, date_2: str):
    date_1 = list(map(int, date_1.split('.')))
    date_2 = list(map(int, date_2.split('.')))
    for i in range(len(date_1) - 1, -1, -1):
        if date_1[i] != date_2[i]:
            return date_1[i] < date_2[i]
    return True


@call_decorate
def is_date(func=lambda x: x):
    @function_decorate
    def decorator(date):
        n = date.split('.')
        filter(lambda x: x != '', n)
        if len(n) != 3:
            raise ValueError(str(date) + ': некоректна дата')
        try:
            day = is_natural_number(n[0])
            month = is_natural_number(n[1])
            year = is_natural_number(n[2])
            if day > 31 or month > 12:
                raise ValueError(str(date) + ': некоректна дата')
            is_month_day(day, month, year)
        except ValueError:
            raise ValueError(str(date) + ': некоректна дата')
        return func('.'.join([str(day), str(month), str(year)]))
    return decorator


@call_decorate
def is_date_after_term(func=lambda x: x):
    @function_decorate
    @many_decorator(is_date, is_date, is_date_term)
    def decorator(this_date, start, term):
        n = this_date
        date = date_plus_date(start, term)
        if not comparison(n, date) or comparison(n, start):
            raise ValueError(str(n) + ' виходить за межі терміну')
        return func(n)
    return decorator


@call_decorate
def is_date_between(func=lambda x: x):
    @function_decorate
    @many_decorator(is_date, is_date, is_date_term, is_date_term)
    def decorator(date, start, term_1, term_2):
        flag = False
        try:
            is_date_after_term(date, start, term_1)
            flag = True
            raise ValueError(str(date) + ': некоректна дата')
        except ValueError as error:
            if flag:
                raise ValueError(error)
        if is_date_after_term(date, start, term_2):
            return func(date)
    return decorator


@call_decorate
def is_date_in_range(func=lambda x: x):
    @function_decorate
    @many_decorator(is_date, is_date, is_date)
    def decorator(date, start, end):
        if not comparison(start, date) or not comparison(start, end):
            raise ValueError(str(date) + ' : некоректна дата')
        return func(date)
    return decorator
