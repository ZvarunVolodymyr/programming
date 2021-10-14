import memento
import validation
from sort import merge_sort
from vaccine_class import COVID_CERTIFICATE


class CertificateConteiner:
    list_ = []
    list_of_id = []
    answer_file = ''
    log_file = ''
    history = None

    def __init__(self, load_from_file='', answer_file='answer.txt', log_file='log.txt'):
        self.list_ = []
        self.list_of_id = []
        self.clear_history()
        self.answer_file = answer_file
        self.log_file = log_file
        if load_from_file != '':
            self.input_from_file(load_from_file)

    def clear_history(self):
        self.history = memento.history(self)

    def get_new_id(self):
        new_id = 1
        while new_id in self.list_of_id:
            new_id += 1
        return new_id

    def unique_id(self):
        self.list_of_id.sort()
        for i in range(1, len(self.list_of_id)):
            if self.list_of_id[i] == self.list_of_id[i - 1]:
                new_id = self.get_new_id()
                validation.was_error(f'id {self.list_of_id[i]} вже зайняте, воно змінене на {new_id}',
                                     file=self.log_file)
                self.change_by_id(self.list_of_id[i], [f'id={new_id}'])
                self.history.pop_snap()

    def swap_id(self, old, new):
        for i, val in enumerate(self.list_of_id):
            if val == old:
                self.list_of_id[i] = new
                return

    @validation.many_decorator(validation.is_empty, validation.is_file)
    def input_from_file(self, file_name=''):
        self.clear()
        self.update_log_file('Load info from:\n' + str(file_name))
        file = open(file_name)
        certificate = COVID_CERTIFICATE()
        flag = False
        for line in file.readlines()[1:]:
            if line[0] == '-':
                if not certificate.has_value(None) and not certificate.has_value(''):
                    self.append(certificate)
                    self.history.pop_snap()
                    flag = True
                    certificate = COVID_CERTIFICATE()
                else:
                    s = 'Неправильні данні у: \n'
                    names = certificate.get_attr_names()
                    t = [i if certificate.__getattribute__(i) is None or certificate.__getattribute__(i) == '' else ''
                         for i in names]
                    t = filter(lambda x: x != '', t)
                    validation.was_error(s + '\n'.join(t), self.log_file)
                self.update_log_file('')
                continue

            input_ = list(map(lambda x: x.strip(), line.split(':')))
            certificate.setattr(input_[0], input_[1], self.log_file)
        if flag:
            self.was_changed()
        file.close()

    def update_answer_file(self):
        file = open(self.answer_file, 'w')
        file.write(self.__str__())
        file.close()

    def update_log_file(self, text):
        file = open(self.log_file, 'a')
        file.write('\n' + '-' * 100 + '\n' + text)
        file.close()

    def __repr__(self):
        return self.__str__()

    def append(self, value):
        if type(value) != COVID_CERTIFICATE:
            validation.was_error()
            return
        self.update_log_file('Add:\n' + str(value))
        self.add_id(value.id)
        self.list_.append(value)
        self.unique_id()
        self.was_changed()

    def part_str(self):
        s = ''
        for i in self.list_:
            s += str(i)
        return s

    def __str__(self):
        s = '-' * 100 + '\n'
        s += ('-' * 100 + '\n').join(str(i) + '\n' for i in self.list_)
        s += '-' * 100 + '\n'
        return s

    def find_part(self, value):
        text = 'Список id елементів у якому є ' + str(value) + ':\n'
        s = str(value)
        answer = []
        for i in self.list_:
            if s in i.part_str():
                answer.append(i)
                text += str(i.id) + '\n'
        self.update_log_file(text)
        return answer

    def find(self, value, field_name='id', is_reversed=False):
        answer = []
        value = str(value)
        for i in self.list_[::-1 if is_reversed else 1]:
            if field_name == '' and i.has_value(value) or field_name != '' and i.get_attr_str(field_name) == value:
                answer.append(i)
        return answer

    def __getitem__(self, item):
        return self.list_[item]

    def sort(self, name='id'):
        self.update_log_file('sort with')

        def comp(a, b):
            return a.getattr(name) > b.getattr(name)

        self.list_ = merge_sort(self.list_, comp)
        self.was_changed()

    def remove(self, value_to_remove, field_name='id'):
        to_remove = self.find(value_to_remove, field_name)
        for i in to_remove:
            self.update_log_file('remove:\n' + str(i))
            self.list_.remove(i)
            self.was_changed()

    @validation.many_decorator(validation.is_empty, validation.is_natural_number)
    def add_id(self, id):
        self.list_of_id.append(id)

    @validation.many_decorator(validation.is_empty, validation.is_natural_number)
    def change_by_id(self, id_to_change, changes=[]):
        self.update_log_file('зміна в ід = ' + str(id_to_change))
        obj = self.find(id_to_change, 'id', True)
        if len(obj) == 0:
            validation.was_error('такого id немає', self.log_file)
            return
        obj = obj[0]
        flag = False
        for j in changes:
            j = j.split('=')
            name = j[0]
            value = j[1]
            old = obj.getattr(name, file=self.log_file, function='print')
            if old is None:
                continue
            obj.setattr(name, value)
            current = obj.getattr(name, file=self.log_file, function='print')
            if current is None:
                obj.setattr(name, old)
                continue
            if name == 'id':
                self.swap_id(old, current)
                self.unique_id()

            self.update_log_file(
                'значення в полі = "' + name + '" змінено:\n' + str(old) + ' -> ' + str(current))
            flag = True
        if flag:
            self.was_changed()

    @validation.many_decorator(validation.is_empty, validation.is_natural_number)
    def has_id(self, id):
        return id in self.list_of_id

    def clear_log(self):
        file = open(self.log_file, 'w')
        file.write('')
        file.close()

    def clear(self):
        self.list_.clear()
        self.list_of_id.clear()
        self.was_changed()

    def was_changed(self):
        self.history.new_snap()
        self.update_answer_file()

    def undo(self):
        if self.history.undo():
            self.update_log_file('UNDO')
            self.update_answer_file()

    def redo(self):
        if self.history.redo():
            self.update_log_file('REDO')
            self.update_answer_file()
