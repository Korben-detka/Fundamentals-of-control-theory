import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Параметры системы
M = 1.0   # масса груза (в килограммах)
g = 9.81  # ускорение свободного падения (м/с^2)
m = 0.01  # масса пули

def create_3d_plot(l_range=(0.1, 5), v_range=(100, 600), l_steps=100, v_steps=100, cmap='viridis', alpha=0.8):
    # Определяем диапазоны для длины подвеса и скорости пули
    l_values = np.linspace(l_range[0], l_range[1], l_steps)
    v_values = np.linspace(v_range[0], v_range[1], v_steps)

    # Создаем сетку для l и v
    l_grid, v_grid = np.meshgrid(l_values, v_values)

    # Вычисляем угол отклонения α в радианах
    alpha_grid_radians = np.arccos(1 - (m * v_grid)**2 / (2 * (m + M)**2 * g * l_grid))

    # Преобразование угла отклонения из радиан в градусы
    alpha_grid_degrees = np.degrees(alpha_grid_radians)

    # Ограничиваем значения угла в пределах от 0 до 90 градусов
    alpha_grid_degrees = np.clip(alpha_grid_degrees, 0, 90)

    # Построение 3D графика
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Используем plot_surface для создания 3D графика с прозрачностью
    surface = ax.plot_surface(l_grid, v_grid, alpha_grid_degrees, cmap=cmap, alpha=alpha)

    # Добавляем контурные линии на "пол"
    # ax.contour(l_grid, v_grid, alpha_grid_degrees, zdir='z', offset=0, cmap=cmap)

    # Добавляем цветовую шкалу
    fig.colorbar(surface, ax=ax, shrink=0.1, aspect=5, label='Угол отклонения (°)')

    # Настройки осей
    ax.set_xlabel('Длина подвеса (m)')
    ax.set_ylabel('Скорость пули (m/s)')
    ax.set_zlabel('Угол отклонения α (degrees)')
    ax.set_title('Зависимость угла отклонения от длины подвеса и скорости пули')

    # Визуальные настройки
    ax.view_init(elev=30, azim=-60)  # Угол обзора графика
    ax.grid(True)

    # Показ графика
    plt.show()

# Вызов функции с параметрами
create_3d_plot(
    l_range=(0.1, 5),   # Диапазон для длины подвеса
    v_range=(0, 600),   # Диапазон для скорости пули
    l_steps=100,        # Количество шагов по длине подвеса
    v_steps=100,        # Количество шагов по скорости
    cmap='plasma',      # Цветовая схема
    alpha=1             # Прозрачность поверхности
)
