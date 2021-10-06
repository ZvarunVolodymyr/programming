import vaccine_validation
import validation


class COVID_CERTIFICATE:
    id: int = ''
    username: str = ''
    international_passport: str = ''
    start_date: str = ''
    end_date: str = ''
    birth_date: str = ''
    vaccine: str = ''
    __attributes = ['id', 'username', 'birth_date', 'start_date', 'end_date', 'vaccine',
                    'international_passport']

    def __init__(self, id='', username='', international_passport='', start_date='', end_date='', date_of_birth='',
                 vaccine=''):
        if id == '':
            return
        for i in vars().items():
            self.__setattr__(i[0], self.is_valid(i[0], i[1]))

    def has_value(self, value):
        for i in [a for a in dir(self) if not ('__' in a) and not callable(getattr(self, a))]:
            if self.__getattribute__(i) == value:
                return True
        return False

    @vaccine_validation.get_vaccine_validation
    def is_valid(func, log_file='', is_input=False):
        try:
            return func()
        except ValueError as error:
            if is_input:
                raise ValueError(error)
            validation.was_error(error, log_file)
            return None

    def part_str(self):
        s = '['
        for i in self.__attributes:
            s += str(self.__getattribute__(i)) + ', '
        if len(s) != 1:
            s = s[:-2]
        s += ']'
        return s

    def input(self):
        for i in self.__attributes:
            text = 'Введіть ' + i
            self.__setattr__(i, validation.input_validation(validation.is_vaccine_filed, self.is_valid, i, text=text))

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = ''
        for i in self.__attributes:
            s += i + ': ' + self.get_attr_str(i) + '\n'
        s = s[:-1]
        return s

    def get_attr(self, name, file=''):
        try:
            return validation.is_valid(validation.is_attribute, self, name)
        except ValueError as error:
            validation.was_error(error, file)
            return None

    def get_attr_str(self, name, file=''):
        ans = self.get_attr(name, file)
        if ans is not None:
            ans = str(ans)
        return ans

    def get_attr_names(self):
        return self.__attributes
