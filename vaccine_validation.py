import validation
from functools import partial


def get_vaccine_validation(func):
    def decorator(obj, name, val, log_file='', is_input=False):
        name = 'is_' + name
        func_ = partial(eval(name), val, obj)
        return func(func_, log_file, is_input)
    return decorator


def attributes(func):
    def decorator(val, vaccine_object):
        name = func.__name__
        try:
            attributes = [val]
            if name == 'is_birth_date':
                attributes += ['1.1.1950', '1.1.2021']
            if name == 'is_start_date':
                attributes += [vaccine_object.birth_date, '14.0.0', '0.0.120']
            if name == 'is_end_date':
                attributes += [vaccine_object.start_date, '0.0.1']
            name = 'is_' + name
            return func(*attributes)
        except ValueError as error:
            raise error
        except KeyError:
            raise ValueError('такого поля не існує')
    return decorator


@attributes
def is_id(*value):
    return validation.is_natural_number(*value)


@attributes
def is_username(n):
    if not n.isalpha():
        raise ValueError(str(n) + ' не є username')
    return n


@attributes
def is_birth_date(*value):
    return validation.is_date_in_range(*value)


@attributes
def is_start_date(*value):
    if value[1] is None or value[1] == '':
        raise ValueError('start_date не перевірити: birth_date не валідне')
    return validation.is_date_between(*value)


@attributes
def is_end_date(*value):
    if value[1] is None or value[1] == '':
        raise ValueError('end_date не перевірити: birth_date не валідне')
    return validation.is_date_after_term(*value)


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
