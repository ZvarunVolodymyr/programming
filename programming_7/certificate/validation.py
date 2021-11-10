from certificate import date_functions
# import validation
from functools import partial


def get_vaccine_validation_functions(name):
    a = {'id': is_empty, 'vaccine': is_vaccine, 'username': is_username, 'birth_date': is_birth_date,
         'start_date': is_start_date, 'end_date': is_end_date, 'international_passport': is_international_passport}
    if not name in a.keys():
        raise ValueError('такого поля не існує')
    return a[name]


def vaccine_validation(name, data):
    return get_vaccine_validation_functions(name)(data, name)


def attributes(func):
    def decorator(data, name):
        try:
            attributes = [data[name]]
            if name == 'birth_date':
                attributes += ['1950-1-1', '2022-1-1']
            if name == 'start_date':
                attributes += [data['birth_date'], '0-0-14', '120-0-0']
            if name == 'end_date':
                attributes += [data['start_date'], '1-0-0']
            return func(*attributes)
        except ValueError as error:
            raise error
        except KeyError:
            raise ValueError('такого поля не існує')

    return decorator


@attributes
def is_empty(value):
    return value


@attributes
def is_username(n):
    if not n.isalpha():
        raise ValueError(str(n) + ' не є username')
    return n


@attributes
def is_birth_date(*value):
    value_ = list(date_functions.ymd_to_dmy(value[i]) for i in range(3))
    date_functions.is_date_after_term(*value_)
    return value[0]


@attributes
def is_start_date(*value):
    if value[1] is None or value[1] == '':
        raise ValueError('start_date не перевірити: birth_date не валідне')
    value_ = list(date_functions.ymd_to_dmy(value[i]) for i in range(4))
    date_functions.is_date_between(*value_)
    return value[0]


@attributes
def is_end_date(*value):
    if value[1] is None or value[1] == '':
        raise ValueError('end_date не перевірити: start_date не валідне')
    value_ = list(date_functions.ymd_to_dmy(value[i]) for i in range(3))
    date_functions.is_date_after_term(*value_)
    return value[0]


@attributes
def is_international_passport(n):
    if not (n[:2].isalpha() and n[2:].isnumeric() and len(n) == 8):
        raise ValueError(str(n) + ': не є міжнародним паспортом')
    return n


@attributes
def is_vaccine(n):
    n = n.strip().lower()
    vaccine_list = ['pfizer', 'moderna', 'AstraZeneca']
    for i in vaccine_list:
        if i.lower() == n:
            return n
    raise ValueError(n + ': не є вакциною, зазначеною в класі')