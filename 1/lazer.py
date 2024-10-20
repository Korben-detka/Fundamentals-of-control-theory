import customtkinter as ctk
import numpy as np
import time
import os

d_t = 10 # m seconds

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.depth = 0
        self.error = False
        self.start_time   = 0
        self.elapsed_time = 0
        self.running      = False
        self.reset        = False
        self.entry_fields = []
        self.L = 0
        self.t = d_t
        self.t_ms = self.t / 1000

        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Обработка события закрытия окна
        self.title("Визуализация графиков")
        self.state("zoomed")
        self.resizable(True,True)

        self.main_frame = ctk.CTkFrame(master=self)
        self.main_frame.pack(fill="both", expand=True)

        self.graph_frame = ctk.CTkFrame(master=self.main_frame, border_width=5)
        self.graph_frame.pack(side="left", fill="both", expand=True)

        self.controls_frame = ctk.CTkFrame(self.main_frame, width=300)
        self.controls_frame.pack(side="right", fill="y",expand=False)
        self.controls_frame.pack_propagate(False)

        self.button_frame = ctk.CTkFrame(self.controls_frame)
        self.button_frame.pack(pady=3,fill="x",padx = 30)

        labels_and_defaults = [
            ("Диаметр лазера (мм):", "5"),
            ("Толщина бруска (мм):", "10"),
            ("Мощность Лазера (Вт):", "200"),
            ("Плотность бруска (кг/м^3):", "7850")
        ]

        for label_text, default_value in labels_and_defaults:
            self.label = ctk.CTkLabel(self.button_frame, text=label_text)
            self.label.pack(anchor='w', pady=(5, 0),padx=25)  # Добавляем отступ сверху для разделения от предыдущих элементов
            self.entry = ctk.CTkEntry(self.button_frame)
            self.entry.insert(0, default_value)  # Устанавливаем дефолтное значение в поле ввода
            self.entry.pack(fill="x", padx = 20)  # Добавляем отступ снизу между полями ввода
            self.entry_fields.append(self.entry)

        self.button_start_lazer = ctk.CTkButton(self.button_frame, text="Start",corner_radius=20,command=self.start_lazer)
        self.button_start_lazer.pack(pady=(20,10))

        self.button_stop_lazer = ctk.CTkButton(self.button_frame, text="Stop",corner_radius=20, command=self.stop_timer)
        self.button_stop_lazer.pack(pady=10)

        self.button_reset = ctk.CTkButton(self.button_frame, text="Reset",corner_radius=20, command=self.reset_timer)
        self.button_reset.pack(pady=10)

        # Метка для отображения времени работы
        self.time_label = ctk.CTkLabel(self.button_frame, text="Время работы: 0.00 мс")
        self.time_label.pack(pady=10)

        self.depth_label = ctk.CTkLabel(self.button_frame, text="Глубина:")
        self.depth_label.pack(pady=10)

        self.result_label = ctk.CTkLabel(self.button_frame, text="Металл готов к обработке",width=200)
        self.result_label.pack(pady=10,expand=False,fill=None)

        try:
            self.L = float(self.entry_fields[1].get()) / 1000  # Конвертируем толщину в метры
        except ValueError:
            print("Enter correct value of L")
            return

    def err(self):
        self.error = True

    def start_lazer(self):
        self.error = False
        self.validate_inputs()
        if not self.error:
            self.entry_fields[1].configure(state="readonly")
            self.start_timer()
            self.update_values()

    def validate_inputs(self):
        try:
            # Преобразуем все данные перед выполнением операций
            a0 = float(self.entry_fields[0].get())
            a1 = float(self.entry_fields[1].get()) / 1000  # Конвертируем толщину в метры
            float(self.entry_fields[2].get())
            a3 = float(self.entry_fields[3].get())
            if a0 == 0:
                self.error = True
                print("Диаметр лазера не может быть 0")
            if a1 == 0:
                self.error = True
                print("Толщина бруска не может быть 0")
            if a3 == 0:
                self.error = True
                print("Плотность бруска не может быть 0")
            return True  # Ввод валиден
        except ValueError:
            self.err()
            print("Ошибка ввода данных. Пожалуйста, проверьте вводимые значения.")
            return False  # Ввод не валиден

    def start_timer(self):
        if not self.running:
            print("Timer in on")
            self.running = True
            self.start_time = time.perf_counter() - self.elapsed_time  # Запускаем или возобновляем таймер

    def update_values(self):
        self.update_timer()
        self.calculate_depth()
        self.update_bar_height()
        if self.running:
            self.after(self.t,self.update_values)

    def update_timer(self):
        if self.reset:
            self.time_label.configure(text=f"Время работы: {0:.2f} мс")  # Обновляем таймер в мс
        if self.running:
            current_time = time.perf_counter() - self.start_time
            self.time_label.configure(text=f"Время работы: {current_time * 1000:.2f} мс")  # Обновляем таймер в мс

    def stop_timer(self):
        if self.running:
            print("Timer in off")
            self.elapsed_time = time.perf_counter() - self.start_time  # Сохраняем текущее время
            self.running = False

    def reset_timer(self):
        self.reset = 1

        self.running = False
        self.depth = 0
        self.start_time = 0
        self.elapsed_time = 0

        saved_t = self.t_ms
        self.t_ms = 0
        self.update_values()
        self.t_ms = saved_t

        self.reset = 0
        self.entry_fields[1].configure(state="normal")
        print("Reset is Done")

    def calculate_depth(self):
        try:
            D = float(self.entry_fields[0].get()) / 1000  # Конвертируем диаметр в метры
            W = float(self.entry_fields[2].get())  # Мощность лазера в ваттах
            rho = float(self.entry_fields[3].get())  # Плотность материала в кг/м^3
        except ValueError:
            self.stop_timer()  # Останавливаем таймер при ошибке
            return

        h = 1000000  # Константа для расчета

        # Расчет площади поперечного сечения
        S = np.pi * (D / 2) ** 2
        # Рассчитываем глубину
        d_depth = (W * self.t_ms) / (h * S * rho)
        self.depth = self.depth + d_depth

        if self.reset:
            self.result_label.configure(text="Металл обрабатывается")
        elif self.depth >= self.L:
            self.depth = self.L
            self.result_label.configure(text=f"Металл частично/полностью испарился. Глубина: {self.depth:.4f} метров",wraplength=220)
        self.depth_label.configure(text=f"Максимальная глубина прожега: {self.depth:.4f} м",wraplength=220)

    def update_bar_height(self):
        # Получаем текущую ширину холста для вычисления центра
        canvas_width = canvas.winfo_width()

        # Вычисляем новые координаты для высоты bar в зависимости от значения self.depth и self.L
        new_height = 350 - (300 * (self.depth / self.L))  # 300 — начальная высота бруска

        # Обновляем координаты bar, чтобы он оставался центрированным по горизонтали
        bar_width = 100
        bar_x = (canvas_width - bar_width) / 2  # Пересчитываем положение по центру
        canvas.coords(bar, bar_x, 50, bar_x + bar_width, new_height)

    def update_bar_height(self):
        # Получаем текущую ширину и высоту холста для вычисления центра
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        high_otstup = round(canvas_height * 0.05)  # Верхний отступ
        bar_width = round(canvas_width * 0.8)      # Ширина бруска
        bar_high = round(canvas_height * 0.8)      # Начальная высота бруска

        # Вычисляем новую высоту бруска в зависимости от значения self.depth и self.L
        new_height = bar_high * (self.depth / self.L)  # Новый расчет высоты

        # Обновляем координаты bar, чтобы он оставался центрированным по горизонтали
        bar_x = (canvas_width - bar_width) / 2
        canvas.coords(bar, bar_x, high_otstup, bar_x + bar_width, bar_high + high_otstup - new_height)




    def on_close(self):
        print("Окно закрывается, завершаем программу.")
        main_window.quit()  # Завершает mainloop
        main_window.destroy()  # Закрывает окно

    def save_graph(self):
        self.graph_frame.savefig("graph.png")

    def create_graphics(self):

        def move_laser(event):
            if event.keysym in ('Left', 'a'):
                canvas.move(laser, -1, 0)  # Движение лазера влево
            elif event.keysym in ('Right', 'd'):
                canvas.move(laser, 1, 0)   # Движение лазера вправо

        global canvas, bar, laser
        height_C = 400
        width_C = 400

        canvas = ctk.CTkCanvas(self.graph_frame, width=width_C, height=height_C, bg="white")
        canvas.pack(fill="both", expand=True)

        def update_positions(event=None):
            canvas_width  = canvas.winfo_width()
            canvas_height = canvas.winfo_height()

            high_otstup = round(canvas_height * 0.05)
            laser_size = round(canvas_width * 0.05)
            bar_width = round(canvas_width * 0.8)
            bar_high  = round(canvas_height * 0.8)

            bar_x = (canvas_width - bar_width) / 2
            canvas.coords(bar, bar_x, high_otstup, bar_x + bar_width, bar_high + high_otstup)

            laser_x = (canvas_width - laser_size) / 2
            canvas.coords(laser, laser_x, bar_high + high_otstup, laser_x + laser_size, bar_high + high_otstup + laser_size)

        bar = canvas.create_rectangle(0, 0, 0, 0, fill="#7b7b7b")
        laser = canvas.create_rectangle(0, 0, 0, 0, fill="red")

        canvas.bind("<Configure>", update_positions)

        self.bind('<Left>', move_laser)
        self.bind('<Right>', move_laser)
        self.bind('a', move_laser)
        self.bind('d', move_laser)

        update_positions()




if __name__ == "__main__":

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("green")
    os.system('cls')
    main_window = App()
    main_window.create_graphics()
    main_window.mainloop()
