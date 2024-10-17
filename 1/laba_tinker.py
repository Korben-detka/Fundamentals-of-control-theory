import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

def save_graph():
    fig.savefig("graph.png")

def draw_funk(title='График функции', xlabel='x', y_label='y', x_lim=(0, 11), y_lim=(0, 20), grid=True):
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(y_label)
    ax.set_xlim(x_lim)
    if y_lim:
        ax.set_ylim(y_lim)
    ax.grid(grid)

def update_graph(val):
    global current_plot_type, v
    ax.cla()
    selected = float(val)

    if current_plot_type == 'a_vs_m':
        argument = 1 - (m**2 * v**2) / (2 * (m + M)**2 * g * selected)
        argument = np.clip(argument, -1, 1)
        a_values = np.arccos(argument)
        a_values = np.degrees(a_values)

        ax.plot(m, a_values, label='a от m при изменении l')
        draw_funk(title='Зависимость угла отклонения от массы пули',
                  xlabel='Масса пули (кг)',
                  y_label='a (градусы)',
                  x_lim=(0, 0.035), y_lim=(0, 180))
        ax.legend()
    elif current_plot_type == 'v_vs_a':
        m_value = 0.01
        a_values = np.arange(0, 14, 0.1)
        v_values = np.sqrt(2 * (m_value + M)**2 * g * selected * (1 - np.cos(np.radians(a_values))) / (m_value**2))

        ax.plot(a_values, v_values, label='v = f(a), m = 10 грамм')
        draw_funk(title='Зависимость скорости пули от угла отклонения груза',
                  xlabel='a, градусы',
                  y_label='V, м/с',
                  x_lim=(0, 14), y_lim=(0, 800))
        ax.legend()
    canvas.draw()

def select_a_vs_m():
    global current_plot_type, x_scale
    current_plot_type = 'a_vs_m'

    # Очистите settings_frame
    for widget in settings_frame.winfo_children():
        widget.destroy()

    # Создайте метку и ползунок в settings_frame
    slider_label = tk.StringVar()
    slider_label.set("Выберите значение l (м)")
    label = ttk.Label(settings_frame, textvariable=slider_label)
    label.pack(pady=5)

    x_scale = tk.Scale(
        settings_frame,
        from_=0.1,
        to=10.0,
        orient=tk.HORIZONTAL,
        command=update_graph,
        length=200,
        resolution=0.1
    )
    x_scale.set(l)
    x_scale.pack(pady=5)

    save_button = ttk.Button(settings_frame, text="Сохранить график", command=save_graph)
    save_button.pack(pady=10)

    # Обновите график с текущим значением ползунка
    update_graph(x_scale.get())

def select_y_equals_x_squared():
    global current_plot_type, x_scale
    current_plot_type = 'v_vs_a'

    # Очистите settings_frame
    for widget in settings_frame.winfo_children():
        widget.destroy()
        #Этот цикл проходит по всем дочерним виджетам контейнера settings_frame и удаляет их с помощью метода
    # Создайте метку и ползунок в settings_frame
    slider_label = tk.StringVar()
    slider_label.set("Выберите значение l")
    label = ttk.Label(settings_frame, textvariable=slider_label)
    label.pack(pady=5)

    x_scale = tk.Scale(
        settings_frame,
        from_=0.1,
        to=10.0,
        orient=tk.HORIZONTAL,
        command=update_graph,
        length=200,
        resolution=0.1
    )
    x_scale.set(1.0)
    x_scale.pack(pady=5)

    save_button = ttk.Button(settings_frame, text="Сохранить график", command=save_graph)
    save_button.pack(pady=10)

    # Обновите график с текущим значением ползунка
    update_graph(x_scale.get())

def select_custom_function():
    global current_plot_type
    current_plot_type = 'custom_function'

    # Очистите settings_frame
    for widget in settings_frame.winfo_children():
        widget.destroy()

    # Создаем виджеты для ввода выражения
    expression_label = ttk.Label(settings_frame, text="Введите функцию от x:")
    expression_label.pack(pady=5)

    expression_entry = ttk.Entry(settings_frame)
    expression_entry.pack(pady=5)

    # Фрейм для ввода пределов оси X
    xlim_frame = ttk.Frame(settings_frame)
    xlim_frame.pack(pady=5)

    xlim_label = ttk.Label(xlim_frame, text="Пределы оси X:")
    xlim_label.pack(side=tk.LEFT)

    x_min_entry = ttk.Entry(xlim_frame, width=5)
    x_min_entry.pack(side=tk.LEFT, padx=2)
    x_min_entry.insert(0, "-10")  # Значение по умолчанию

    x_max_entry = ttk.Entry(xlim_frame, width=5)
    x_max_entry.pack(side=tk.LEFT, padx=2)
    x_max_entry.insert(0, "10")  # Значение по умолчанию

    # Фрейм для ввода пределов оси Y
    ylim_frame = ttk.Frame(settings_frame)
    ylim_frame.pack(pady=5)

    ylim_label = ttk.Label(ylim_frame, text="Пределы оси Y:")
    ylim_label.pack(side=tk.LEFT)

    y_min_entry = ttk.Entry(ylim_frame, width=5)
    y_min_entry.pack(side=tk.LEFT, padx=2)
    y_min_entry.insert(0, "")  # Оставляем пустым по умолчанию

    y_max_entry = ttk.Entry(ylim_frame, width=5)
    y_max_entry.pack(side=tk.LEFT, padx=2)
    y_max_entry.insert(0, "")  # Оставляем пустым по умолчанию

    # Фрейм для ввода точности
    precision_frame = ttk.Frame(settings_frame)
    precision_frame.pack(pady=5)

    precision_label = ttk.Label(precision_frame, text="Точность (шаг):")
    precision_label.pack(side=tk.LEFT)

    precision_entry = ttk.Entry(precision_frame, width=10)
    precision_entry.pack(side=tk.LEFT, padx=2)
    precision_entry.insert(0, "0.1")  # Значение по умолчанию

    # Кнопка для построения графика
    plot_button = ttk.Button(settings_frame, text="Построить график", command=lambda: plot_custom_function(
        expression_entry.get(),
        x_min_entry.get(),
        x_max_entry.get(),
        y_min_entry.get(),
        y_max_entry.get(),
        precision_entry.get()
    ))
    plot_button.pack(pady=5)

    save_button = ttk.Button(settings_frame, text="Сохранить график", command=save_graph)
    save_button.pack(pady=10)

    # Очистите график при выборе нового варианта
    ax.cla()
    canvas.draw()



def plot_custom_function(expression, x_min_str, x_max_str, y_min_str, y_max_str, precision_str):
    ax.cla()

    # Обработка пределов оси X
    try:
        x_min = float(x_min_str)
        x_max = float(x_max_str)
        if x_min >= x_max:
            raise ValueError("Минимальный предел X должен быть меньше максимального")
    except ValueError as e:
        print(f"Ошибка в вводе пределов оси X: {e}")
        return

    # Обработка точности
    try:
        precision = float(precision_str)
        if precision <= 0:
            raise ValueError("Точность должна быть положительным числом")
    except ValueError as e:
        print(f"Ошибка в вводе точности: {e}")
        return

    # Вычисление количества точек на основе точности
    num_points = int((x_max - x_min) / precision) + 1
    if num_points > 1000001:
        print("Слишком большое количество точек. Увеличьте шаг.")
        return

    x = np.linspace(x_min, x_max, num_points)

    # Обработка пределов оси Y
    y_lim = None
    if y_min_str and y_max_str:
        try:
            y_min = float(y_min_str)
            y_max = float(y_max_str)
            if y_min >= y_max:
                raise ValueError("Минимальный предел Y должен быть меньше максимального")
            y_lim = (y_min, y_max)
        except ValueError as e:
            print(f"Ошибка в вводе пределов оси Y: {e}")
            return

    # Разрешенные функции и переменные
    allowed_names = {}
    allowed_names['x'] = x
    for key in dir(np):
        if not key.startswith("_"):
            allowed_names[key] = getattr(np, key)

    try:
        y = eval(expression, {"__builtins__": None}, allowed_names)
        ax.plot(x, y, label=expression)
        ax.legend()
        draw_funk(title='Пользовательская функция', xlabel='x', y_label='y', x_lim=(x_min, x_max), y_lim=y_lim)
        canvas.draw()
    except Exception as e:
        print(f"Ошибка при вычислении функции: {e}")



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

# Создание фрейма для контролов
controls_frame = ttk.Frame(main_frame)
controls_frame.pack(side=tk.RIGHT, fill=tk.Y)

# Создание фрейма для кнопок
button_frame = ttk.Frame(controls_frame)
button_frame.pack(pady=10)

# Создание фрейма для настроек графика
settings_frame = ttk.Frame(controls_frame)
settings_frame.pack(pady=10)

# Кнопки для выбора графика
button_a_vs_m = ttk.Button(button_frame, text="Построить a от m", command=select_a_vs_m)
button_a_vs_m.pack(fill=tk.X, pady=5) # fill=tk.X = кнопка будет расширяться по оси X
                                      # pady=5 отступы вертикальные

button_y_equals_x_squared = ttk.Button(button_frame, text="Построить v от a", command=select_y_equals_x_squared)
button_y_equals_x_squared.pack(fill=tk.X, pady=5)

button_custom = ttk.Button(button_frame, text="Свой вариант", command=select_custom_function)
button_custom.pack(fill=tk.X, pady=5)

# Создание фигуры и оси для графика
fig, ax = plt.subplots(figsize=(10, 6), dpi=100)

# Начальный график
argument_initial = 1 - (m**2 * v**2) / (2 * (m + M)**2 * g * l)
argument_initial = np.clip(argument_initial, -1, 1)
a_initial = np.arccos(argument_initial)
a_initial = np.degrees(a_initial)

ax.plot(m, a_initial, label='a от m при изменении l')

draw_funk(title='Зависимость угла отклонения от массы пули',
          xlabel='Масса пули (кг)',
          y_label='a (градусы)',
          x_lim=(0, 0.035), y_lim=(0, 180))
ax.legend()

canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Инициализация настроек для начального графика
select_a_vs_m()

# Запуск основного цикла
root.mainloop()
