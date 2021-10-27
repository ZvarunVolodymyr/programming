import date_functions
import validation
from functools import partial


def get_vaccine_validation_functions(name):
    a = {'id': is_id, 'username': is_username, 'birth_date': is_birth_date, 'start_date': is_start_date,
         'end_date': is_end_date, 'international_passport': is_international_passport, 'vaccine': is_vaccine}
    return a[name]


def vaccine_decorator(func):
    def decorator(obj, name, val, log_file='', is_input=False):
        try:
            return func(obj, name, get_vaccine_validation_functions(name)(val, name, obj))
        except Exception as error:
            if is_input:
                raise ValueError(error)
            validation.was_error(error, log_file)
            return None

    return decorator


def attributes(func):
    def decorator(val, name, vaccine_object):
        try:
            attributes = [val]
            if name == 'birth_date':
                attributes += ['1.1.1950', '1.1.2021']
            if name == 'start_date':
                attributes += [vaccine_object.birth_date, '14.0.0', '0.0.120']
            if name == 'end_date':
                attributes += [vaccine_object.start_date, '0.0.1']
            return func(*attributes)
        except ValueError as error:
            raise error
        except KeyError:
            raise ValueError('такого поля не існує')

    return decorator


@attributes
@validation.is_natural_number
def is_id(value):
    return value


@attributes
def is_username(n):
    if not n.isalpha():
        raise ValueError(str(n) + ' не є username')
    return n


@attributes
@date_functions.is_date_in_range
def is_birth_date(value):
    return value


@attributes
def is_start_date(*value):
    if value[1] is None or value[1] == '':
        raise ValueError('start_date не перевірити: birth_date не валідне')
    return date_functions.is_date_between(*value)


@attributes
def is_end_date(*value):
    if value[1] is None or value[1] == '':
        raise ValueError('end_date не перевірити: birth_date не валідне')
    return date_functions.is_date_after_term(*value)


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
