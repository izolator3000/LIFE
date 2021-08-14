from numpy import sign


class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({str(self.x)}, {str(self.y)})"

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y


class Coords(Pair):
    def __init__(self, x=-1, y=-1):
        super(Coords, self).__init__(x, y)

    def neighbors(self):
        return (Coords(self.x + i, self.y + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if not i == j == 0)

    def get_coords_on_line(start, finish):
        res = [start]
        if start == finish:
            return res

        distance = Pair(abs(finish.x - start.x), abs(finish.y - start.y))
        coefficents = Pair(sign(finish.x - start.x), sign(finish.y - start.y))
        step = max(distance.x, distance.y)
        counters = Pair(0, 0)
        current_position = Coords(start.x, start.y)

        while current_position != finish:
            counters.x += distance.x
            counters.y += distance.y
            if counters.x >= step:
                counters.x = counters.x - step
                current_position.x += coefficents.x
            if counters.y >= step:
                counters.y = counters.y - step
                current_position.y += coefficents.y
            res.append(Coords(current_position.x, current_position.y))
        return res

    def _check_intersection(first_start, first_finish, second_start, second_finish):
        if second_start.x >= first_finish.x or second_start.y >= first_finish.y:
            return False
        if second_finish.x <= first_start.x or second_finish.y <= first_start.y:
            return False
        return True

    def calculate_intersection(first_start, first_finish, second_start, second_finish):

        if Coords._check_intersection(first_start, first_finish, second_start, second_finish):
            intersection_coords_start = Coords()
            intersection_coords_start.x = max(first_start.x, second_start.x)
            intersection_coords_start.y = max(first_start.y, second_start.y)
            intersection_coords_finish = Coords()
            intersection_coords_finish.x = min(first_finish.x, second_finish.x)
            intersection_coords_finish.y = min(first_finish.y, second_finish.y)
            return Pair(intersection_coords_start, intersection_coords_finish)


class Cell:
    def __init__(self, is_alive=True, number_of_neighbors=0):
        self.is_alive = is_alive
        self.number_of_neighbors = number_of_neighbors

    def __repr__(self):
        return f"({self.is_alive}, {self.number_of_neighbors})"

    def add_neighbor(self):
        self.number_of_neighbors += 1

    def dead(self):
        self.is_alive = False

    def alive(self):
        self.is_alive = True

    def reset(self):
        self.is_alive = True
        self.number_of_neighbors = 0
