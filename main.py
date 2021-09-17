# right->down->left->up == 0->1->2->3
class spiral_trail:
    i = 0
    j = 0
    n = 0
    matrix = []
    direction = 0

    def __init__(self, n:int):
        self.matrix = [[0] * n for i in range(n)]
        self.n = n

    def direction_change(self):
        i = self.i
        j = self.j
        if self.direction in (0, 2):
            j += (1 if self.direction == 0 else -1)
        else:
            i += (1 if self.direction == 1 else -1)

        if not (0 <= i < self.n and 0 <= j < self.n and self.matrix[i][j] == 0):
            self.direction = (self.direction + 1) % 4

    def next_step(self):
        if self.direction in (0, 2):
            self.j += (1 if self.direction == 0 else -1)
        else:
            self.i += (1 if self.direction == 1 else -1)

    def set_value(self, val:int):
        self.matrix[self.i][self.j] = val



def main_function(n:int):
    spiral = spiral_trail(n)
    for i in range(1, n**2 + 1):
        spiral.set_value(i)
        spiral.direction_change()
        spiral.next_step()

    return spiral.matrix

def input_natural_number():
    while True:
        try:
            n = int(input())
            if n <= 0 and n != -1:
                int('error')
            return n
        except ValueError:
            print('Ввід не правильний, спробуйте йще раз')


def output(n:int, matrix):
    for i in range(n):
        print(matrix[i])
    print()


print('Введіть одне натуральне число n(для виходу з програми введіть -1)')
while True:
    n = input_natural_number()
    if n == -1:
        print('Програма закінчила свою роботу')
        exit()
    output(n, main_function(n))
    print('Для продовження роботи введіть йще одне число, або -1 для виходу з програми')