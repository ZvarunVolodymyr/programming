import os


def is_str(value: []):
    return value[0]


def is_float_number(value: []):
    n = value[0]
    n = n.strip()
    try:
        return float(n)
    except ValueError:
        raise ValueError(n + ' не є дійсним числом')


def is_int_number(value: []):
    if len(value) == 0:
        value = ['None']
    n = value[0]
    if type(n) == str:
        n = n.strip()
    try:
        return int(n)
    except ValueError:
        raise ValueError(n + ' не є цілим числом')


def is_natural_number(value: []):
    n = value[0]
    n = n.strip()
    if not (is_int_number([n]) and int(n) > 0):
        raise ValueError(n + ' не є натуральним цілим числом')
    return int(n)


def is_menu(value: []):
    n = value[0]
    n = n.strip()
    if not n in value[1:]:
        raise ValueError(n + ' не є полем меню')
    return n


def is_greater_then(value: []):
    n = value[0]
    k = is_int_number(n)
    for i in value:
        if k <= i:
            raise ValueError(str(k) + ' не є більшим за ' + str(i))
    return k


def is_in_list(value:[]):
    n = value[0]
    n = is_natural_number([n])
    list_ = value[1]
    if not n in list_:
        raise ValueError(str(n) + ' немає в потрібному масиві')
    return n


def is_attribute(value:[]):
    n:str = value[0]
    att = value[1]
    try:
        n.__getattribute__(att)
    except Exception:
        raise ValueError("об'єкт не має атрибута " + str(att))
    return n.__getattribute__(att)


def is_valid_array(value: []):
    n = value[0]
    s = []
    if value[2] == -1:
        s = n.split(value[3])
    else:
        s = n.split(value[3])[:value[2]]
        if len(s) < value[2]:
            raise ValueError(str(s) + ': не правильна кількість елементів')
    for i in range(len(s)):
        s[i].strip()
        s[i] = value[1](s[i])
    return s


def is_username(value: []):
    n = value[0]
    if not n.isalpha():
        raise ValueError(str(n) + ' не є username')
    return n


def is_passport(value: []):
    n = value[0]
    if not (n[:2].isalpha() and n[2:].isnumeric() and len(n) == 8):
        raise ValueError(str(n) + 'не є міжнародним паспортом')
    return n


def is_month_day(value: []):
    day = value[0]
    month = value[1]
    year = value[2]
    if day <= 0 or month <= 0 or year <= 0 or month > 12 or day > 31:
        raise ValueError
    if month in (4, 6, 9, 11) and day == 31:
        raise ValueError
    if month == 2:
        if day == 30:
            raise ValueError
        if not (year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)):
            if day == 29:
                raise ValueError


def is_date(value: []):
    n = value[0]
    n = n.split('.')
    filter(lambda x: x != '', n)
    if len(n) != 3:
        raise ValueError(str(n) + ': некоректна дата')
    try:
        day = is_int_number([n[0]])
        month = is_int_number([n[1]])
        year = is_int_number([n[2]])
        is_valid(is_month_day, day, month, year)
    except ValueError:
        raise ValueError(str(value[0]) + ': некоректна дата')
    return '.'.join([str(day), str(month), str(year)])


def is_date_after_term(value: []):
    n = value[0]
    n = is_date(n)
    date = list(map(int, n.split('.')))
    start_date = list(map(int, value[0].split('.')))
    term = list(map(int, value[0].split('.')))
    for i in range(3):
        start_date[i] += term[i]


def is_vaccine(value: []):
    n = value[0]
    n = n.strip()
    vaccine_list = ['pfizer', 'moderna', 'AstraZeneca']
    if not n in vaccine_list:
        raise ValueError(n + ': не є вакциною, зазначеною в класі')
    return n


def is_file(value: []):
    n = value[0]
    n = n.strip()
    if not os.path.isfile(n):
        raise ValueError(str(n) + ': файлу не існує, або програма його не бачить')


def is_valid(additional_condition=is_str, *value_for_conditional):
    try:
        return additional_condition(value_for_conditional)
    except ValueError as error:
        raise ValueError(error)


def input_validation(text="", additional_condition=is_str, *value_for_conditional):
    slesh_n = '\n'
    print(text, end=f'{slesh_n if text != "" else ""}')
    while True:
        try:
            a = [input()]
            a += value_for_conditional
            return additional_condition(a)
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
    if size != -1:
        list_ = list_[:size]
    return list_