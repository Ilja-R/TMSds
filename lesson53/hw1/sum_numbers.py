import sys


def sum_numbers():
    """
    This script takes two numbers as arguments and prints the sum of them.
    Those numbers must be valid, e.g. 1, 2, 3.4, 5.6, etc

    Example:
    sum_numbers.py 100 200

    When running from docker container:
    docker run --rm robalkin-python:53 sum_numbers.py 100 200
    """
    hint = sum_numbers.__doc__
    if len(sys.argv) != 3:
        print(hint)
        return

    try:
        num1 = float(sys.argv[1])
        num2 = float(sys.argv[2])
        result = num1 + num2
        print(f"The sum of {num1} and {num2} is {result}.")
    except ValueError:
        print(hint)


if __name__ == '__main__':
    sum_numbers()
