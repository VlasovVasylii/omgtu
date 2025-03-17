"""
Чтение входных данных

Определить количество тестовых блоков.
Считать структуру оплаты (24 числа).
Считать записи въезда/выезда в формате (номер машины, дата, время, тип записи, км-метка).
Обработка данных

Сортировать записи по времени.
Группировать записи по номеру автомобиля.
Обрабатывать только пары "enter-exit".
Вычислять расстояние и стоимость проезда.
Расчет стоимости

Вычислять километраж между "enter" и "exit".
Определять стоимость на основе тарифа, действующего в час въезда.
Добавлять $1 за поездку и $2 за счет.
Вывод результатов

Сортировать автомобили по номеру.
Форматировать сумму в долларах (2 знака после запятой).
Разделять тестовые блоки пустой строкой.
"""

import sys
from collections import defaultdict


def parse_input():
    input_data = sys.stdin.read().strip().split('\n')
    index = 0
    num_blocks = int(input_data[index])
    index += 1
    blocks = []

    for _ in range(num_blocks):
        while index < len(input_data) and input_data[index] == "":
            index += 1
        fees = list(map(int, input_data[index].split()))
        index += 1
        records = []
        while index < len(input_data) and input_data[index] != "":
            records.append(input_data[index])
            index += 1
        blocks.append((fees, records))

    return blocks


def process_block(fees, records):
    trips = defaultdict(list)

    for record in records:
        parts = record.split()
        plate = parts[0]
        month, day, hour, minute = map(int, parts[1].split(':'))
        timestamp = (day, hour, minute)
        action = parts[2]
        km_marker = int(parts[3])
        trips[plate].append((timestamp, action, km_marker))

    bills = {}
    for plate in trips:
        trips[plate].sort()
        total_cost = 2  # $2 for the bill processing fee
        i = 0
        while i < len(trips[plate]) - 1:
            if trips[plate][i][1] == "enter" and trips[plate][i + 1][1] == "exit":
                day, hour, minute = trips[plate][i][0]
                km_start = trips[plate][i][2]
                km_end = trips[plate][i + 1][2]

                distance = abs(km_end - km_start)
                cost = distance * fees[hour] / 100 + 1  # Convert cents to dollars, add $1 trip fee
                total_cost += cost
                i += 2
            else:
                i += 1

        if total_cost > 2:  # Ignore if no valid trips were found
            bills[plate] = total_cost

    return sorted(bills.items())


def main():
    blocks = parse_input()
    results = []

    for i, (fees, records) in enumerate(blocks):
        processed = process_block(fees, records)
        if i > 0:
            results.append("")
        for plate, cost in processed:
            results.append(f"{plate} ${cost:.2f}")

    print("\n".join(results))


if __name__ == "__main__":
    main()
