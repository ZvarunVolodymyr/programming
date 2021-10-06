import os
import date_functions


def is_str(n):
    return n


def is_float_number(n):
    n = n.strip()
    try:
        return float(n)
    except ValueError:
        raise ValueError(n + ' не є дійсним числом')


def is_int_number(n):
    if type(n) == str:
        n = n.strip()
    try:
        return int(n)
    except ValueError:
        raise ValueError(n + ' не є цілим числом')


def is_natural_number(n):
    n = n.strip()
    if not (is_int_number(n) and int(n) > 0):
        raise ValueError(n + ' не є натуральним цілим числом')
    return int(n)


def is_menu(n, list_):
    n = n.strip()
    if not n in list_:
        raise ValueError(n + ' не є полем меню')
    return n


def is_greater_then(n, list_):
    k = is_int_number(n)
    for i in list_:
        if k <= i:
            raise ValueError(str(k) + ' не є більшим за ' + str(i))
    return k


def is_in_list(n, list_):
    n = is_natural_number(n)
    if not n in list_:
        raise ValueError(str(n) + ' немає в потрібному масиві')
    return n


def is_attribute(obj, att):
    try:
        return obj.__getattribute__(att)
    except Exception:
        raise ValueError("об'єкт не має атрибута " + str(att))


def has_attribute(att, obj):
    try:
        is_attribute(obj, att)
        return att
    except Exception as error:
        raise ValueError(error)


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
        is_valid(date_functions.is_month_day, day, month, year)
    except ValueError:
        raise ValueError(str(date) + ': некоректна дата')
    return '.'.join([str(day), str(month), str(year)])


def is_date_after_term(this_date, start, term):
    n = this_date
    n = is_date(n)
    date = date_functions.date_plus_date(start, term)
    if not date_functions.comparison(n, date) or date_functions.comparison(n, start):
        raise ValueError(n + ' виходить за межі терміну')
    return n


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


def is_date_in_range(date, start, end):
    if not date_functions.comparison(start, date) or not date_functions.comparison(start, end):
        raise ValueError(str(date) + ' : некоректна дата')
    return date


def is_file(n):
    n = n.strip()
    if not os.path.isfile(n):
        raise ValueError(str(n) + ': файлу не існує, або програма його не бачить')
    return n


def is_vaccine_filed(val, func, name):
    return func(name, val, is_input=True)


def is_valid(additional_condition=is_str, *value_for_conditional):
    try:
        return additional_condition(*value_for_conditional)
    except ValueError as error:
        raise ValueError(error)


def input_validation(additional_condition=is_str, *value_for_conditional, text=""):
    slesh_n = '\n'
    print(text, end=f'{slesh_n if text != "" else ""}')
    while True:
        try:
            a = [input()]
            a += value_for_conditional
            return additional_condition(*a)
        except ValueError as error:
            print(error)
            print('спробуйте йще раз')
        except KeyboardInterrupt:
            print('Програма завершила свою роботу')
            exit()


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
