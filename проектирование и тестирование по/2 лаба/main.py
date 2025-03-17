"""
Сортировка фрагментов: Фрагменты сортируются по длине.
Определение максимальной длины файла: Считается, что файл состоит из самого короткого и самого длинного фрагмента.
Попытка восстановления файла:
Перебираются все возможные пары коротких и длинных фрагментов.
Проверяется, можно ли составить файл, комбинируя оставшиеся фрагменты в пары.
Возвращение результата: Если найдено валидное восстановление, оно возвращается.
"""


def restore_original(fragments):
    if not fragments:
        return ""

    fragments_sorted = sorted(fragments, key=lambda x: len(x))
    min_len = len(fragments_sorted[0])
    max_len = len(fragments_sorted[-1])
    total_length = min_len + max_len

    # Перебираем все возможные пары фрагментов
    for i in range(len(fragments_sorted)):
        for j in range(len(fragments_sorted)):
            if i == j:
                continue
            a, b = fragments_sorted[i], fragments_sorted[j]
            if len(a) + len(b) != total_length:
                continue

            # Пробуем обе комбинации (a + b и b + a)
            candidates = [a + b, b + a]
            for candidate in candidates:
                used = [False] * len(fragments_sorted)
                used[i] = used[j] = True

                # Проверяем, можно ли составить файл из оставшихся фрагментов
                valid = True
                for k in range(len(fragments_sorted)):
                    if used[k]:
                        continue
                    current = fragments_sorted[k]
                    needed_len = total_length - len(current)
                    found = False
                    for l in range(len(fragments_sorted)):
                        if not used[l] and len(fragments_sorted[l]) == needed_len:
                            combined = current + fragments_sorted[l]
                            combined_rev = fragments_sorted[l] + current
                            if combined == candidate or combined_rev == candidate:
                                used[k] = used[l] = True
                                found = True
                                break
                    if not found:
                        valid = False
                        break

                if valid:
                    return candidate

    return ""


def main():
    import sys

    input = sys.stdin.read().splitlines()
    idx = 0
    n = int(input[idx].strip())
    idx += 1

    for t in range(n):
        # Пропускаем пустые строки между тестами
        while idx < len(input) and input[idx].strip() == "":
            idx += 1

        # Считываем фрагменты для текущего теста
        fragments = []
        while idx < len(input) and input[idx].strip() != "":
            fragments.append(input[idx].strip())
            idx += 1

        # Восстанавливаем файл и выводим результат
        result = restore_original(fragments)
        print(result)

        # Добавляем пустую строку между выводами, если это не последний тест
        if t < n - 1:
            print()


if __name__ == "__main__":
    main()

