import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

def set_graph(slider_label='', fr=0, to=0, precision=0, scale_set=0):
    slider_label.set(slider_label)
    x_scale.config(from_=fr, to=to, resolution=precision)  # Используем именованные аргументы
    x_scale.set(scale_set)
    update_graph(str(scale_set))  # Передаём значение как строку

def select_a_vs_m():
    global current_plot_type
    current_plot_type = 'a_vs_m'
    set_graph(
        slider_label='Выберите значение l (м)',
        fr=0.1,
        to=10.0,
        precision=0.1,
        scale_set=l
    )

def select_y_equals_x_squared():
    global current_plot_type
    current_plot_type = 'v_vs_a'
    set_graph(
        slider_label='Выберите значение x',
        fr=0.0,
        to=10.0,
        precision=0.1,
        scale_set=5.0
    )

def save_graph():
    fig.savefig("graph.png")

# Функция для настройки графика
def draw_funk(title='График функции', xlabel='x', y_label='y', x_lim=(0, 11), y_lim=(0, 20), grid=True):
    ax.set_title(title)          # Установка заголовка графика
    ax.set_xlabel(xlabel)        # Установка метки оси x
    ax.set_ylabel(y_label)       # Установка метки оси y
    ax.set_xlim(x_lim)           # Установка фиксированных пределов по оси x
    ax.set_ylim(y_lim)           # Установка фиксированных пределов по оси y
    ax.grid(grid)                # Включение сетки

def update_graph(val):
    global current_plot_type
    ax.cla()  # Очистка предыдущего графика
    selected = float(val)

    if current_plot_type == 'a_vs_m':
        argument = 1 - (m**2 * v**2) / (2 * (m + M)**2 * g * selected)
        argument = np.clip(argument, -1, 1)  # Ограничиваем аргумент
        a = np.arccos(argument)
        a = np.degrees(a)  # Переводим радианы в градусы

        ax.plot(m, a, label='a от m при изменении l')
        draw_funk(title='Зависимость угла отклонения от массы пули',
                    xlabel='Macca пули (кг)',
                    y_label='a (градусы)',
                    x_lim=(0, 0.035), y_lim=(0, 180))

    elif current_plot_type == 'v_vs_a':
        m = 0.01  # масса пули, кг
        a = np.arange(0, 14, 0.1)  # углы от 0.1° до 14° с шагом 0.1°
        v = np.sqrt(2 * (m + M)**2 * g * selected * (1 - np.cos(np.radians(a))) / (m**2))

        ax.plot(a, v, label='v = f(a), m = 10 gramm')
        draw_funk(title='Зависимость скорости пули в зависимости от угла отклонения груза',
                    xlabel='a, C',
                    y_label='V, m/c',
                    x_lim=(0, 14), y_lim=(0, 800))
    canvas.draw() # Обновление графика


current_plot_type = 'a_vs_m'

# Параметры системы
M = 10.0    # Масса груза, кг
g = 9.8     # Ускорение свободного падения, м/с²
l = 1.0     # Длина подвеса груза, м
v = 300.0   # Скорость пули, м/с
m = np.arange(0.001, 0.031, 0.001)  # Массы пули от 0.001 кг до 0.03 кг с шагом 0.001 кг

# Создание главного окна
root = tk.Tk()
root.title("Визуализация графиков")
root.state("zoomed")

main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Создание фрейма для графика
graph_frame = ttk.Frame(main_frame)
graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Создание фрейма для кнопок
controls_frame = ttk.Frame(main_frame)
controls_frame.pack(side=tk.RIGHT, fill=tk.Y)

fig, ax = plt.subplots(figsize=(10, 6), dpi=100)

argument_initial = 1 - (m**2 * v**2) / (2 * (m + M)**2 * g * l)
argument_initial = np.clip(argument_initial, -1, 1)  # Ограничиваем аргумент
a_initial = np.arccos(argument_initial)
a_initial = np.degrees(a_initial)

ax.plot(m, a_initial, label='a от m при изменении l')

# Применение настроек графика
draw_funk(title='Зависимость угла отклонения от массы пули',
         xlabel='Macca пули (кг)',
         y_label='a (градусы)',
         x_lim=(0, 0.035), y_lim=(0, 180))

# Встраивание графика в Tkinter
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Создание метки для ползунка
slider_label = tk.StringVar()
slider_label.set("Выберите значение l (м)")
label = ttk.Label(controls_frame, textvariable=slider_label)

# Создание ползунка (Scale)
x_scale = tk.Scale(
    controls_frame,
    from_      = 0.1,          # Минимальное  значение
    to         = 10.0,            # Максимальное значение
    orient     = tk.HORIZONTAL,
    label      = "",
    command    = update_graph,
    length     = 200,
    resolution = 0.1
)
x_scale.set(l)  # Установка начального значения
x_scale.pack(pady=1)

# Создание фрейма для кнопок
button_frame = ttk.Frame(controls_frame)
button_frame.pack(pady=10)

# Создание кнопки для первого графика (a от m)
button_a_vs_m = ttk.Button(button_frame,text="Построить a от m",command=select_a_vs_m)
button_a_vs_m.pack(fill=tk.X, pady=5)

# Создание кнопки для второго графика (y = x^2)
button_y_equals_x_squared = ttk.Button(button_frame,text="Построить y = x²",command=select_y_equals_x_squared)
button_y_equals_x_squared.pack(fill=tk.X, pady=5)

save_button = ttk.Button(controls_frame, text="Сохранить график", command=save_graph)
save_button.pack(pady=10)

# Запуск основного цикла
root.mainloop()
