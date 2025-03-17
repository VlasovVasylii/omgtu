import io
import sys


def test_minesweeper():
    test_cases = [
        ("""4 4
*...
....
.*..
....
0 0
""", """Field #1:
*100
2210
1*10
1110
"""),

        ("""3 5
**...
.....
.*...
0 0
""", """Field #1:
**100
33200
1*100
"""),

        ("""2 2
..
..
0 0
""", """Field #1:
00
00
"""),

        ("""3 3
***
*.*
***
0 0
""", """Field #1:
***
*8*
***
""")
    ]

    for i, (input_data, expected_output) in enumerate(test_cases, 1):
        sys.stdin = io.StringIO(input_data)
        sys.stdout = io.StringIO()

        # Выполняем код
        exec(open("main.py").read())

        output = sys.stdout.getvalue()
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

        assert output.strip() == expected_output.strip(), f"Тест {i} не пройден!"

    print("Все тесты пройдены!")


test_minesweeper()
