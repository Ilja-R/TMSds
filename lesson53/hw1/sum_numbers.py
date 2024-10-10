import sys


def print_hint():
    print(
        """Please provide exactly two numbers as arguments when running script
Numbers must be valid, e.g. 1, 2, 3.4, 5.6, etc
Example:
docker run --rm robalkin-python:53 sum_numbers.py 100 200
"""
    )


def sum_numbers():
    if len(sys.argv) != 3:
        print_hint()
        return

    try:
        num1 = float(sys.argv[1])
        num2 = float(sys.argv[2])
        result = num1 + num2
        print(f"The sum of {num1} and {num2} is {result}.")
    except ValueError:
        print_hint()


if __name__ == '__main__':
    sum_numbers()
