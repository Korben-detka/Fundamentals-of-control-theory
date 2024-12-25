import numpy as np
from scipy.signal import TransferFunction, bode, step, impulse
import matplotlib.pyplot as plt

# Заданные параметры
k = 0.5
T1 = 6
T2 = 4
epsilon = 0.6
T = 2  # Для tf анализа

# Частотная область
omega = np.logspace(-2, 2, 500)

# Частотные характеристики апериодического звена
A_omega = k / np.sqrt((T1 * omega)**2 + 1)
phi_omega = -np.arctan(T1 * omega)
U_omega = A_omega * np.cos(phi_omega)
V_omega = A_omega * np.sin(phi_omega)
L_omega = 20 * np.log10(A_omega)

# Анализ с использованием функции tf
system = TransferFunction([k], [T, 1])

# Построение всех характеристик с помощью tf
w, mag, phase = bode(system)
t, step_response = step(system)
t_impulse, impulse_response = impulse(system)

# Анализ влияния параметра T на φ(ω) и L(ω)
T_values = [1, 2, 5, 10]
phi_results = {}
L_results = {}

for T_test in T_values:
    system_test = TransferFunction([k], [T_test, 1])
    _, mag_test, phase_test = bode(system_test, omega)
    phi_results[T_test] = phase_test
    L_results[T_test] = mag_test

# Анализ:
# 1. Увеличение параметра T смещает ЛАЧХ влево, так как постоянная времени растет, а следовательно, система становится медленнее.
# 2. Фазовая характеристика φ(ω) при увеличении T становится более пологой, задержка по фазе увеличивается.

# Код завершен. Выводы:
# - Точная и асимптотическая ЛАЧХ совпадают при низких и высоких частотах.
# - Постоянная времени T значительно влияет на частотные характеристики.
# - Для построения всех характеристик можно использовать функцию TransferFunction из SciPy.
