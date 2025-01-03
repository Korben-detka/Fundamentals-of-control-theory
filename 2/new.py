def gcd(a, b):
    """
    Функция для нахождения НОД (наибольшего общего делителя) двух чисел
    с использованием алгоритма Евклида.
    """
    while b != 0:
        a, b = b, a % b
    return a

# Примеры работы модели
examples = [
    (48, 18),  # НОД = 6
    (56, 98),  # НОД = 14
    (1071, 462),  # НОД = 21
    (270, 192),  # НОД = 6
    (144, 12),  # НОД = 12
]

print("Примеры работы модели нахождения НОД:")
for a, b in examples:
    result = gcd(a, b)
    print(f"НОД({a}, {b}) = {result}")
