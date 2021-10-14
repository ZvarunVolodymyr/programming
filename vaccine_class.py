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
            self.setattr(i[0], i[1])

    def has_value(self, value):
        for i in self.__attributes:
            if self.__getattribute__(i) == value:
                return True
        return False

    @vaccine_validation.vaccine_decorator
    def is_valid(self, name, val):
        return val

    def part_str(self):
        return ', '.join([str(self.__getattribute__(i)) for i in self.__attributes])

    def input(self):
        for i in self.__attributes:
            text = 'Введіть ' + i
            self.__setattr__(i, validation.is_vaccine_filed(self.is_valid, i, text=text, function='input'))

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '\n'.join(i + ': ' + str(validation.is_attribute(self, i, function='print')) for i in self.__attributes)

    @vaccine_validation.vaccine_decorator
    def setattr(self, name, val):
        self.__setattr__(name, val)

    @validation.is_attribute
    def getattr(val):
        return val

    def get_attr_str(self, name, file=''):
        ans = self.getattr(name, function='print', file=file)
        if ans is not None:
            ans = str(ans)
        return ans

    def get_attr_names(self):
        return self.__attributes
