import sys
import numpy as np
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Класс для интеграции matplotlib в PyQt5
class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(10, 6), dpi=100)  # Создаём фигуру с заданными размерами и разрешением
        self.axes = fig.add_subplot(111)        # Добавляем один подграфик
        super(MatplotlibCanvas, self).__init__(fig)  # Инициализируем базовый класс с фигурой
        self.setParent(parent)

# Основной класс приложения
class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        # Замените 'interface.ui' на путь к вашему .ui файлу, если он находится в другой директории
        uic.loadUi('interface.ui', self)  # Загружаем интерфейс из .ui файла

        self.M = 10                  # Значение массы по умолчанию
        self.current_plot = 'angle'  # Текущий отображаемый график ('angle' или 'speed')

        # Создаём экземпляр холста matplotlib и добавляем его в plot_widget
        self.canvas = MatplotlibCanvas(self.plot_widget)
        layout = QtWidgets.QVBoxLayout(self.plot_widget)
        layout.addWidget(self.canvas)

        # Подключаем кнопки к методам
        self.btn_angle_function.clicked.connect(self.plot_angle_function)
        self.btn_speed_function.clicked.connect(self.plot_speed_function)

        # Подключаем ползунок к методу обновления M
        self.slider_M.valueChanged.connect(self.update_M)

        # Устанавливаем начальное значение метки для отображения M
        self.label_M_value.setText(f"M = {self.M} кг")
        self.label_M_value_2.setText("Масса груза123456789")
        self.label_M_value_2.adjustSize()


        # Настройка автоматической подстройки размера метки
        self.label_M_value.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.label_M_value.adjustSize()

        # Разворачиваем окно на весь экран
        self.showMaximized()

        # Отображаем первоначальный график
        self.plot_angle_function()


    def update_M(self, value):
        """
        Обновляет значение массы M при изменении ползунка и обновляет текущий график.
        """
        self.M = value  # Обновляем значение M
        self.label_M_value.setText(f"M = {self.M} кг")  # Обновляем текст метки

        # Обновляем метку и подстраиваем размер
        self.label_M_value.adjustSize()

        # Автоматически обновляем текущий график
        if self.current_plot == 'angle':
            self.plot_angle_function()
        elif self.current_plot == 'speed':
            self.plot_speed_function()

    def plot_angle_function(self):
        """
        Строит график зависимости угла отклонения от массы пули.
        """
        self.current_plot = 'angle'  # Устанавливаем текущий график

        # Очищаем предыдущий график
        self.canvas.axes.clear()

        # Параметры системы
        M = self.M   # Используем текущее значение M
        g = 9.8     # Ускорение свободного падения, м/с²
        l = 1       # Длина подвеса груза, м

        # Модель влияния массы пули на угол отклонения груза
        v = 300  # Скорость пули, м/с
        m = np.arange(0.001, 0.031, 0.001)  # Массы пули от 0.001 кг до 0.03 кг с шагом 0.001 кг

        # Вычисляем аргумент для arccos и обрезаем его в пределах [-1, 1], чтобы избежать ошибок
        argument = 1 - (m**2 * v**2) / (2 * (m + M)**2 * g * l)
        argument = np.clip(argument, -1, 1) # ограничиваем угол
        a = np.arccos(argument)
        a = np.degrees(a)  # Переводим радианы в градусы

        # Строим график
        self.canvas.axes.plot(m * 1000, a, marker='o', linestyle='-', color='b')
        self.canvas.axes.set_xlabel('m, грамм')
        self.canvas.axes.set_ylabel(r'$\alpha$, °')
        self.canvas.axes.set_title(f'Зависимость угла отклонения от массы пули при M = {M} кг')
        self.canvas.axes.grid(True)

        # Обновляем холст
        self.canvas.draw()

    def plot_speed_function(self):
        """
        Строит график зависимости скорости пули от угла отклонения груза.
        """
        self.current_plot = 'speed'  # Устанавливаем текущий график

        # Очищаем предыдущий график
        self.canvas.axes.clear()

        # Параметры системы
        M = self.M   # Используем текущее значение M
        g = 9.8     # Ускорение свободного падения, м/с²
        l = 1       # Длина подвеса груза, м

        # Модель скорости пули в зависимости от угла отклонения груза
        m = 0.01  # Масса пули, кг
        a = np.arange(0.1, 14.1, 0.1)  # Углы от 0.1° до 14° с шагом 0.1°
        v = np.sqrt(2 * (m + M)**2 * g * l * (1 - np.cos(np.radians(a))) / (m**2))

        # Строим график
        self.canvas.axes.plot(a, v, marker='x', linestyle='--', color='r')
        self.canvas.axes.set_xlabel(r'$\alpha$, °')
        self.canvas.axes.set_ylabel('v, м/с')
        self.canvas.axes.set_title(f'Зависимость скорости пули от угла отклонения при M = {M} кг')
        self.canvas.axes.grid(True)

        # Обновляем холст
        self.canvas.draw()

# Точка входа в приложение
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.showMaximized()  # Разворачиваем окно на весь экран
    sys.exit(app.exec_())
