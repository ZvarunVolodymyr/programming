from functools import partial

import validation


def get_functions_list(name):
    return {'valid': is_valid, 'input': is_input, 'print': print_error}.get(name, is_valid)


def get_functions(func):
    def decorator(*value, **kwargs):
        functions = get_functions_list(kwargs.get('function', 'valid'))
        funcc = partial(functions, *value, **kwargs)
        kwargs.pop('function', None)
        return func(funcc)
    return decorator


def is_input(*value_for_conditional, function=None, text=""):
    slesh_n = '\n'
    print(text, end=f'{slesh_n if text != "" else ""}')
    while True:
        try:
            a = [input()]
            a += value_for_conditional
            return function(*a)
        except ValueError as error:
            print(error)
            print('спробуйте йще раз')
        except KeyboardInterrupt:
            print('Програма завершила свою роботу')
            exit()


def is_valid(*value_for_conditional, function=None):
    try:
        return function(*value_for_conditional)
    except ValueError as error:
        raise ValueError(error)


def print_error(*value_for_conditional, function=None, file=''):
    try:
        return function(*value_for_conditional)
    except Exception as error:
        validation.was_error(error, file)
        return None
