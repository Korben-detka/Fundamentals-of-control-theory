import numpy as np
import matplotlib.pyplot as plt

# Параметры системы
M = 10  # масса груза, кг
g = 9.8  # ускорение свободного падения, м/с²
l = 1  # длина подвеса груза, м

# Модель влияния массы пули на угол отклонения груза
v = 300  # скорость пули, м/с
m = np.arange(0.001, 0.031, 0.001)  # массы пули от 0.001 до 0.03 кг с шагом 0.001 кг
a = np.arccos(1 - (m**2 * v**2) / (2 * (m + M)**2 * g * l))
a = np.degrees(a)  # переводим радианы в градусы

plt.subplot(2, 1, 1)
plt.plot(m * 1000, a)
plt.grid(True)
plt.xlabel('m, грамм')  # подписываем оси
plt.ylabel(r'$\alpha$, °')
plt.title(r'$\alpha = f(m)$. v = 300 м/с')

# Модель скорости пули в зависимости от угла отклонения груза
m = 0.01  # масса пули, кг
a = np.arange(0.1, 14.1, 0.1)  # углы от 0.1° до 14° с шагом 0.1°
v = np.sqrt(2 * (m + M)**2 * g * l * (1 - np.cos(np.radians(a))) / (m**2))

plt.subplot(2, 1, 2)
plt.plot(a, v)
plt.grid(True)
plt.xlabel(r'$\alpha$, °')  # подписываем оси
plt.ylabel('v, м/с')
plt.title('v = f($\\alpha$). m = 10 грамм.')

plt.tight_layout()
plt.show()
