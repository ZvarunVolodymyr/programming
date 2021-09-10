def is_int_number(num: str):
    if num == '':
        return False

    for i in num:
        if not ('0' <= i <= '9'):
            return False

    return True


def is_float_number(num: str):
    if num == '':
        return False

    count_of_points = 0
    is_first_symbol = True
    has_number = False

    for i in num:
        if i == '-' and is_first_symbol == True and len(num) != 1:
            continue
        is_first_symbol = False

        if not (('0' <= i <= '9' or i == '.' or i == ',') and count_of_points <= 1):
            return False

        if '0' <= i <= '9':
            has_number = True

        if (i == '.' or i == ',') and has_number == True:
            count_of_points += 1
        elif i == '.' or i == ',':
            return False

    return True


def input_number(is_float = False):
    num = 0
    flag = False
    while not flag:
        num = input()
        if is_float:
            if is_float_number(num):
                flag = True
        else:
            if is_int_number(num):
                flag = True

        if flag == False:
            print('Неправильний ввід, спробуйте йще раз')
    return num


def main_function():
    print('Введіть натуральне число n(в рядку має бути тільки число, без лишніх символів)')

    n = int(input_number())
    elements_list = []

    print('Введіть n чисел, кожне число в новому рядку(дійсна частина вказана через . або ,)')

    max = min = float(input_number(True))
    elements_list.append(max)

    for i in range(n - 1):
        num = float(input_number(True))
        elements_list.append(num)

        if min > num:
            min = num

        if max < num:
            max = num

    coefficient = 0
    if elements_list[0] >= 0:
        coefficient = min * min
    else:
        coefficient = max * max

    for i in range(n):
        elements_list[i] *= coefficient

    return elements_list


print(main_function())