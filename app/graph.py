import matplotlib.pyplot as plt # Графики
import asyncio


async def build_graph(id, x, y, name_month, name_file):
    fig, ax = plt.subplots(figsize=(20, 10), dpi=100) # Создание объектов фигуры и осей
    bars = ax.bar(x, y, color='lightblue')  # Создание столбчатой диаграммы

    # Выделение осей
    ax.spines['bottom'].set_color('black')
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_color('black')
    ax.spines['left'].set_linewidth(2)

    # Удаление верхней и правой границы
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


    # Добавление надписей на столбцах
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # X позиция надписи
            height,  # Y позиция надписи
            f'{round(height, 2)}',  # Текст надписи
            ha='center',  # Горизонтальное выравнивание
            va='bottom'  # Вертикальное выравнивание
        )
    plt.xticks(x)
    plt.title(f'Общая статистика доход - расход, {name_month}')
    plt.xlabel(name_month)
    plt.ylabel('Суммы')
    plt.grid(axis='y')  # Включение сетки по оси Y
    plt.savefig(f'./graph/{name_file}')
    plt.close()
    return True









async def build_graph_hor(x, y, add_or_del , name_month, name_file):

    plt.figure(figsize=(20, 10), dpi=100, facecolor='w', edgecolor='k', frameon=True) # num='MyFigure', 
    bars = plt.barh(x, y, color='lightblue')  # Создание горизонтальной столбчатой диаграммы
    plt.title(f'Категории {add_or_del}, {name_month}')
    plt.xlabel('Суммы в руб.')
    plt.ylabel(f'Категории {add_or_del}')
    plt.grid(axis='x')  # Включение сетки по оси X

    # Добавление текста к каждой полосе
    for bar in bars:
        plt.text(
            bar.get_width(),       # X координата, начало полосы + её ширина
            bar.get_y() + bar.get_height() / 2,  # Y координата, центр полосы
            f' {round(bar.get_width(), 2)}', # Текст, который будет отображаться (значение Y)
            va='center'            # Вертикальное выравнивание по центру
        )

    plt.savefig(f'./graph/{name_file}')
    plt.close()
    return True




























# if __name__ == "__main__":
#     asyncio.run(build_graph_hor())











    # График кривой 
    # # Пример данных для графика
    # x = [1, 2, 3, 4, 5, 6, 7, 8 , 9, 10]
    # y = [300, 0, 0, 0, 2500, 1500, -2600, 0, 0, 3000]

    # # plt.figure()
    # plt.figure(num='MyFigure', figsize=(20, 10), dpi=100, facecolor='w', edgecolor='k', frameon=True)
    # plt.plot(x, y)
    # plt.title('График дохода')
    # plt.xlabel('Число месяца') # X
    # plt.ylabel('Доход в руб.') # Y
    # plt.grid(True)
    # plt.savefig('./graph/graph.png')  # Сохранение графика в файл
    # plt.close()  # Закрытие объекта figure, чтобы освободить память


    # График горизонтальными колонами
    # plt.figure(num='MyFigure', figsize=(20, 10), dpi=100, facecolor='w', edgecolor='k', frameon=True)
    # plt.barh(x, y, color='green')  # Создание горизонтальной столбчатой диаграммы
    # plt.title('График уровней')
    # plt.xlabel('Значения')
    # plt.ylabel('Уровни')
    # plt.grid(axis='x')  # Включение сетки по оси X
    # plt.savefig('levels_horizontal.png')
    # plt.close()


    # if __name__ == "__main__":
#     asyncio.run(build_graph())