class Coords:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x=}, {self.y=})"

    def neighbors(self):
        return (Coords(self.x + i, self.y + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if not i == j == 0)


class Cell:
    def __init__(self, is_alive=True, number_of_neighbors=0):
        self.is_alive = is_alive
        self.number_of_neighbors = number_of_neighbors

    def __repr__(self):
        return f"({self.is_alive=}, {self.number_of_neighbors=})"

    def add_neighbor(self):
        self.number_of_neighbors += 1

    def dead(self):
        self.is_alive = False

    def alive(self):
        self.is_alive = True

    def reset(self):
        self.is_alive = True
        self.number_of_neighbors = 0
