import os
import validation_functions


def is_valid(func):
    @validation_functions.get_functions
    def decorator(funcc):
        return funcc(function=func)
    return decorator

import date_functions

@is_valid
def is_str(n):
    return n


@is_valid
def is_float_number(n):
    n = n.strip()
    try:
        return float(n)
    except ValueError:
        raise ValueError(n + ' не є дійсним числом')


@is_valid
def is_int_number(n):
    if type(n) == str:
        n = n.strip()
    try:
        return int(n)
    except ValueError:
        raise ValueError(n + ' не є цілим числом')


@is_valid
def is_natural_number(n):
    n = n.strip()
    if not (is_int_number(n) and int(n) > 0):
        raise ValueError(n + ' не є натуральним цілим числом')
    return int(n)


@is_valid
def is_menu(n, list_):
    n = n.strip()
    if not n in list_:
        raise ValueError(n + ' не є полем меню')
    return n


@is_valid
def is_greater_then(n, list_):
    k = is_int_number(n)
    for i in list_:
        if k <= i:
            raise ValueError(str(k) + ' не є більшим за ' + str(i))
    return k


@is_valid
def is_in_list(n, list_):
    n = is_natural_number(n)
    if not n in list_:
        raise ValueError(str(n) + ' немає в потрібному масиві')
    return n


@is_valid
def is_attribute(obj, att):
    try:
        return obj.__getattribute__(att)
    except Exception:
        raise ValueError("об'єкт не має атрибута " + str(att))


@is_valid
def has_attribute(att, obj):
    try:
        is_attribute(obj, att)
        return att
    except Exception as error:
        raise ValueError(error)


@is_valid
def is_valid_array(list_, func, size, split_):
    s = []
    if size == -1:
        s = list_.split(split_)
    else:
        s = list_.split(split_)
        if len(s) != size:
            raise ValueError(str(s) + ': не правильна кількість елементів')
    for i in range(len(s)):
        s[i].strip()
        s[i] = func(s[i])
    return s


@is_valid
def is_date(date):

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
        date_functions.is_month_day(day, month, year)
    except ValueError:
        raise ValueError(str(date) + ': некоректна дата')
    return '.'.join([str(day), str(month), str(year)])


@is_valid
def is_date_after_term(this_date, start, term):
    n = this_date
    n = is_date(n)
    date = date_functions.date_plus_date(start, term)
    if not date_functions.comparison(n, date) or date_functions.comparison(n, start):
        raise ValueError(n + ' виходить за межі терміну')
    return n


@is_valid
def is_date_between(date, start, term_1, term_2):
    date = is_date(date)
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


@is_valid
def is_date_in_range(date, start, end):
    if not date_functions.comparison(start, date) or not date_functions.comparison(start, end):
        raise ValueError(str(date) + ' : некоректна дата')
    return date


@is_valid
def is_file(n):
    n = n.strip()
    if not os.path.isfile(n):
        raise ValueError(str(n) + ': файлу не існує, або програма його не бачить')
    return n


@is_valid
def is_vaccine_filed(val, func, name):
    return func(name, val, is_input=True)





def was_error(message='ПОМИЛКА', file=''):
    message = str(message)
    message = '\n' + '*' * len(message) + '\n' + message + '\n' + '*' * len(message)
    print(message)
    if file != '':
        file = open(file, 'a')
        file.write('\n' + message + '\n')
        file.close()


def array_input(text="", size=-1, additional_condition=is_str, split_symbol=' '):
    list_ = input_validation(text, is_valid_array, additional_condition, size, split_symbol)
    return list_
