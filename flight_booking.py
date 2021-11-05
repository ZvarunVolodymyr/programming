import validation
import class_validation


class FlightBooking:
    avia_company: str = ''
    num_of_people: int = ''
    start_time: str = ''
    end_time: str = ''
    date: str = ''
    flight_number: str = ''
    __attributes = ['avia_company', 'num_of_people', 'start_time', 'end_time', 'date',
                    'flight_number']

    def __init__(self, avia_company='', num_of_people='', start_time='', end_time='', date='', flight_number=''):
        if num_of_people == '':
            return
        for i in vars().items():
            self.__setattr__(i[0], i[1])

    @validation.many_decorator(validation.is_empty, validation.is_file)
    def read_from(self, file_name='input.txt', start_line=0):
        file = open(file_name)
        for line in file.readlines()[start_line:]:
            start_line += 1
            input_ = list(map(lambda x: x.strip(), line.split(':')))
            if not input_[0] in self.__attributes:
                break
            self.setattr(input_[0], input_[1])
        file.close()
        return start_line

    @class_validation.vaccine_decorator
    def is_valid(self, name, val):
        return val

    def read_from_console(self):
        for i in self.__attributes:
            text = 'Введіть ' + i
            self.setattr(i, validation.is_class_filed(self.is_valid, i, text=text, function='input'))

    def has_val(self, val):
        for i in self.__attributes:
            if self.getattr(i) is val or self.getattr(i) == val:
                return True
        return False

    def __str__(self):
        return '\n'.join(i + ': ' + str(validation.is_attribute(self, i, function='print')) for i in self.__attributes)

    @class_validation.vaccine_decorator
    def setattr(self, name, val):
        self.__setattr__(name, val)

    @validation.is_attribute
    def getattr(val):
        return val

