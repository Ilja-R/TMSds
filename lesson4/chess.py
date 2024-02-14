from abc import ABC, abstractmethod
"""
Шахматы. у вас есть стандартное поле 8*8, после введения координат (a, b)
нахождения вашей фигуры и фигуры соперника (с, d), необходимо получить
ответ, угрожает ли вражеская фигура вам

Сложная задача
Шахматы. у вас есть стандартное поле 8*8, после введения координат (a, b)
нахождения вашей фигуры конь и фигуры соперника (с, d). Необходимо определить,
угрожаете ли вы сопернику, с учетом того, что у вас есть ход. (проверить состояние
до и после хода, координаты хода рассчитывается автоматически, соперник стоит на
месте)
"""

DIAGONAL_DIRECTIONS = ((-1, -1), (-1, 1), (1, -1), (1, 1))
HORSE_MOVE_DIRECTION= ((-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1))

def is_legal_chess_cell(x: int, y: int) -> bool:
    """Return if given cell is in range of a chess field."""
    return 0 <= x <= 7 and 0 <= y <= 7


def get_cells_on_same_vertical(x: int, y: int) -> set:
    """
    Return all squares on same vertical, do not return square figure is standing on.
    Use for: rook and queen
    """
    return set((x, new_y) for new_y in range (0, 7) if new_y != y)

def get_cells_on_same_horizontal(x: int, y: int) -> set:
    """
    Return all squares on same horizontal, do not return square figure is standing on.
    Use for: rook and queen
    """
    return set((new_x, y) for new_x in range (0, 7) if new_x != x)

def get_cells_on_same_diagonal(x: int, y: int) -> set:
    """
    Return all squares on same diagonal, do not return square figure is standing on.
    Use for: bishop and queen
    """
    cells_on_same_diagonal = set()
    for diagonal_direction in DIAGONAL_DIRECTIONS:
        x_new, direction_x = x + diagonal_direction[0], diagonal_direction[0]
        y_new, direction_y = y + diagonal_direction[1], diagonal_direction[1]
        while is_legal_chess_cell(x_new, y_new):
            cells_on_same_diagonal.add((x_new, y_new))
            x_new += direction_x
            y_new += direction_y
    return cells_on_same_diagonal


# This is used to store cached moves possibility.
# Do not use in actual chess as there are pieces on the table
cached_moves = {}

class ChessFigure(ABC):
    """Generic abstract class to share logic of all figures."""
    def __init__(self, name, x, y):
        if is_legal_chess_cell(x, y):
            self.name = name
            self.x = x
            self.y = y
        else:
            raise ValueError(f"Cannot init ChessFigure {name} with positions {x , y}")

    def __repr__(self) -> str:
        return f"({self.name} [{self.x}, {self.y}])"

    def move(self, x, y):
        """Move a piece."""
        if is_legal_chess_cell(x, y) and (x, y) in self.get_moves():
            self.x = x
            self.y = y
        else:
            raise ValueError(f"Cannot move {self.name} from positions {self.x, self.y} to positions {x , y}")

    def can_eat(self, other_figure):
        """Tell if given piece can eat other figure."""
        if is_legal_chess_cell(other_figure.x, other_figure.y) and (other_figure.x, other_figure.y) in self.get_moves():
            return True
        return False

    def get_moves(self):
        """Get all moves. Uses cache for efficiency."""
        if (self.name, self.x, self.y) in cached_moves:
            return cached_moves.get((self.name, self.x, self.y))
        else:
            allowed_moves = self.get_piece_moves()
            cached_moves[(self.name, self.x, self.y)] = allowed_moves
            return allowed_moves

    def can_eat_in_moves(self, other_figure, number_of_moves):
        """Tell if given piece can eat other figure in given number of moves."""
        # Maybe we can eat in first move
        if self.can_eat(other_figure):
            return True
        # If one move left and cannot eat, return False
        if number_of_moves == 1:
            return False
        # If not use recursion to check for all possible moves
        x_start = self.x
        y_start = self.y
        possible_moves = self.get_piece_moves()
        for possible_move in possible_moves:
            # Move to new position
            self.move(possible_move[0], possible_move[1])
            # Check for all possible moves, might be overkill, but jut for fun:)
            if self.can_eat_in_moves(other_figure, number_of_moves - 1):
                self.move(x_start, y_start)
                return True
            self.move(x_start, y_start)
        return False

    @abstractmethod
    def get_piece_moves(self):
        """This is the only different method for class implementation."""
        pass


class StaticFigure(ChessFigure):
    """
    This class represents figures, which cannot move.
    This is for given exercise only, do not use in the chess:)
    """
    def __init__(self, x, y):
        super().__init__('Other Figure', x, y)

    def get_piece_moves(self):
        raise ValueError("Cannot get moves of a static figure.")


class Queen(ChessFigure):

    def __init__(self, x, y):
        super().__init__('Queen', x, y)

    def get_piece_moves(self):
        vertical_moves = get_cells_on_same_vertical(self.x, self.y)
        horizontal_moves = get_cells_on_same_horizontal(self.x, self.y)
        diagonal_moves = get_cells_on_same_diagonal(self.x, self.y)
        all_possible_moves = vertical_moves.union(horizontal_moves).union(diagonal_moves)
        return all_possible_moves


class Knight(ChessFigure):

    def __init__(self, x, y):
        super().__init__('Knight', x, y)

    def get_piece_moves(self):
        possible_moves = set()
        for move in HORSE_MOVE_DIRECTION:
            if is_legal_chess_cell(self.x + move[0], self.y + move[1]):
                possible_moves.add((self.x + move[0], self.y + move[1]))
        return possible_moves



if __name__ == '__main__':
    # Queen tests
    enemy_queen = Queen(3, 3)

    my_figure = StaticFigure(3, 0)
    print(f"{enemy_queen} can eat {my_figure}:", enemy_queen.can_eat(my_figure))
    my_figure = StaticFigure(0, 0)
    print(f"{enemy_queen} can eat {my_figure}:", enemy_queen.can_eat(my_figure))
    my_figure = StaticFigure(0, 3)
    print(f"{enemy_queen} can eat {my_figure}:", enemy_queen.can_eat(my_figure))
    my_figure = StaticFigure(6, 2)
    # Not on same horizontal, vertical, diagonal -> False
    print(f"{enemy_queen} can eat {my_figure}:", enemy_queen.can_eat(my_figure))

    # Knight tests
    enemy_knight = Knight(3, 4)

    my_figure = StaticFigure(2, 2)
    print(f"{enemy_knight} can eat {my_figure}:", enemy_knight.can_eat(my_figure))
    my_figure = StaticFigure(5, 5)
    print(f"{enemy_knight} can eat {my_figure}:", enemy_knight.can_eat(my_figure))
    my_figure = StaticFigure(5, 2)
    print(f"{enemy_knight} can eat {my_figure}:",enemy_knight.can_eat(my_figure))

    # Task 2 knight tests
    my_knight = Knight(3, 4)
    enemy_figure = StaticFigure(1, 7)
    print(f"{my_knight} can eat {enemy_figure}:", enemy_knight.can_eat(my_figure))
    print(f"{my_knight} can eat {enemy_figure} in 2 moves:", my_knight.can_eat_in_moves(enemy_figure, 2))
    print(f"{my_knight} can eat {enemy_figure} in 3 moves:", my_knight.can_eat_in_moves(enemy_figure, 3))

    enemy_figure = StaticFigure(0, 7)
    print(f"{my_knight} can eat {enemy_figure} in 2 moves:", my_knight.can_eat_in_moves(enemy_figure, 2))

    my_knight = Knight(0, 0)
    enemy_figure = StaticFigure(7, 7)
    print(f"{my_knight} can eat {enemy_figure} in 5 moves:", my_knight.can_eat_in_moves(enemy_figure, 5))
    # Proof: https://chess.stackexchange.com/questions/34588/how-many-moves-needed-for-a-knight-to-go-from-any-square-to-any-other-square
    print(f"{my_knight} can eat {enemy_figure} in 6 moves:", my_knight.can_eat_in_moves(enemy_figure, 6))
