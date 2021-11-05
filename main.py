import conteiner
import flight_booking
import validation
import flight_booking

def menu_exit(value):
    exit(0)


def menu_load(certificate_array: conteiner.FlightConteiner):
    variant = validation.is_menu(['choose', 'default'], text='choose - для вибору файлу\n'
                                                             'default - стандартний файл(input.txt)', function='input')
    file = 'input.txt'
    if variant == 'choose':
        file = validation.is_file(text='Введіть назву файла', function='input')
    certificate_array.read_from(file)


def menu_add(certificate_array: conteiner.FlightConteiner):
    certificate = flight_booking.FlightBooking()
    certificate.read_from_console()
    certificate_array.append(certificate)


def menu_company(certificate_array: conteiner.FlightConteiner):
    certificate_array.most_flight()


def menu_time(certificate_array: conteiner.FlightConteiner):
    certificate_array.most_flight()


def menu_print(certificate_array: conteiner.FlightConteiner):
    print(certificate_array)


def menu():
    menu_parameters = {'exit': menu_exit, 'load': menu_load, 'add': menu_add, 'company': menu_company, 'time': menu_time,
                       'print':menu_print}

    text = 'exit - вийти з програми\n' \
           'load - зчитати масив з файла\n' \
           'add - додати політ\n' \
           'remove - видалити сертефікат з масиву за id\n' \
           'company - вивести компанію\n' \
           'time - вивести час\n' \
           'print - вивести\n'
    certificate_array = conteiner.FlightConteiner()
    while True:
        variant = validation.is_menu(list(menu_parameters.keys()), text=text, function='input')
        menu_parameters[variant](certificate_array)


file = open('answer.txt', 'w')
file.write('')
file.close()
menu()