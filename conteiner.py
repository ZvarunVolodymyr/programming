import copy

import validation
from flight_booking import FlightBooking


class FlightConteiner:
    list_ = []

    def __init__(self, arr=[]):
        for i in arr:
            self.append(i)

    def append(self, value):
        if type(value) != FlightBooking:
            raise TypeError
        self.list_.append(value)

    @validation.many_decorator(validation.is_empty, validation.is_file)
    def read_from(self, file_name=''):
        file = open(file_name)
        i = 1
        len_ = len(file.readlines())
        file.close()
        while i > len_:
            obj = FlightBooking()
            i = obj.read_from(file_name, i)
            if obj.has_val(None) or obj.has_val(''):
                continue
            self.append(obj)

    @validation.many_decorator(validation.is_empty, validation.is_file)
    def most_flight(self, file='output.txt'):
        dict = {}
        for i in self.list_:
            dict[i.avia_company] += 1

        max_ = 0
        name = ''
        for i in dict.items():
            if i[1] > max_:
                max_ = i[1]
                name = i[0]

        file_ = open(file, 'a')
        file_.write(f'Найбільше перевезень за рік у {name} = {max_}')
        file_.close()

    @validation.many_decorator(validation.is_empty, validation.is_file)
    def most_start_time(self, file='output.txt'):
        dict = {}
        for i in self.list_:
            dict[i.start_time] += 1

        max_ = 0
        name = ''
        for i in dict.items():
            if i[1] > max_:
                max_ = i[1]
                name = i[0]
        file_ = open(file, 'a')
        file_.write(f'Найбільше подій у: \n')
        for i in dict.items():
            if i[1] == max_:
                file_.write(f'{i[0]} = {i[1]}')
        file_.close()

    def __len__(self):
        return len(self.list_)

    def __str__(self):
        s = '-' * 100 + '\n'
        s += ('-' * 100 + '\n').join(str(i) + '\n' for i in self.list_)
        s += '-' * 100 + '\n'
        return s