from transitions import Machine
import random

# Класс для модели климата на планете Оз
class PlanetOz:
    states = ['sunny', 'rainy', 'snowy']  # Определение состояний
    
    def __init__(self):
        # Счетчики для каждого состояния
        self.sunny_days = 0
        self.rainy_days = 0
        self.snowy_days = 0

        # Инициализация машины состояний
        self.machine = Machine(model=self, states=PlanetOz.states, initial='sunny')

        # Определение переходов
        self.machine.add_transition(trigger='next_day', source='sunny', dest='rainy', after='increment_rainy')
        self.machine.add_transition(trigger='next_day', source='sunny', dest='snowy', after='increment_snowy')
        self.machine.add_transition(trigger='next_day', source='sunny', dest='sunny', after='increment_sunny')

        self.machine.add_transition(trigger='next_day', source='rainy', dest='snowy', after='increment_snowy')
        self.machine.add_transition(trigger='next_day', source='rainy', dest='sunny', after='increment_sunny')
        self.machine.add_transition(trigger='next_day', source='rainy', dest='rainy', after='increment_rainy')

        self.machine.add_transition(trigger='next_day', source='snowy', dest='sunny', after='increment_sunny')
        self.machine.add_transition(trigger='next_day', source='snowy', dest='rainy', after='increment_rainy')
        self.machine.add_transition(trigger='next_day', source='snowy', dest='snowy', after='increment_snowy')

    # Методы для инкрементации счетчиков
    def increment_sunny(self):
        self.sunny_days += 1

    def increment_rainy(self):
        self.rainy_days += 1

    def increment_snowy(self):
        self.snowy_days += 1

    # Метод для случайного перехода
    def random_weather(self):
        self.next_day()  # Выполняет переход

# Создание модели и запуск симуляции
oz = PlanetOz()

# Симулируем погоду на протяжении 100 дней
for day in range(100):
    oz.random_weather()  # Переход в случайное состояние

# Вывод результатов
print("Количество солнечных дней:", oz.sunny_days)
print("Количество дождливых дней:", oz.rainy_days)
print("Количество снежных дней:", oz.snowy_days)
