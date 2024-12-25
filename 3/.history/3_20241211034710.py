import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import TransferFunction, bode, step, impulse

# ==============================================================
# Апериодическое звено (First-order lag element)
# ==============================================================
# Теоретическое обоснование:
# Апериодическое звено характеризуется передаточной функцией:
#     W(s) = k / (T1 * s + 1)
# где:
#     - k: коэффициент передачи
#     - T1: постоянная времени
#
# Частотные характеристики апериодического звена включают:
#     - Амплитудно-частотная характеристика (АЧХ)
#     - Фазо-частотная характеристика (ФЧХ)
#     - Действительная и мнимая части
#     - Логарифмическая амплитудно-частотная характеристика (ЛАЧХ)
#
# Цель: исследовать влияние параметра T1 на ФЧХ и ЛАЧХ.

# Заданные параметры
k = 0.5          # Коэффициент передачи
T1 = 6           # Постоянная времени T1
T2 = 4           # Дополнительный параметр (не используется в апериодическом звене)
epsilon = 0.6    # Коэффициент затухания (не используется в апериодическом звене)

# Диапазон частот
omega = np.logspace(-2, 2, 500)  # Логарифмически распределенные частоты от 0.01 до 100 рад/с

# Расчет амплитудно-частотной характеристики (АЧХ)
# А(ω) = k / sqrt((T1 * ω)^2 + 1)
A_omega = k / np.sqrt((T1 * omega)**2 + 1)

# Расчет фазо-частотной характеристики (ФЧХ)
# φ(ω) = -arctangent(T1 * ω)
phi_omega = -np.arctan(T1 * omega)

# Расчет действительной и мнимой частей
# U(ω) = А(ω) * cos(φ(ω))
# V(ω) = А(ω) * sin(φ(ω))
U_omega = A_omega * np.cos(phi_omega)
V_omega = A_omega * np.sin(phi_omega)

# Логарифмическая амплитудно-частотная характеристика (ЛАЧХ)
# L(ω) = 20 * log10(A(ω))
L_omega = 20 * np.log10(A_omega)

# Построение графиков частотных характеристик
# --------------------------------------------

# 1. Амплитудная характеристика A(ω)
plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.semilogx(omega, A_omega)
plt.title("Амплитудная характеристика A(ω)")
plt.xlabel("ω (рад/с)")
plt.ylabel("A(ω)")
plt.grid(True)

# 2. Фазовая характеристика φ(ω)
plt.subplot(2, 2, 2)
plt.semilogx(omega, phi_omega)
plt.title("Фазовая характеристика φ(ω)")
plt.xlabel("ω (рад/с)")
plt.ylabel("φ(ω) (рад)")
plt.grid(True)

# 3. Действительная часть U(ω)
plt.subplot(2, 2, 3)
plt.semilogx(omega, U_omega)
plt.title("Действительная часть U(ω)")
plt.xlabel("ω (рад/с)")
plt.ylabel("U(ω)")
plt.grid(True)

# 4. Мнимая часть V(ω)
plt.subplot(2, 2, 4)
plt.semilogx(omega, V_omega)
plt.title("Мнимая часть V(ω)")
plt.xlabel("ω (рад/с)")
plt.ylabel("V(ω)")
plt.grid(True)

plt.tight_layout()
plt.show()

# Построение Логарифмической АЧХ (ЛАЧХ)
# -------------------------------------

# Точная ЛАЧХ
plt.figure(figsize=(10, 6))
plt.semilogx(omega, L_omega, label="Точная ЛАЧХ")

# Асимптотическая ЛАЧХ
# При низких частотах (ω → 0): L(ω) ≈ 20 * log10(k)
# При высоких частотах (ω → ∞): L(ω) ≈ 20 * log10(k) - 20 * log10(T1 * ω)
asymp_L_omega = np.where(
    omega <= 1/T1,
    20 * np.log10(k),
    20 * np.log10(k) - 20 * np.log10(T1 * omega)
)
plt.semilogx(omega, asymp_L_omega, '--', label="Асимптотическая ЛАЧХ")
plt.title("Логарифмическая АЧХ (ЛАЧХ)")
plt.xlabel("ω (рад/с)")
plt.ylabel("L(ω) (дБ)")
plt.legend()
plt.grid(True)
plt.show()

# Исследование влияния параметра T1 на φ(ω) и L(ω)
# -------------------------------------------------
# Будем варьировать значение T1 и наблюдать изменения в ФЧХ и ЛАЧХ

T1_values = [2, 4, 6, 8, 10]  # Различные значения T1 для исследования

plt.figure(figsize=(12, 5))

# Фазовая характеристика при различных T1
plt.subplot(1, 2, 1)
for T1_var in T1_values:
    phi_var = -np.arctan(T1_var * omega)
    plt.semilogx(omega, phi_var, label=f"T1={T1_var}")
plt.title("Влияние T1 на фазовую характеристику φ(ω)")
plt.xlabel("ω (рад/с)")
plt.ylabel("φ(ω) (рад)")
plt.legend()
plt.grid(True)

# Логарифмическая АЧХ при различных T1
plt.subplot(1, 2, 2)
for T1_var in T1_values:
    A_var = k / np.sqrt((T1_var * omega)**2 + 1)
    L_var = 20 * np.log10(A_var)
    plt.semilogx(omega, L_var, label=f"T1={T1_var}")
plt.title("Влияние T1 на ЛАЧХ L(ω)")
plt.xlabel("ω (рад/с)")
plt.ylabel("L(ω) (дБ)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Выводы:
# -------
# 1. При увеличении параметра T1 фазовая характеристика φ(ω) становится более пологой,
#    что указывает на увеличение фазового сдвига на низких частотах.
# 2. ЛАЧХ смещается влево при увеличении T1, демонстрируя уменьшение полосы пропускания
#    системы и снижение усиления на высоких частотах.

# Использование функции tf для задания передаточной функции
# ---------------------------------------------------------
# Функция tf из модуля scipy.signal позволяет задать передаточную функцию системы

# Задаем передаточную функцию апериодического звена с параметрами T=2, k=1
k_tf = 1
T_tf = 2
system = TransferFunction([k_tf], [T_tf, 1])

# Построение характеристик с использованием функции tf
# ----------------------------------------------------

# 1. Частотные характеристики (Bode plot)
w, mag, phase = bode(system, omega)

plt.figure(figsize=(12, 5))

# Амплитудная характеристика (Bode magnitude)
plt.subplot(1, 2, 1)
plt.semilogx(w, mag)
plt.title("Bode Амплитудная характеристика")
plt.xlabel("ω (рад/с)")
plt.ylabel("Магнитуда (дБ)")
plt.grid(True)

# Фазовая характеристика (Bode phase)
plt.subplot(1, 2, 2)
plt.semilogx(w, phase)
plt.title("Bode Фазовая характеристика")
plt.xlabel("ω (рад/с)")
plt.ylabel("Фаза (градусы)")
plt.grid(True)

plt.tight_layout()
plt.show()

# 2. Переходная характеристика (ступенчатая)
t_step, step_response = step(system)

plt.figure(figsize=(8, 5))
plt.plot(t_step, step_response)
plt.title("Переходная характеристика на единичное ступенчатое воздействие")
plt.xlabel("Время (с)")
plt.ylabel("Амплитуда")
plt.grid(True)
plt.show()

# 3. Импульсная переходная характеристика
t_impulse, impulse_response = impulse(system)

plt.figure(figsize=(8, 5))
plt.plot(t_impulse, impulse_response)
plt.title("Импульсная переходная характеристика")
plt.xlabel("Время (с)")
plt.ylabel("Амплитуда")
plt.grid(True)
plt.show()

# Выводы:
# -------
# - Передаточная функция апериодического звена позволяет анализировать систему во временной области.
# - Переходные характеристики показывают, как система реагирует на различные входные воздействия.
# - Функция tf упрощает процесс моделирования и анализа линейных систем.

# Примечание:
# -----------
# Для полного исследования рекомендуется ознакомиться с функцией ltiview (в MATLAB),
# однако в Python эквивалентом может служить использование функций из пакета control или scipy.signal.

# Конец кода
