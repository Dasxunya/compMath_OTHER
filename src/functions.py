import datetime
import random
import colors as color
import re
from math import fabs


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
    """"Функция для файлового ввода значений"""
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
    """"Функция для консольного ввода значений"""
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
    """"Функция для генерации значений матрицы"""
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
    X = []
    Y = []
    coeff = []  # система уравнений
    sum = []
    vector = []  # вектор неизвестных
    det = 0  # определитель матрицы

    def __init__(self, n, coeff):
        self.n = n
        self.coeff = coeff
        self.det = []
        self.total_sum = [0 for i in range(n)]
        self.X = [0 for i in range(n)]
        self.Y = [0 for i in range(n)]
        self.B = [[0 for i in range(n + 1)] for j in range(n + 1)]
        self.C = [[0 for i in range(n + 2)] for j in range(n + 2)]
        for i in range(n):
            for j in range(n + 2):
                if i != j:
                    self.C[i][j] = 0
                else:
                    self.C[i][j] = 1

    def calculate(self):
        try:
            print("\nПолученная система:")
            self.print_coeff(self.coeff)

            print("\nСтолбец сумм:")
            self.t_sum()

            start = datetime.datetime.now()
            self.method_Choleskogo()
            timedelta = datetime.datetime.now() - start

            print("\nМатрица B:")
            self.print_matrix(self.B)
            print("\nМатрица C | b | Σ:")
            self.print_matrix(self.C)
            print("\nПреобразованный столбец сумм:")
            for i in range(self.n):
                print("Σ[" + str(i + 1) + "] =" + toFixed(self.C[i][self.n + 1]))

            print("\nРезультат:")
            self.calc_res()

            self.print_residuals()
            print("\nВремя работы метода: " + str(timedelta) + "\n")

        except (ZeroDivisionError, ArithmeticError):
            print(color.RED + "\nНет решений:(\n")
            return

    def print_matrix(self, some_list):
        i = 0
        while i < self.n:
            j = 0
            while j < self.n + 1:
                print(" ", toFixed(some_list[i][j]), end='')
                j += 1
            print(" ", toFixed(some_list[i][-1]))
            i += 1

    # Вывод системы на экран
    def print_coeff(self, some_list):
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
            for j in range(self.n + 2):
                # для B - нижний треугольник
                if i >= j:
                    self.B[i][0] = self.coeff[i][0]
                    if j > 0:
                        sum = 0
                        for k in range(j):
                            sum = sum + self.B[i][k] * self.C[k][j]
                        self.B[i][j] = self.coeff[i][j] - sum
                # для C - верхний треугольник
                if (i < j) and (j != self.n + 1):
                    self.C[0][j] = self.coeff[0][j] / self.B[0][0]
                    if i > 0:
                        sum = 0
                        for k in range(i):
                            sum = sum + self.B[i][k] * self.C[k][j]
                        self.C[i][j] = (self.coeff[i][j] - sum) / self.B[i][i]
                # для столбца сумм
                if (j == self.n + 1) and (i < j):
                    self.C[0][self.n + 1] = self.total_sum[0] / self.B[0][0]
                    if i > 0:
                        sum = 0
                        for k in range(i):
                            sum = sum + self.B[i][k] * self.C[k][j]
                        self.C[i][j] = (self.total_sum[i] - sum) / self.B[i][i]

    def t_sum(self):
        for i in range(self.n):
            sum = 0
            for j in range(self.n + 1):
                sum = sum + self.coeff[i][j]
            self.total_sum[i] = sum
            print("\tZ[" + str(i + 1) + "] = " + str(sum))

    def calc_res(self):
        # подсчет Y
        for i in range(self.n):
            self.Y[0] = self.coeff[0][self.n] / self.B[0][0]
            if i > 0:
                sum = 0
                for k in range(i):
                    sum = sum + self.B[i][k] * self.Y[k]
                self.Y[i] = (self.coeff[i][self.n] - sum) / self.B[i][i]
        # подсчет X
        self.X[self.n - 1] = self.Y[self.n - 1]
        i = self.n - 2
        while i > -1:
            k = self.n - 1
            sum = 0
            while k > i:
                sum = sum + self.C[i][k] * self.X[k]
                k -= 1
            self.X[i] = self.Y[i] - sum
            i -= 1
        # вывод результата
        for i in range(self.n):
            print(" Y[" + str(i + 1) + "] = " + toFixed(self.Y[i]) + " X[" + str(i + 1) + "] = " + toFixed(self.X[i]))

    # Подсчет невязки r1 ... rn
    def print_residuals(self):
        i = 0
        print('\nНевязки:')
        while i < self.n:
            res = 0
            j = 0
            while j < self.n:
                res = res + self.coeff[i][j] * self.X[j]
                j += 1
            res = res - self.coeff[i][self.n]
            i += 1
            print('Невязка', i, 'строки:', fabs(res))
