import conteiner
import vaccine_class
import validation


def menu_exit(value):
    exit(0)


def menu_load(certificate_array : conteiner.CertificateConteiner):
    variant = validation.input_validation('choose - для вибору файлу\n'
                                          'default - стандартний файл(input.txt)', validation.is_menu,
                                          ['choose', 'default'])
    file = 'input.txt'
    if variant == 'choose':
        file = validation.input_validation('Введіть назву файла', validation.is_file)
    certificate_array.input_from_file(file)


def menu_set_answer_file(certificate_array : conteiner.CertificateConteiner):
    file = validation.input_validation('Введіть назву файла', validation.is_file)
    certificate_array.answer_file = file


def menu_set_log_file(certificate_array : conteiner.CertificateConteiner):
    file = validation.input_validation('Введіть назву файла', validation.is_file)
    certificate_array.log_file = file


def menu_add(certificate_array: conteiner.CertificateConteiner):
    certificate = vaccine_class.COVID_CERTIFICATE()
    certificate.input()
    certificate_array.append(certificate)


def menu_remove(certificate_array: conteiner.CertificateConteiner):
    id = validation.input_validation('Введіть іd сертефікату для видалення')
    certificate_array.remove(id)


def menu_change(certificate_array: conteiner.CertificateConteiner):
    id = validation.input_validation('Введіть id сертифікату до зміни', validation.is_in_list,
                                     certificate_array.list_of_id)
    changes = []
    while True:
        variant = validation.input_validation('next - ввести настпну зміну\n'
                                              'stop - припинити вводити зміни', validation.is_menu, ['next', 'stop'])
        if variant == 'stop':
            certificate_array.change_by_id(id, changes)
            return 0
        name = input('Введіть назву поля, що хочете змінити\n')
        val = input('Введіть нове значення\n')
        changes.append(name + '=' + val)


def menu_find(certificate_array: conteiner.CertificateConteiner):
    to_find = input('Введіть рядок для пошуку, регістр важливий\n')
    certificate_array.find_part(to_find)


def menu_sort(certificate_array: conteiner.CertificateConteiner):
    certificate_array.sort()


def menu_clear(certificate_array: conteiner.CertificateConteiner):
    certificate_array.clear()


def menu_clear_log(certificate_array: conteiner.CertificateConteiner):
    certificate_array.clear_log()


def menu():
    menu_parameters = {'exit': menu_exit, 'load': menu_load, 'set_answer_file': menu_set_answer_file,
                       'set_log_file': menu_set_log_file, 'add': menu_add, 'remove': menu_remove, 'change': menu_change,
                       'find': menu_find, 'sort': menu_sort, 'clear': menu_clear, 'clear_log_file': menu_clear_log}

    text = 'exit - вийти з програми\n' \
           'load - зчитати масив сертефікатів з файла\n' \
           'set_answer_file - задати файл для відображення масиву\n' \
           'set_log_file - задати файл для історії змін\n' \
           'add - додати сертифікат\n' \
           'remove - видалити сертефікат з масиву за id\n' \
           'change - змінити параметри сертефіката за його id\n' \
           'find - знайти сертефікати масиву, в яких фігурує певний рядок\n' \
           'sort - сортувати\n' \
           'clear - очистити масив сертефікатів\n' \
           'clear_log_file - очистити файл історії\n'

    while True:
        certificate_array = conteiner.CertificateConteiner()
        variant = validation.input_validation(text, validation.is_menu, list(menu_parameters.keys()))
        menu_parameters[variant](certificate_array)


file = open('answer.txt', 'w')
file.write('')
file.close()
menu()