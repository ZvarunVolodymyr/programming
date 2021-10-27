def false(*data, obj=None, func=None):
    try:
        func(*data)
        obj.fail('Не видало помилки де мало')
    except ValueError:
        pass


def true(*data, obj=None, func=None):
    try:
        return func(*data)
    except Exception as error:
        obj.fail(error)