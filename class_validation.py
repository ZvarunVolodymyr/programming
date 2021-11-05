import time_date
import validation
from functools import partial


def get_class_validation_functions(name):
    a = {'avia_company': is_avia_company, 'num_of_people': is_num_of_people, 'start_time': is_start_time,
         'end_time': is_end_time, 'date': is_date, 'vaccine': is_flight_number}
    if not name in a.keys():
        raise KeyError
    return a[name]


def vaccine_decorator(func):
    def decorator(obj, name, val, log_file='', is_input=False):
        try:
            return func(obj, name, get_class_validation_functions(name)(val, name, obj))
        except Exception as error:
            if is_input:
                raise ValueError(error)
            validation.was_error(error, log_file)
            return None

    return decorator


def attributes(func):
    def decorator(val, name, obj):
        try:
            attributes = [val]
            if name == 'date':
                attributes += ['1.1.1950', '1.1.2022']
            if name == 'end_time':
                attributes += [obj.start_time]
            if name == 'avia_company':
                attributes += [['Wizzair', 'Ryanair', 'SkyUp', 'QatarAirlines']]
            return func(*attributes)
        except ValueError as error:
            raise error
        except KeyError:
            raise ValueError('такого поля не існує')

    return decorator


@attributes
@validation.is_in_list
def is_avia_company(value):
    return value


@attributes
@validation.is_int_number
def is_num_of_people(n):
    if not (0 <= n <= 300):
        raise ValueError(str(n) + ' некоректна кількість людей')
    return n


@attributes
@time_date.is_time
def is_start_time(value):
    return value


@attributes
def is_end_time(*value):
    if value[1] is None or value[1] == '':
        raise ValueError('end_time не перевірити: start_time не валідне')
    return time_date.is_time_after(*value)


@attributes
def is_date(*value):
    return time_date.is_date_after(*value)


@attributes
def is_flight_number(n):
    if not (n[:2].isalpha() and n[2] == ' ' and n[3:].isnumeric() and len(n) == 8):
        raise ValueError(str(n) + ': не є міжнародним паспортом')
    return n

