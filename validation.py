import os
import validation_functions


def function_decorate(func):
    @validation_functions.get_functions
    def decorator(funcc):
        return funcc(function=func)
    return decorator


def call_decorate(func):
    def decorator(*value, **args):
        if len(value) == 1 and callable(value[0]):
            return func(value[0])
        return func()(*value, **args)
    return decorator


def many_decorator(*decorators):
    def decorator(func):
        def inner_decorator(*value):
            ans = []
            if len(value) < len(decorators):
                raise ValueError('декораторів забагато')
            for i in range(len(decorators)):
                ans.append(decorators[i](value[i]))
            for i in range(len(decorators), len(value)):
                ans.append(value[i])
            return func(*ans)
        return inner_decorator
    return decorator


@call_decorate
def is_empty(func=lambda x: x):
    @function_decorate
    def decorator(n):
        return func(n)
    return decorator


@call_decorate
def is_float_number(func=lambda x: x):
    @function_decorate
    def decorator(n):
        n = str(n)
        n = n.strip()
        try:
            return func(float(n))
        except ValueError:
            raise ValueError(n + ' не є дійсним числом')
    return decorator


@call_decorate
def is_int_number(func=lambda x: x):
    @function_decorate
    def decorator(n):
        n = str(n)
        n = n.strip()
        val = None
        try:
            val = int(n)
        except ValueError as error:
            raise ValueError(n + ' не є цілим числом')
        return func(val)
    return decorator


@call_decorate
def is_natural_number(func=lambda x: x):
    @function_decorate
    @is_int_number
    def decorator(n):
        if n <= 0:
            raise ValueError(str(n) + ' не є натуральним цілим числом')
        return func(n)
    return decorator


@call_decorate
def is_in_list(func=lambda x: x):
    @function_decorate
    def decorator(n, list_):
        if not n in list_:
            raise ValueError(str(n) + ' немає в потрібному масиві')
        return func(n)
    return decorator


@call_decorate
def is_menu(func=lambda x: x):
    @function_decorate
    @is_in_list
    def decorator(n):
        return func(n)
    return decorator


@call_decorate
def is_attribute(func=lambda x: x):
    @function_decorate
    def decorator(obj, att):
        val = None
        try:
            val = obj.__getattribute__(att)
        except Exception:
            raise ValueError("об'єкт не має атрибута " + str(att))
        return func(val)
    return decorator


@call_decorate
def has_attribute(func=lambda x: x):
    @function_decorate
    def decorator(att, obj):
        val = None
        try:
            is_attribute(obj, att)
            val = att
        except Exception as error:
            raise ValueError(error)
        return func(val)
    return decorator


@call_decorate
def is_valid_array(func=lambda x: x):
    @function_decorate
    @many_decorator(is_empty, is_empty, is_natural_number, is_empty)
    def decorator(list_, func_, size, split_):
        s = []
        if size == -1:
            s = list_.split(split_)
        else:
            s = list_.split(split_)
            if len(s) != size:
                raise ValueError(str(s) + ': не правильна кількість елементів')
        for i in range(len(s)):
            s[i].strip()
            s[i] = func_(s[i])
        return func(s)
    return decorator


@call_decorate
def is_file(func=lambda x: x):
    @function_decorate
    def decorator(n):
        n = n.strip()
        if not os.path.isfile(n):
            raise ValueError(str(n) + ': файлу не існує, або програма його не бачить')
        return func(n)
    return decorator


@call_decorate
def is_class_filed(func=lambda x: x):
    @function_decorate
    def decorator(val, func_, name):
        return func(func_(name, val, is_input=True))
    return decorator


@call_decorate
def is_int_in_range(func=lambda x: x):
    @function_decorate
    @many_decorator(is_int_number, is_int_number, is_int_number)
    def decorator(val, a, b):
        if not (a <= val <= b):
            raise ValueError('число виходить за межі')
        return func(val)
    return decorator


def was_error(message='ПОМИЛКА', file=''):
    message = str(message)
    message = '\n' + '*' * len(message) + '\n' + message + '\n' + '*' * len(message)
    print(message)
    if file != '':
        file = open(file, 'a')
        file.write('\n' + message + '\n')
        file.close()


# def array_input(text="", size=-1, additional_condition=is_str, split_symbol=' '):
#     list_ = input_validation(text, is_valid_array, additional_condition, size, split_symbol)
#     return list_
