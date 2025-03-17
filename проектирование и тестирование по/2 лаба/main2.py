"""
Описание алгоритма решения:
1. Структура входных данных:
    -   Первая строка содержит количество тестовых случаев
    -   Каждый тестовый случай начинается с тарифной сетки (24 числа)
    -   Далее следуют записи о въезде/выезде автомобилей
2. Основные шаги алгоритма:
   a) Чтение тарифной сетки (24 тарифа для каждого часа)
   b) Сбор записей по каждому автомобилю в словарь
   c) Для каждого автомобиля:
      - Сортировка записей по времени
      - Поиск пар "enter-exit"
      - Расчет стоимости для каждой поездки:
        * Расстояние * тариф (зависит от часа въезда)
        * +$1 за каждую поездку
      - +$2 за счет (если были поездки)
   d) Вывод результатов в алфавитном порядке по номеру автомобиля
3. Особенности реализации:
   - Все расчеты производятся в центах во избежание ошибок округления
   - Используется timestamp для корректной сортировки записей
   - Игнорируются записи без парных въездов/выездов
   - Результат форматируется с двумя знаками после запятой
4. Обработка краевых случаев:
   - Пропуск пустых строк между тестовыми случаями
   - Проверка наличия парных записей enter/exit
   - Корректная обработка различных форматов времени
"""


def solve():
    import sys
    from collections import defaultdict

    def calculate_trip_cost(hour, distance, rates):
        # Стоимость за километр для данного часа (в центах)
        rate = rates[hour]
        # Стоимость = (расстояние * тариф за км) в центах
        return (distance * rate)

    # Читаем входные данные
    data = sys.stdin.read().splitlines()
    num_cases = int(data[0])
    current_line = 1

    for case in range(num_cases):
        # Пропускаем пустые строки
        while current_line < len(data) and not data[current_line].strip():
            current_line += 1

        # Читаем тарифы
        rates = list(map(int, data[current_line].split()))
        current_line += 1

        # Собираем записи по машинам
        car_records = defaultdict(list)
        while current_line < len(data) and data[current_line].strip():
            parts = data[current_line].split()
            plate = parts[0]
            time = parts[1]
            event = parts[2].lower()
            location = int(parts[3])

            month, day, hour, minute = map(int, time.split(':'))
            timestamp = month * 31 * 24 * 60 + day * 24 * 60 + hour * 60 + minute

            car_records[plate].append((timestamp, hour, event, location))
            current_line += 1

        # Обрабатываем записи каждой машины
        bills = {}
        for plate, records in car_records.items():
            records.sort()  # Сортировка по времени
            total_cost = 0
            i = 0

            while i < len(records) - 1:
                current = records[i]
                next_record = records[i + 1]

                if current[2] == "enter" and next_record[2] == "exit":
                    # Вычисляем расстояние
                    distance = abs(next_record[3] - current[3])
                    # Вычисляем стоимость поездки в центах
                    trip_cost = calculate_trip_cost(current[1], distance, rates)
                    # Добавляем $1 (100 центов) за поездку
                    trip_cost += 100
                    total_cost += trip_cost
                    i += 2
                else:
                    i += 1

            if total_cost > 0:
                # Добавляем $2 (200 центов) за счёт
                total_cost += 200
                bills[plate] = total_cost

        # Выводим результаты
        for plate in sorted(bills.keys()):
            print(f"{plate} ${bills[plate] / 100:.2f}")

        # Печатаем пустую строку между тестовыми случаями, кроме последнего
        if case < num_cases - 1:
            print()


if __name__ == "__main__":
    solve()