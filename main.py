import vaccine_class
import validation


def menu_load(certificate_array : vaccine_class.CertificateConteiner):
    variant = validation.input_validation('choose - для вибору файлу\n'
                                          'default - стандартний файл(input.txt)', validation.is_menu,
                                          'choose', 'default')
    file = 'input.txt'
    if variant == 'choose':
        file = validation.input_validation('Введіть назву файла', validation.is_file)
    certificate_array.input_from_file(file)


def menu_set_answer_file(certificate_array : vaccine_class.CertificateConteiner):
    file = validation.input_validation('Введіть назву файла', validation.is_file)
    certificate_array.answer_file = file


def menu_set_log_file(certificate_array : vaccine_class.CertificateConteiner):
    file = validation.input_validation('Введіть назву файла', validation.is_file)
    certificate_array.log_file = file


def menu_add(certificate_array: vaccine_class.CertificateConteiner):
    certificate = vaccine_class.COVID_CERTIFICATE()
    certificate.input()
    certificate_array.append(certificate)


def menu_remove(certificate_array: vaccine_class.CertificateConteiner):
    id = validation.input_validation('Введіть іd сертефікату для видалення')
    certificate_array.remove(id)


def menu_change(certificate_array: vaccine_class.CertificateConteiner):
    id = validation.input_validation('Введіть id сертифікату до зміни', validation.is_in_list,
                                     certificate_array.list_of_id)
    changes = []
    while True:
        variant = validation.input_validation('next - ввести настпну зміну\n'
                                              'stop - припинити вводити зміни')
        if variant == 'stop':
            certificate_array.change_by_id(id, changes)
            return 0
        name = input('Введіть назву поля, що хочете змінити\n')
        val = input('Введіть нове значення\n')
        changes.append(name + '=' + val)


def menu_find(certificate_array: vaccine_class.CertificateConteiner):
    to_find = input('Введіть рядок для пошуку, регістр важливий\n')
    certificate_array.find_part(to_find)


def menu_sort(certificate_array: vaccine_class.CertificateConteiner):
    certificate_array.sort()


def menu_clear(certificate_array: vaccine_class.CertificateConteiner):
    certificate_array.clear()


def menu_clear_log(certificate_array: vaccine_class.CertificateConteiner):
    certificate_array.clear_log()


def menu():
    while True:
        certificate_array = vaccine_class.CertificateConteiner()
        variant = validation.input_validation('exit - вийти з програми\n'
                                              'load - зчитати масив сертефікатів з файла\n'
                                              'set_answer_file - задати файл для відображення масиву\n'
                                              'set_log_file - задати файл для історії змін\n'
                                              'add - додати сертифікат\n'
                                              'remove - видалити сертефікат з масиву за id\n'
                                              'change - змінити параметри сертефіката за його id\n'
                                              'find - знайти сертефікати масиву, в яких фігурує певний рядок\n'
                                              'sort - сортувати\n'
                                              'clear - очистити масив сертефікатів\n'
                                              'clear_log_file - очистити файл історії\n',
                                              validation.is_menu,
                                              'exit', 'load', 'set_answer_file', 'set_log_file', 'change', 'remove',
                                              'add',
                                              'find', 'sort', 'clear', 'clear_log_file')
        if variant == 'exit':
            exit(0)

        if variant == 'load':
            menu_load(certificate_array)

        if variant == 'set_answer_file':
            menu_set_answer_file(certificate_array)

        if variant == 'set_log_file':
            menu_set_log_file(certificate_array)

        if variant == 'add':
            menu_add(certificate_array)

        if variant == 'remove':
            menu_remove(certificate_array)

        if variant == 'change':
            menu_change(certificate_array)

        if variant == 'find':
            menu_find(certificate_array)

        if variant == 'sort':
            menu_sort(certificate_array)

        if variant == 'clear':
            menu_clear(certificate_array)

        if variant == 'clear_log_file':
            menu_clear_log(certificate_array)


file = open('answer.txt', 'w')
file.write('')
file.close()
menu()