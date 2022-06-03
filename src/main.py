import colors as color
import functions as f
while True:
    try:
        print(color.BLUE, 'Выбери режим ввода для решения уравнения методом Холецкого:')
        print('1 ~ Считывание из файла')
        print('2 ~ Ввод линейной системы вручную')
        print('3 ~ Автоматическая генерация матрицы')
        print('4 ~ Выход')

        number = int(input('\n>'))

        if number == 1:
            print('\nВы выбрали ввод данных через файл:')
            f.file_function(input('Введите имя файла:'))
        elif number == 2:
            print('\nВы выбрали ввод данных через консоль:')
            f.console_function()

        elif number == 3:
            print('\nВы выбрали автоматическую генерацию матрицы:')
            f.generate_function()

        elif number == 4:
            print(color.GREEN + '\nДо встречи :)')
            break

        else:
            print(color.RED, 'Такого пункта не существует... Воспользуйтесь предложенными в меню :)\n')

    except KeyboardInterrupt:
        print(color.RED, '\nПрограмма прервана :(\n')
        exit(1)
    except FileNotFoundError:
        print("Проверьте имя файла\n")
    except:
        print(color.RED, '\nЧто-то пошло не так :(')
