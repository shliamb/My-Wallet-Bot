import matplotlib.pyplot as plt # Графики
import asyncio


async def build_graph(id, x, y, name_month):
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
            f'{height}',  # Текст надписи
            ha='center',  # Горизонтальное выравнивание
            va='bottom'  # Вертикальное выравнивание
        )
    plt.xticks(x)
    plt.title('Общая статистика доход - расход по дням текущего месяца')
    plt.xlabel(name_month)
    plt.ylabel('Суммы')
    plt.grid(axis='y')  # Включение сетки по оси Y
    plt.savefig(f'./graph/graph_{id}.png')
    plt.close()
    return True




if __name__ == "__main__":
    asyncio.run(build_graph())






















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