import validation


def is_valid(name, val, vaccine_object, log_file=''):
    try:
        attributes = [val]
        if name == 'birth_date':
            attributes += ['1.1.1950', '1.1.2021']
        if name == 'start_date':
            attributes += [vaccine_object.birth_date, '14.0.0', '0.0.120']
        if name == 'end_date':
            attributes += [vaccine_object.start_date, '0.0.1']
        name = 'is_' + name
        return eval(name)(attributes)
    except ValueError as error:
        raise error
    except KeyError:
        raise ValueError('такого поля не існує')


def is_id(value: []):
    return validation.is_natural_number(value)


def is_username(value: []):
    n = value[0]
    if not n.isalpha():
        raise ValueError(str(n) + ' не є username')
    return n


def is_birth_date(value: []):
    return validation.is_date_in_range(value)


def is_start_date(value: []):
    if value[1] is None or value[1] == '':
        raise ValueError('start_date не перевірити: birth_date не валідне')
    return validation.is_date_between(value)


def is_end_date(value: []):
    if value[1] is None or value[1] == '':
        raise ValueError('end_date не перевірити: birth_date не валідне')
    return validation.is_date_after_term(value)


def is_international_passport(value: []):
    n = value[0]
    if not (n[:2].isalpha() and n[2:].isnumeric() and len(n) == 8):
        raise ValueError(str(n) + ': не є міжнародним паспортом')
    return n


def is_vaccine(value: []):
    n = value[0]
    n = n.strip()
    vaccine_list = ['pfizer', 'moderna', 'AstraZeneca']
    for i in vaccine_list:
        if i.lower() == n:
            return n
    raise ValueError(n + ': не є вакциною, зазначеною в класі')
