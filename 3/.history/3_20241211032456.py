import numpy as np
from scipy.signal import TransferFunction, bode, step, impulse
import matplotlib.pyplot as plt

# Заданные параметры
k  = 0.5
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

# Построение графиков частотных характеристик
plt.figure(figsize=(12, 8))

# Амплитудная характеристика
plt.subplot(2, 2, 1)
plt.semilogx(omega, A_omega)
plt.title("Амплитудная характеристика A(ω)")
plt.xlabel("ω (рад/с)")
plt.ylabel("A(ω)")
plt.grid(True)

# Фазовая характеристика
plt.subplot(2, 2, 2)
plt.semilogx(omega, phi_omega)
plt.title("Фазовая характеристика φ(ω)")
plt.xlabel("ω (рад/с)")
plt.ylabel("φ(ω) (рад)")
plt.grid(True)

# Действительная часть
plt.subplot(2, 2, 3)
plt.semilogx(omega, U_omega)
plt.title("Действительная часть U(ω)")
plt.xlabel("ω (рад/с)")
plt.ylabel("U(ω)")
plt.grid(True)

# Мнимая часть
plt.subplot(2, 2, 4)
plt.semilogx(omega, V_omega)
plt.title("Мнимая часть V(ω)")
plt.xlabel("ω (рад/с)")
plt.ylabel("V(ω)")
plt.grid(True)

plt.tight_layout()
plt.show()

# Логарифмическая АЧХ
plt.figure(figsize=(10, 6))
plt.semilogx(omega, L_omega, label="Точная ЛАЧХ")

# Асимптотическая ЛАЧХ
asymp_L_omega = 20 * np.log10(k) - 20 * np.log10(T1 * omega + 1)
plt.semilogx(omega, asymp_L_omega, "--", label="Асимптотическая ЛАЧХ")
plt.title("Логарифмическая амплитудно-частотная характеристика (ЛАЧХ)")
plt.xlabel("ω (рад/с)")
plt.ylabel("L(ω) (дБ)")
plt.legend()
plt.grid(True)
plt.show()

# Анализ с использованием функции tf
system = TransferFunction([k], [T, 1])

# Построение всех характеристик с помощью tf
w, mag, phase = bode(system)
t, step_response = step(system)
t_impulse, impulse_response = impulse(system)

plt.figure(figsize=(12, 8))

# Bode Amplitude
plt.subplot(2, 2, 1)
plt.semilogx(w, mag)
plt.title("Bode Амплитудная характеристика")
plt.xlabel("ω (рад/с)")
plt.ylabel("Магнитуда (дБ)")
plt.grid(True)

# Bode Phase
plt.subplot(2, 2, 2)
plt.semilogx(w, phase)
plt.title("Bode Фазовая характеристика")
plt.xlabel("ω (рад/с)")
plt.ylabel("Фаза (градусы)")
plt.grid(True)

# Step Response
plt.subplot(2, 2, 3)
plt.plot(t, step_response)
plt.title("Переходная характеристика (ступенчатая)")
plt.xlabel("Время (с)")
plt.ylabel("Амплитуда")
plt.grid(True)

# Impulse Response
plt.subplot(2, 2, 4)
plt.plot(t_impulse, impulse_response)
plt.title("Импульсная переходная характеристика")
plt.xlabel("Время (с)")
plt.ylabel("Амплитуда")
plt.grid(True)

plt.tight_layout()
plt.show()

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
