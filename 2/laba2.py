import customtkinter as ctk 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

# Установка темы и режима отображения
ctk.set_appearance_mode("System")  # Режимы: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Темы: "blue", "green", "dark-blue"

class WeatherSimulation(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # Создаем прокручиваемый фрейм для настроек
        self.weather_settings_frame = ctk.CTkScrollableFrame(self)
        self.weather_settings_frame.grid(row=0, column=0, sticky="nsew")

        self.weather_result_frame = ctk.CTkFrame(self)
        self.weather_result_frame.grid(row=0, column=0, sticky="nsew")
        self.weather_result_frame.grid_remove()  # Скрываем результатовый фрейм

        self.weather_settings_frame.columnconfigure(1, weight=1)
        self.weather_settings_frame.rowconfigure(8, weight=1)

        # Состояния погоды
        self.weather_states = ["Солнечно", "Дождь", "Снег", "Облачно", "Ветер"]

        # Поля ввода для вероятностей перехода
        self.transition_entries = {}
        row = 0
        ctk.CTkLabel(self.weather_settings_frame, text="Количество дней:").grid(row=row, column=0, padx=5, pady=5, sticky='e')
        self.days_entry = ctk.CTkEntry(self.weather_settings_frame)
        self.days_entry.grid(row=row, column=1, padx=5, pady=5, sticky='we')
        self.days_entry.insert(0, "365")
        row += 1

        for from_state in self.weather_states:
            ctk.CTkLabel(self.weather_settings_frame, text=f"Вероятности переходов из состояния '{from_state}':", font=('Arial', 12, 'bold')).grid(row=row, column=0, columnspan=2, padx=5, pady=5)
            row += 1
            for to_state in self.weather_states:
                label_text = f"P({from_state} → {to_state}):"
                ctk.CTkLabel(self.weather_settings_frame, text=label_text).grid(row=row, column=0, padx=5, pady=5, sticky='e')
                entry = ctk.CTkEntry(self.weather_settings_frame)
                entry.grid(row=row, column=1, padx=5, pady=5, sticky='we')
                entry.insert(0, "0.2")  # Начальное значение вероятности
                self.transition_entries[(from_state, to_state)] = entry
                row += 1

        ctk.CTkButton(self.weather_settings_frame, text="Смоделировать", command=self.count_weather).grid(row=row, column=0, columnspan=2, padx=5, pady=5)
        row += 1

        # Кнопка для отображения автомата
        ctk.CTkButton(self.weather_settings_frame, text="Показать автомат", command=self.show_automaton).grid(row=row, column=0, columnspan=2, padx=5, pady=5)
        row += 1

        # Метка для вывода ошибок
        self.weather_error_label = ctk.CTkLabel(self.weather_settings_frame, text="", text_color="red")
        self.weather_error_label.grid(row=row, column=0, columnspan=2, padx=5, pady=5)

    def count_weather(self):
        try:
            self.weather_error_label.configure(text="")  # Очистить предыдущие ошибки
            days = int(self.days_entry.get())
            if days <= 0:
                raise ValueError("Количество дней должно быть положительным числом.")

            weather_states = self.weather_states
            current_state = weather_states[0]  # Начинаем с первого состояния
            state_indices = {state: idx for idx, state in enumerate(weather_states)}
            state_counts = np.zeros(len(weather_states))

            # Создание матрицы переходов
            transition_matrix = np.zeros((len(weather_states), len(weather_states)))
            for from_state in weather_states:
                total_prob = 0
                for to_state in weather_states:
                    prob_str = self.transition_entries[(from_state, to_state)].get()
                    try:
                        prob = float(prob_str)
                    except ValueError:
                        raise ValueError(f"Вероятность перехода от {from_state} к {to_state} должна быть числом.")
                    if prob < 0 or prob > 1:
                        raise ValueError(f"Вероятность перехода от {from_state} к {to_state} равна {prob}, что не входит в диапазон [0,1].")
                    transition_matrix[state_indices[from_state], state_indices[to_state]] = prob
                    total_prob += prob
                # Проверяем, что сумма вероятностей из состояния равна 1
                if abs(total_prob - 1.0) > 1e-6:
                    raise ValueError(f"Сумма вероятностей исходящих из состояния {from_state} должна быть равна 1. Текущая сумма: {total_prob}")
            # Если все проверки пройдены, начинаем симуляцию
            states_over_time = []
            for _ in range(days):
                current_idx = state_indices[current_state]
                probs = transition_matrix[current_idx]
                next_state_idx = np.random.choice(len(weather_states), p=probs)
                current_state = weather_states[next_state_idx]
                state_counts[next_state_idx] += 1
                states_over_time.append(next_state_idx)

            result_text = "\n".join([f"{state}: {int(count)} дней" for state, count in zip(weather_states, state_counts)])

            # Находим самую частую погоду и её вероятность
            most_common_state_idx = np.argmax(state_counts)
            most_common_state = weather_states[most_common_state_idx]
            most_common_count = int(state_counts[most_common_state_idx])
            most_common_probability = most_common_count / days * 100  # в процентах

            # Скрыть настройки и показать результаты
            self.weather_settings_frame.grid_remove()
            self.weather_result_frame.grid()
            self.weather_result_frame.columnconfigure(0, weight=1)
            self.weather_result_frame.rowconfigure(1, weight=1)

            ctk.CTkLabel(self.weather_result_frame, text=result_text).grid(row=0, column=0, padx=5, pady=5)

            # Построение графика
            self.weather_figure = plt.Figure(figsize=(5, 4), dpi=100)
            self.weather_ax = self.weather_figure.add_subplot(111)
            self.weather_canvas = FigureCanvasTkAgg(self.weather_figure, master=self.weather_result_frame)
            self.weather_canvas.get_tk_widget().grid(row=1, column=0, sticky='nsew')
            self.weather_ax.plot(states_over_time)
            self.weather_ax.set_yticks(range(len(weather_states)))
            self.weather_ax.set_yticklabels(weather_states)
            self.weather_ax.set_xlabel("День")
            self.weather_ax.set_ylabel("Состояние погоды")
            # Обновленный заголовок графика
            self.weather_ax.set_title(f"За {days} дней самая частая погода: {most_common_state} ({most_common_count} раз, {most_common_probability:.2f}%)")
            self.weather_canvas.draw()

            # Кнопка возврата к настройкам
            ctk.CTkButton(self.weather_result_frame, text="Назад", command=self.back_to_weather_settings).grid(row=2, column=0, padx=5, pady=5)
        except ValueError as e:
            self.weather_error_label.configure(text=f"Ошибка: {e}")

    def show_automaton(self):
        try:
            weather_states = self.weather_states
            state_indices = {state: idx for idx, state in enumerate(weather_states)}
            # Создание направленного графа
            G = nx.DiGraph()
            for state in weather_states:
                G.add_node(state)
            for from_state in weather_states:
                for to_state in weather_states:
                    prob_str = self.transition_entries[(from_state, to_state)].get()
                    try:
                        prob = float(prob_str)
                    except ValueError:
                        raise ValueError(f"Вероятность перехода от {from_state} к {to_state} должна быть числом.")
                    if prob > 0:
                        G.add_edge(from_state, to_state, weight=prob)
            # Отрисовка графа
            pos = nx.circular_layout(G)
            edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True)}
            # Создаем новое окно
            automaton_window = ctk.CTkToplevel(self)
            automaton_window.title("Автомат переходов погоды")
            figure = plt.Figure(figsize=(8,8), dpi=100)
            ax = figure.add_subplot(111)
            nx.draw_networkx_nodes(G, pos, ax=ax, node_size=1500, node_color='lightblue')
            nx.draw_networkx_edges(G, pos, ax=ax, arrowstyle='->', arrowsize=20)
            nx.draw_networkx_labels(G, pos, ax=ax, font_size=12)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, label_pos=0.3, font_color='red')
            ax.set_title("Автомат переходов погоды")
            ax.axis('off')
            canvas = FigureCanvasTkAgg(figure, master=automaton_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
        except ValueError as e:
            self.weather_error_label.configure(text=f"Ошибка: {e}")

    def back_to_weather_settings(self):
        # Скрыть результаты и показать настройки
        self.weather_result_frame.grid_remove()
        self.weather_settings_frame.grid()

# Остальная часть кода остается без изменений...


class GCDCalculator(ctk.CTkFrame):
    def __init__(self, parent, result_label):
        super().__init__(parent)
        self.parent = parent
        self.result_label = result_label
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(1, weight=1)

        ctk.CTkLabel(self, text="Число a:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.a_entry = ctk.CTkEntry(self)
        self.a_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        self.a_entry.insert(0, "252")

        ctk.CTkLabel(self, text="Число b:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.b_entry = ctk.CTkEntry(self)
        self.b_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        self.b_entry.insert(0, "198")

        ctk.CTkButton(self, text="Вычислить НОД", command=self.calculate_gcd).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def calculate_gcd(self):
        try:
            a = int(self.a_entry.get())
            b = int(self.b_entry.get())
            if a <= 0 or b <= 0:
                raise ValueError("Числа должны быть положительными целыми числами.")

            original_a, original_b = a, b
            steps = []

            while b:
                q = a // b
                r = a % b
                # Добавляем объяснение к каждому шагу
                steps.append(f"{a} = {b} * {q} + {r}  # Делим {a} на {b}, получаем частное {q} и остаток {r}")
                a, b = b, r  # Переходим к следующей паре чисел

            gcd = a
            # Выводим результат и шаги
            self.result_label.configure(text=f"НОД({original_a}, {original_b}) = {gcd}\n" + "\n".join(steps))
        except ValueError as e:
            self.result_label.configure(text=f"Ошибка: {e}")

class AmplifierSimulation(ctk.CTkFrame):
    def __init__(self, parent, result_label):
        super().__init__(parent)
        self.parent = parent
        self.result_label = result_label
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(5, weight=1)

        ctk.CTkLabel(self, text="Время симуляции:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.simulation_time_entry = ctk.CTkEntry(self)
        self.simulation_time_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        self.simulation_time_entry.insert(0, "10")

        ctk.CTkLabel(self, text="Время задержки:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.delay_entry = ctk.CTkEntry(self)
        self.delay_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        self.delay_entry.insert(0, "2")

        ctk.CTkLabel(self, text="Формула коэффициента усиления (K):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.gain_formula_entry = ctk.CTkEntry(self)
        self.gain_formula_entry.grid(row=2, column=1, padx=5, pady=5, sticky='we')
        self.gain_formula_entry.insert(0, "5")  # Начальное значение K - 5

        ctk.CTkLabel(self, text="Формула сигнала (используйте 'x'):").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.signal_formula_entry = ctk.CTkEntry(self)
        self.signal_formula_entry.grid(row=3, column=1, padx=5, pady=5, sticky='we')
        self.signal_formula_entry.insert(0, "np.sin(x)")

        ctk.CTkButton(self, text="Смоделировать усиление", command=self.plot_amplifier).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=2, sticky='nsew')

    def plot_amplifier(self):
        try:
            simulation_time = float(self.simulation_time_entry.get())
            if simulation_time <= 0:
                raise ValueError("Время симуляции должно быть положительным числом.")

            delay_time = float(self.delay_entry.get())
            if delay_time < 0 or delay_time > simulation_time:
                raise ValueError("Время задержки должно быть между 0 и временем симуляции.")

            time_threshold = delay_time

            self.time = np.linspace(0, simulation_time, 1000)
            x = self.time  # Для использования в пользовательских функциях

            # Безопасное вычисление пользовательской формулы для сигнала
            formula = self.signal_formula_entry.get()
            allowed_names = {"np": np, "x": x, "sin": np.sin, "cos": np.cos, "exp": np.exp,
                             "log": np.log, "sqrt": np.sqrt, "pi": np.pi, "abs": np.abs}
            code = compile(formula, "<string>", "eval")
            for name in code.co_names:
                if name not in allowed_names:
                    raise NameError(f"Использование '{name}' не разрешено.")
            input_signal = eval(code, {"__builtins__": {}}, allowed_names)

            # Безопасное вычисление пользовательской формулы для коэффициента усиления K
            gain_formula = self.gain_formula_entry.get()
            code_gain = compile(gain_formula, "<string>", "eval")
            for name in code_gain.co_names:
                if name not in allowed_names:
                    raise NameError(f"Использование '{name}' в формуле K не разрешено.")
            gain = eval(code_gain, {"__builtins__": {}}, allowed_names)

            output_signal = np.where(self.time >= time_threshold, input_signal * gain, 0)

            self.ax.clear()
            self.ax.plot(self.time, input_signal, label="Входной сигнал")
            self.ax.plot(self.time, output_signal, label="Выходной сигнал")
            self.ax.set_xlabel("Время")
            self.ax.set_ylabel("Амплитуда")
            self.ax.set_title("Моделирование усиления сигнала с функцией K")
            self.ax.legend()
            self.canvas.draw()
            self.result_label.configure(text="")
        except Exception as e:
            self.result_label.configure(text=f"Ошибка в формуле: {e}")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Модели StateFlow")
        self.state('zoomed')  # Расширить окно на весь экран без полноэкранного режима

        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(fill='both', expand=True)

        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack(pady=5)

        self.create_weather_tab()
        self.create_gcd_tab()
        self.create_amplifier_tab()

    def create_weather_tab(self):
        self.notebook.add("Погода")
        weather_tab = self.notebook.tab("Погода")
        weather_simulation = WeatherSimulation(weather_tab)
        weather_simulation.pack(fill='both', expand=True)

    def create_gcd_tab(self):
        self.notebook.add("НОД")
        gcd_tab = self.notebook.tab("НОД")
        gcd_calculator = GCDCalculator(gcd_tab, self.result_label)
        gcd_calculator.pack(fill='both', expand=True)

    def create_amplifier_tab(self):
        self.notebook.add("Усилитель")
        amplifier_tab = self.notebook.tab("Усилитель")
        amplifier_simulation = AmplifierSimulation(amplifier_tab, self.result_label)
        amplifier_simulation.pack(fill='both', expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
