import random
import colors as color
from math import fabs
import re
import datetime


def toFixed(num):
    """"Округление"""
    return f'{num:.3f}'


def optimize(n, arr):
    """"Конвертация коэффициентов матрицы во float"""
    i = 0
    while i < n:
        j = 0
        while j <= n:
            arr[i][j] = float(arr[i][j])
            j += 1
        i += 1
    return arr


def file_function(filename):
    """"Функия для файлового ввода значений"""
    try:
        n = -1
        array = []
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if (line != '\n') and (line != ' ') and (line != ' \n'):
                    n += 1
            if n > 20:
                print(color.RED,
                      'В файле превышено количество уравнений! Уменьшите до 20 или менее и попробуйте снова.\n')
                return
        file.close()

        with open(filename, 'r', encoding='utf-8') as file:
            file.readline()
            for row in file:
                line = list(row.split())
                for i in line:
                    # не пропускает числа без точки (7 = 7.0)
                    if (re.search('([-]?\d{1,}\.{1}\d{1,})', i) is None) and (not i.isnumeric()):
                        print(color.RED,
                              'Проверьте формат введенных данных (вещественные числа должны быть разделены точкой).')
                        return
                array.append(list(line))
            file.close()
            compute = Calculator(n, optimize(n, array))
            compute.calculate()
            del compute
    except FileNotFoundError:
        print(color.RED, 'Файл не найден. Проверьте введенное имя.\n')


def console_function():
    """"Функия для консольного ввода значений"""
    try:
        n = int(input("Введите количество строк в уравнении (число не должно превышать 20):\n>"))
        if (n <= 20) and (n > 1):
            array = []
            print(color.BLUE, "Введите строки в следующем формате:")
            print("ai1, ai2, ai3, ... ain bi")
            for i in range(n):
                while True:
                    line = list((input(str(i + 1) + ': ').split()))
                    if int(len(line) != n + 1):
                        print(color.RED,
                              "Убедитесь в правильности ввода количества значений. \nПроверьте правильность ввода и "
                              "попробуйте снова")
                    else:
                        array.append(line)
                        break
            compute = Calculator(n, optimize(n, array))
            compute.calculate()
            del compute
        else:
            print(color.RED, "Проверьте правильность ввода!")
            return
    except ValueError:
        print(color.RED, "Неверные аргументы ввода!")


def generate_function():
    """"Функия для генерации значений матрицы"""
    try:
        array = []
        n = int(input("Введите количество строк в уравнении (число не должно превышать 20):\n>"))
        if (n <= 20) and (n > 1):
            print("Генерирую матрицу...")
            for i in range(n):
                line = [random.randint(-20, 20) + random.uniform(-1, 1) for _ in range(n + 1)]
                array.append(line)
            compute = Calculator(n, optimize(n, array))
            compute.calculate()
            del compute
        else:
            print(color.YELLOW, "Проверьте правильность ввода и попробуйте снова")
    except ValueError:
        print(color.RED, "Неверные аргументы ввода!")


class Calculator:
    n = 0  # количество уравнений/неизвестных
    C = []
    B = []
    coeff = []  # система уравнений
    sum = []
    vector = []  # вектор неизвестных
    det = 0  # определитель матрицы

    def __init__(self, n, coeff):
        self.n = n
        self.coeff = coeff
        self.det = []
        self.total_sum = [0 for i in range(n)]
        self.B = [[0 for i in range(n+1)] for j in range(n+1)]
        self.C = [[0 for i in range(n+1)] for j in range(n+1)]
        for i in range(n):
            for j in range(n+1):
                if i != j:
                    self.C[i][j] = 0
                else:
                    self.C[i][j] = 1

    def calculate(self):
        try:
            print("\nПолученная система:")
            self.print_coeff()
            print("\n")
            self.method_Choleskogo()
            print("\n")
        except ZeroDivisionError:
            return
        except ArithmeticError:
            print(color.RED + "\nНет решений:(\n")
            return

    # Вывод системы на экран
    def print_coeff(self):
        i = 0
        while i < self.n:
            j = 0
            while j < self.n:
                print(" ", toFixed(self.coeff[i][j]), end='')
                j += 1
            print(" ", toFixed(self.coeff[i][-1]), "b[" + str(i + 1) + "]")
            i += 1

    def print_matrix(self, some_list):
        i = 0
        while i < self.n:
            j = 0
            while j < self.n:
                print(" ", toFixed(some_list[i][j]), end='')
                j += 1
            print(" ", toFixed(some_list[i][-1]))
            i += 1

    def method_Choleskogo(self):
        global sum
        for i in range(self.n):
            for j in range(self.n + 1):
                # для B - нижний треугольник
                if i >= j:
                    self.B[i][0] = self.coeff[i][0]
                    if j > 0:
                        sum = 0
                        for k in range(j):
                            sum = sum + self.B[i][k] * self.C[k][j]
                        self.B[i][j] = self.coeff[i][j] - sum
                # для C - верхний треугольник
                if i < j:
                    self.C[0][j] = self.coeff[0][j] / self.B[0][0]
                    if i > 0:
                        sum = 0
                        for k in range(i):
                            sum = sum + self.B[i][k] * self.C[k][j]
                        self.C[i][j] = (self.coeff[i][j] - sum) / self.B[i][i]
        print("Матрица B:")
        self.print_matrix(self.B)
        print("\nМатрица C:")
        self.print_matrix(self.C)
        print("\nСтолбец сумм:")



# def print_vector_x(self):
#     i = 0
#     print('Решение системы:')
#     self.vector.reverse()
#     while i < self.n:
#         print('x[' + str(i + 1) + ']:', self.vector[i])
#         i += 1
#     print('')
#
# # Подсчет невязки r1 ... rn
# def print_residuals(self):
#     i = 0
#     print('Невязки:')
#     while i < self.n:
#         res = 0
#         j = 0
#         while j < self.n:
#             res = res + self.coeff[i][j] * self.vector[j]
#             j += 1
#         res = res - self.coeff[i][-1]
#         i += 1
#         print('Невязка', i, 'строки:', fabs(res))
#     print('')