import tkinter as tk
from tkinter import messagebox
from tkinter import *
import numpy as np
import time

# Глобальные переменные для таймера
start_time   = 0
elapsed_time = 0
running      = False
reset        = False
depth        = 0

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Обработка события закрытия окна
        self.title("Визуализация графиков")
        self.state("zoomed")
        self.resizable(True,True)

        self.main_frame = Frame(master=self)
        self.main_frame.pack(fill=BOTH, expand=True)

        self.graph_frame = Frame(master=self.main_frame,relief=SUNKEN, borderwidth=5)
        self.graph_frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.controls_frame = Frame(self.main_frame,width=250)
        self.controls_frame.pack(side=RIGHT, fill=Y)
        self.controls_frame.pack_propagate(False)

        self.button_frame = Frame(self.controls_frame)
        self.button_frame.pack(pady=10)

        labels_and_defaults = [
            ("Диаметр лазера (мм):", "5"),
            ("Толщина бруска (мм):", "10"),
            ("Мощность Лазера (Вт):", "500"),
            ("Плотность бруска (кг/м^3):", "7850")
        ]

        entry_fields = []
        for label_text, default_value in labels_and_defaults:
            self.label = Label(self.button_frame, text=label_text)
            self.label.pack(anchor='w', pady=(10, 0))  # Добавляем отступ сверху для разделения от предыдущих элементов
            self.entry = Entry(self.button_frame)
            self.entry.insert(0, default_value)  # Устанавливаем дефолтное значение в поле ввода
            self.entry.pack(fill=X, pady=(0, 5))  # Добавляем отступ снизу между полями ввода
            entry_fields.append(self.entry)


        self.button_start_time= Button(self.button_frame, text="start", command=lambda: self.start_timer(entry_fields))
        self.button_start_time.pack(fill=X, pady=5)

        self.button_stop_time = Button(self.button_frame, text="stop", command=self.stop_timer)
        self.button_stop_time.pack(fill=X, pady=5)

        self.button_reset = Button(self.button_frame, text="reset", command=lambda: self.reset_timer(entry_fields))
        self.button_reset.pack(fill=X,pady=5)

        # Метка для отображения времени работы
        self.time_label = Label(self.button_frame, text="Время работы: 0.00 мс")
        self.time_label.pack(pady=10)

        self.depth_label = Label(self.button_frame, text="Depth:")
        self.depth_label.pack(pady=10)
        self.result_label = Label(self.button_frame, text="Металл обрабатывается")
        self.result_label.pack(pady=10)

    def update_timer(self,entry_fields):
        if reset:
            current_time = 0
            self.time_label.config(text=f"Время работы: {current_time * 1000:.2f} мс")  # Обновляем таймер в мс
            self.calculate_depth(entry_fields,0)  # Обновляем расчет глубины при каждом тике
        if running:
            current_time = time.perf_counter() - start_time
            self.time_label.config(text=f"Время работы: {current_time * 1000:.2f} мс")  # Обновляем таймер в мс
            self.calculate_depth(entry_fields,0.001)  # Обновляем расчет глубины при каждом тике
            self.time_label.after(10, lambda: self.update_timer(entry_fields))  # Передаем entry_fields при каждом обновлении

    def start_timer(self, entry_fields):
        global start_time, running
        if not running:
            start_time = time.perf_counter() - elapsed_time  # Запускаем или возобновляем таймер
            running = True
            self.update_timer(entry_fields)

    def stop_timer(self):
        global elapsed_time, running
        if running:
            elapsed_time = time.perf_counter() - start_time  # Сохраняем текущее время
            running = False

    def reset_timer(self, entry_fields):
        global start_time, elapsed_time, running,depth,reset
        depth = 0
        reset = 1
        start_time = 0
        elapsed_time = 0
        running = False
        self.update_timer(entry_fields)
        reset = 0


    def calculate_depth(self, entry_fields,elapsed_time):
        # Получаем данные от пользователя
        global depth,reset
        try:
            D = float(entry_fields[0].get()) / 1000  # Конвертируем диаметр в метры
            L = float(entry_fields[1].get()) / 1000  # Конвертируем толщину в метры
            W = float(entry_fields[2].get())  # Мощность лазера в ваттах
            rho = float(entry_fields[3].get())  # Плотность материала в кг/м^3
        except ValueError:
            self.stop_timer()  # Вызываем функцию stop_timer() при ошибке
            return
        # Далее идёт логика работы с корректными значениями
        # Например:
        # process_calculation(D, L, W, rho)
        h = 1000000  # Константа для расчета

        # Расчет площади поперечного сечения
        S = np.pi * (D / 2) ** 2
        # Рассчитываем глубину, до которой металл будет испарен
        d_depth = (W * elapsed_time) / (h * S * rho)
        depth = depth + d_depth
        if reset:
            self.result_label.config(text="Металл обрабатывается")
        elif depth >= L:
            depth = L
            self.result_label.config(text=f"Металл полностью испарился. Глубина: {depth:.4f} метров")
        self.depth_label.config(text=f"Глубина прожига: {depth:.4f} м")  # Обновляем таймер в мс
        self.update_bar_height(depth, L)

    def update_bar_height(self, depth, L):
        # Рассчитываем, насколько высота бруска должна уменьшиться
        if L != 0:
            new_height = 350 - (300 * (depth / L))  # 300 — начальная высота бруска
            canvas.coords(bar, bar_x, 50, bar_x + 100, new_height)
        else:
            self.stop_timer()
        # Нижняя граница бруска поднимается, верхняя граница остается на месте (на уровне 50 пикселей)


    def on_close(self):
        print("Окно закрывается, завершаем программу.")
        main_window.quit()  # Завершает mainloop
        main_window.destroy()  # Закрывает окно

    def save_graph(self):
        self.graph_frame.savefig("graph.png")

    def create_graphics(self, graph_frame):
        def move_laser(event):
            if event.keysym in ('Left', 'a'):
                canvas.move(laser, -1, 0)  # Движение лазера влево
            elif event.keysym in ('Right', 'd'):
                canvas.move(laser, 1, 0)   # Движение лазера вправо

        # Создаем Canvas для отрисовки графических элементов внутри graph_frame
        global canvas, bar, bar_x  # Используем глобальные переменные для бруска
        height_C = 400

        canvas = Canvas(self.graph_frame, width=400, height=height_C, bg="white")
        canvas.pack(fill=BOTH, expand=True)

        # Рисуем брусок по центру окна
        bar_x = (400 - 100) / 2  # Начальная позиция для центра бруска
        bar = canvas.create_rectangle(bar_x, 50, bar_x + 100, 350, fill="#7b7b7b")

        # Создаем лазер внизу окна
        laser = canvas.create_rectangle(190, 380, 210, 400, fill="red")

        # Привязываем события клавиш к функции перемещения лазера
        self.graph_frame.bind_all('<Left>', move_laser)
        self.graph_frame.bind_all('<Right>', move_laser)
        self.graph_frame.bind_all('a', move_laser)
        self.graph_frame.bind_all('d', move_laser)

if __name__ == "__main__":
    main_window = App()
    main_window.create_graphics(main_window.graph_frame)


# Создание главного окна


main_window.mainloop()
