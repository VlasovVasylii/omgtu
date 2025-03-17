import io
import sys


def test_programming_contest():
    test_cases = [
        # Тест 1: базовый сценарий с 2 участниками
        ("""1

    1 2 10 I
    3 1 11 C
    1 2 19 R
    1 2 21 C
    1 1 25 C
    """,
    """1 2 66\n3 1 11"""),

        # Тест 2: участник решает задачу с несколькими ошибками
        ("""1

    2 3 15 I
    2 3 25 I
    2 3 30 C
    """, """2 1 70"""),

        # Тест 3: несколько участников с разными решениями
        ("""1

    1 1 10 C
    2 1 20 C
    3 1 30 C
    4 1 40 C
    """, """1 1 10\n2 1 20\n3 1 30\n4 1 40"""),

        # Тест 4: равные по задачам, но разные по штрафу
        ("""1

    1 2 10 C
    2 2 15 C
    1 3 20 C
    2 3 25 C
    """, """1 2 30\n2 2 40"""),

        # Тест 5: два блока соревнований
        ("""2

    1 1 10 C
    2 2 20 C

    3 3 30 C
    4 4 40 C
    """, """1 1 10\n2 1 20\n\n3 1 30\n4 1 40""")
    ]

    for i, (input_data, expected_output) in enumerate(test_cases, 1):
        sys.stdin = io.StringIO(input_data)
        sys.stdout = io.StringIO()

        # Запуск кода
        exec(open("main2.py", encoding="utf-8").read())

        output = sys.stdout.getvalue()
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

        assert output.strip() == expected_output.strip(), f"Тест {i} не пройден!\nОжидалось:\n{expected_output}\nПолучено:\n{output}"

    print("Все тесты пройдены!")


test_programming_contest()
