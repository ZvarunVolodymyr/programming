def false(*data, obj=None, func=None):
    try:
        func(*data)
        obj.fail('Не видало помилки де мало')
    except:
        pass


def true(*data, obj=None, func=None):
    try:
        return func(*data)
    except:
        obj.fail('Помилка')
