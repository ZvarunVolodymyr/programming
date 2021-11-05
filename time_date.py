from validation import  call_decorate, function_decorate
import validation


@call_decorate
def is_time(func=lambda x: x):
    @function_decorate
    def decorator(time=''):
        time_ = time.split(':')
        try:
            if len(time_) != 2:
                raise ValueError
            time_[0] = validation.is_int_in_range(time_[0], 0, 24)
            time_[1] = validation.is_int_in_range(time_[1], 0, 60)
        except ValueError as error:
            raise ValueError(str(time) + ' некоректний час')
        return func(time)

    return decorator


@call_decorate
def is_time_after(func=lambda x: x):
    @function_decorate
    @validation.many_decorator(is_time, is_time)
    def decorator(time='', start_time=''):
        time_ = time
        time = time.split(':')
        start_time = start_time.split(':')
        if not(time[0] > start_time[0] or time[0] == start_time[0] and time[1] > start_time[1]):
            raise ValueError(str(time_) + ' некоректний час')
        return func(time_)


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


def is_month_day(*value):
    day = value[0]
    month = value[1]
    year = value[2]
    if day > get_max_day_in_month(month, year):
        raise ValueError


@call_decorate
def is_date(func=lambda x: x):
    @function_decorate
    def decorator(date):
        n = date.split('.')
        filter(lambda x: x != '', n)
        if len(n) != 3:
            raise ValueError(str(date) + ': некоректна дата')
        try:
            day = validation.is_natural_number(n[0])
            month = validation.is_natural_number(n[1])
            year = validation.is_natural_number(n[2])
            if day > 31 or month > 12:
                raise ValueError(str(date) + ': некоректна дата')
            is_month_day(day, month, year)
        except ValueError:
            raise ValueError(str(date) + ': некоректна дата')
        return func('.'.join([str(day), str(month), str(year)]))
    return decorator


@validation.many_decorator(is_date, is_date)
def date_comparison(date_1: str, date_2: str):
    date_1 = list(map(int, date_1.split('.')))
    date_2 = list(map(int, date_2.split('.')))
    for i in range(len(date_1) - 1, -1, -1):
        if date_1[i] != date_2[i]:
            return date_1[i] < date_2[i]
    return True


@call_decorate
def is_date_after(func=lambda x: x):
    @function_decorate
    @validation.many_decorator(is_date, is_date)
    def decorator(date, start):
        if not date_comparison(start, date):
            raise ValueError(str(date) + ' виходить за межі терміну')
        return func(date)
    return decorator


@validation.many_decorator(is_time, is_time)
def time_comparison(time_1, time_2):
    return time_1[0] > time_2[0] or time_1[0] == time_2[0] and time_1[1] >= time_2[1]


def is_time_colision(time_1_start, time_1_end, time_2_start, time_2_end):
    def func(time_1_start, time_1_end, time_2_start, time_2_end):
        return time_comparison(time_2_start, time_1_end) and time_comparison(time_1_end, time_2_start) \
               or time_comparison(time_2_end, time_1_start) and time_comparison(time_1_end, time_2_end)

    return func(time_1_start, time_1_end, time_2_start, time_2_end) or\
            func(time_2_start, time_2_end, time_1_start, time_1_end)
