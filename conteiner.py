import validation
from sort import merge_sort
from vaccine_class import COVID_CERTIFICATE


class CertificateConteiner:
    list_ = []
    list_of_id = []
    answer_file = ''
    log_file = ''

    def __init__(self, load_from_file='', answer_file='answer.txt', log_file='log.txt'):
        self.answer_file = answer_file
        self.log_file = log_file
        if load_from_file != '':
            self.input_from_file(load_from_file)

    @validation.is_file
    def input_from_file(self, file_name=''):
        self.update_log_file('Load info from:\n' + str(file_name))
        file = open(file_name)
        self.list_.clear()
        self.list_of_id.clear()
        certificate = COVID_CERTIFICATE()
        flag = False
        for line in file:
            if line[0] == '-':
                if not certificate.has_value(None) and not certificate.has_value(''):
                    self.append(certificate)
                    certificate = COVID_CERTIFICATE()
                elif flag:
                    s = 'Неправильні данні у: '
                    t = '\n'
                    names = certificate.get_attr_names()
                    for i in names:
                        if certificate.__getattribute__(i) is None or certificate.__getattribute__(i) == '':
                            t += i + '\n'
                    validation.was_error(s + t, self.log_file)
                self.update_log_file('')
                flag = True
                continue

            input_ = line.split(':')
            certificate.setattr(input_[0].strip(), input_[1].strip(), self.log_file)
            if line[0].strip() == 'id':
                self.add_id(certificate.get_attr(input_[0].strip(), input_[1].strip()))
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
        self.update_answer_file()

    def part_str(self):
        s = ''
        for i in self.list_:
            s += str(i)
        return s

    def __str__(self):
        s = ''
        for i in self.list_:
            s += '-' * 100 + '\n' + str(i) + '\n'
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

    def find(self, value, field_name=''):
        answer = []
        for i in self.list_:
            if field_name == '' and i.has_value(value) or field_name != '' and i.get_attr_str(field_name) == value:
                answer.append(i)
        return answer

    def __getitem__(self, item):
        return self.list_[item]

    def sort(self, name=''):
        self.update_log_file('sort with')

        def comp(a, b):
            return a.get_attr(name) > b.get_attr(name)

        self.list_ = merge_sort(self.list_, comp, name)
        self.update_answer_file()

    def remove(self, value_to_remove, field_name='id'):
        to_remove = self.find(value_to_remove, field_name)
        for i in to_remove:
            self.update_log_file('remove:\n' + str(i))
            self.list_.remove(i)
        self.update_answer_file()

    @validation.many_decorator(validation.is_empty, validation.is_natural_number)
    def add_id(self, id):
        id = validation.is_natural_number(id)
        if id in self.list_of_id:
            validation.was_error('такий id уже існує', self.log_file)
            return
        self.list_of_id.append(id)

    @validation.many_decorator(validation.is_empty, validation.is_natural_number)
    def change_by_id(self, id_to_change, changes=[]):
        flag = False
        self.update_log_file('change in id = ' + str(id_to_change))
        for i in self.find(id_to_change):
            flag = True
            for j in changes:
                j = j.split('=')
                name = j[0]
                value = j[1]
                old = i.get_attr(name, self.log_file)
                if old is None:
                    continue
                if i.__setattr__(name, i.function_decorate(name, value)):
                    continue
                current = i.get_attr(name)
                if current is None:
                    i.__setattr__(name, old)
                    continue
                if name == 'id':
                    self.list_of_id.remove(old)
                    self.add_id(current)

                self.update_log_file(
                    'value in field = "' + name + '" was changed:\n' + str(old) + ' -> ' + str(current))
                self.update_answer_file()
        if not flag:
            validation.was_error('такого id немає', self.log_file)

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
