import random

def generate_matrix(size: int) -> list:
    """
    Generate a square number matrix of given size. Starts at random number 10 - 20.

    :param size: size of square matrix
    :return: a new generated matrix, internally a list of lists
    """
    counter = random.randint(10, 21)
    matrix = []
    for i in range(size):
        inner_matrix = []
        for j in range(size):
            inner_matrix.append(counter)
            counter += 1
        matrix.append(inner_matrix)
    return matrix


def filter_numbers(element: tuple, column_position: int, size: int) -> bool:
    """
    Return element if it should be added.

    :param element: a tuple which holds index in a row and a value
    :param column_position: int row number
    :param size: a size of a square matrix
    :return: True if element should be added, else false
    """
    is_odd = size % 2 != 0
    row_position = element[0]
    if column_position < size // 2 + is_odd:
        if row_position < column_position or row_position > (size - 1) - column_position:
            return False
    else:
        if row_position + 1 < size - column_position or row_position > column_position:
            return False
    print(element[1])
    return True


def calculate_row(row: list, i: int) -> int:
    """
    Calculate a sum of a separate row in matrix.

    :param row: list of integers
    :param i: a row number
    :return: sum of elements
    """
    size = len(row)
    print(row)
    return sum([element[1] for element in filter(lambda x: filter_numbers(x, i, size), enumerate(row))])

def get_sum_of_matrix(matrix: list) -> int:
    """
    Return summ of a given matrix based on sand watch filter
    Matrix of size 5:
        +++++
        0+++0
        00+00
        0+++0
        +++++
    Matrix of size 6:
        ++++++
        0++++0
        00++00
        00++00
        0++++0
        ++++++

    :param matrix: square matrix
    :return: int sum of elements in a matrix
    """
    summ = 0
    for i, row in enumerate(matrix):
        summ += calculate_row(row, i)
    return summ


new_matrix = generate_matrix(7)
print(new_matrix)
print(get_sum_of_matrix(new_matrix))