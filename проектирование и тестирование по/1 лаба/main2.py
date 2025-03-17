"""
Чтение входных данных
Первое число (n) указывает количество блоков соревнований.
После первого блока есть пустая строка, разделяющая блоки.

Обработка посылок участников
Используется словарь results, где ключ — номер участника, а значение — информация о нем (количество решенных задач, штрафное время, неправильные попытки).
Для каждого участника храним вложенный словарь tasks, отслеживающий попытки по каждой задаче.
При правильной посылке ("C"):
Если задача еще не решена, фиксируем штрафное время и решенные задачи.
При неправильной посылке ("I"):
Увеличиваем счетчик некорректных попыток для задачи.

Сортировка и вывод
Сортируем участников по убыванию числа решенных задач, затем по штрафному времени, затем по номеру участника.
Выводим таблицу с нужным форматированием.
"""
n = int(input().strip())

for i in range(n):
    if i == 0:
        input()

    results = {}

    while True:
        s = input().strip()
        if s == '':
            break

        num, task, time, state = s.split()
        num, task, time = int(num), int(task), int(time)

        if num not in results:
            results[num] = {'solved': 0, 'penalty': 0, 'tasks': {}}

        if state == "C":
            if task in results[num]['tasks'] and results[num]['tasks'][task]['solved']:
                continue

            incorrect_attempts = results[num]['tasks'].get(task, {}).get('incorrect', 0)
            results[num]['solved'] += 1
            results[num]['penalty'] += time + 20 * incorrect_attempts
            results[num]['tasks'][task] = {'solved': True, 'incorrect': incorrect_attempts}

        elif state == 'I':
            if task not in results[num]['tasks']:
                results[num]['tasks'][task] = {'solved': False, 'incorrect': 0}
            if not results[num]['tasks'][task]['solved']:
                results[num]['tasks'][task]['incorrect'] += 1

    rating_table = []
    for participant, data in results.items():
        rating_table.append((participant, data['solved'], data['penalty']))

    rating_table.sort(key=lambda x: (-x[1], x[2], x[0]))

    for participant, solved, penalty in rating_table:
        print(participant, solved, penalty)

    if i < n - 1:
        print()
