from Component import Component
from coords_cell import Pair, Coords
from field import Field
from mouse import MouseEvents
from Subscriber import Subscriber
import pygame
from numpy import sign


class Screen(Component, Subscriber):
    def __init__(self, start: Coords, width: int, height: int, cell_size: int, generation_speed=15,
                 cell_color=(255, 255, 255, 255), background_color=(0, 0, 0, 255)):
        super().__init__()
        self._field = Field()
        self._start = start
        self._width = width
        self._height = height
        self.cell_size = cell_size
        self._cell_color = cell_color
        self._background_color = background_color
        self._generation_speed = 1000 // generation_speed
        self._generation_timer = 0
        self._generation_clock = pygame.time.Clock()
        self._cursor_status = Pair(False, Pair(0, 0))  # (1,0) (1,0) (1,1)  # не на экране, зоны смещения
        self._is_active = False  # находится ли экран в активном режиме
        self._offset_zone_coefficient = 10
        self._build_mode = Pair(False, 0)  # активен ли режим добавления новых клеток и тип этого режима
        self._prev_coord = Coords(-1, -1)  # абстрактные координаты
        self._zoom_speed = 2
        # offset

        self._offset = Coords(0, 0)  # при использовании округлять значения до целых чисел
        self._offset_clock = pygame.time.Clock()
        self._cursor_old_position = Coords(0, 0)
        self._speed = 0.3
        # test
        self._cursor_continous_coord = None

    @property
    def cell_size(self):
        return int(self._cell_size)

    @cell_size.setter
    def cell_size(self, value):
        self._cell_size = value

    def _cursor_on_screen(self, position):
        if position.x < self._start.x or position.x > self._start.x + self._width:
            self._cursor_status = Pair(False, Pair(0, 0))
            return False

        if position.y < self._start.y or position.y > self._start.y + self._height:
            self._cursor_status = Pair(False, Pair(0, 0))
            return False
        return True

    def _offset_zones_status(self, position):  # работает только если курсор на экране
        res = Pair(0, 0)
        if position.x < self._start.x + self._width / self._offset_zone_coefficient:
            res.x = -1
        if position.x > self._start.x + self._width * (
                (self._offset_zone_coefficient - 1) / self._offset_zone_coefficient):
            res.x = 1
        if position.y < self._start.y + self._height / self._offset_zone_coefficient:
            res.y = 1
        if position.y > self._start.y + self._height * (
                (self._offset_zone_coefficient - 1) / self._offset_zone_coefficient):
            res.y = -1
        return res

    def _update_cursor(self, data: tuple):  # типы событий:мышь подвинута и фокус получен/потерян
        event, position = data

        if event == MouseEvents.FOCUS_REALISED or not self._cursor_on_screen(position):
            self._cursor_status = Pair(False, Pair(0, 0))
            self._cursor_continous_coord = None
            return
        # FOCUS_GET,POSITION_CHANGED,кусор на экране
        self._cursor_continous_coord = position

        self._cursor_status = Pair(True, self._offset_zones_status(position))

    def _get_new_cells_coords(self, data: tuple):  # не трогать!!!!
        event, position = data

        if not self._build_mode.x:
            if not self._is_active and self._cursor_status.x:
                if event == MouseEvents.LEFT_KEY_PRESSED:
                    self._build_mode.x = True
                    self._build_mode.y = 1  # добавление клеток
                    return position
                if event == MouseEvents.RIGHT_KEY_PRESSED:
                    self._build_mode.x = True
                    self._build_mode.y = -1  # удаление клеток
                    return position

        else:
            if self._is_active or not self._cursor_status.x:
                self._build_mode.x = False
                self._prev_coord = Coords(-1, -1)
                return
            if (event == MouseEvents.LEFT_KEY_REALISED and self._build_mode.y == 1) or (
                    event == MouseEvents.RIGHT_KEY_REALISED and self._build_mode.y == -1):
                self._build_mode.x = False
                self._prev_coord = Coords(-1, -1)
            if event == MouseEvents.POSITION_CHANGED:
                return position

    def _get_abstract_coords(self, coords):  # использовать только если мышь на экране

        res = Coords()
        res.x = (coords.x - (self._start.x + self._width // 2) + int(self._offset.x)) // self.cell_size
        res.y = (self._start.y + self._height // 2 - coords.y + int(self._offset.y)) // self.cell_size + 1
        return res

    def _set_new_cells(self, build_start_coords):

        if build_start_coords is None:
            return
        new_coord = self._get_abstract_coords(build_start_coords)
        if self._prev_coord == Coords(-1, -1):
            new_coords = [new_coord]

        else:
            new_coords = Coords.get_coords_on_line(new_coord, self._prev_coord)

        for elem in new_coords:
            if self._build_mode.y == 1:

                self._field.add_alive_cell(elem)
            else:

                self._field.del_alive_cell(elem)

        self._prev_coord = new_coord

    def _calculate_zoom_offset(self, cursor_position, new_cell_size: int):
        coords = self._get_abstract_coords(cursor_position)

        distance = Coords(abs(coords.x), abs(coords.y))
        offset_odds = Pair(sign(coords.x), sign(coords.y))
        offset = self._calculate_cell_offset(cursor_position, new_cell_size)

        offset.x += distance.x * offset_odds.x * (new_cell_size - self.cell_size)
        offset.y += distance.y * offset_odds.y * (new_cell_size - self.cell_size)
        self._offset.x += offset.x
        self._offset.y += offset.y

    def _get_next_cell_size_val(self, direction):  # возвращает дробное значение которое должен будет принять cell_size
        if direction == 1:
            if self.cell_size == 1:
                return 2

            return self._cell_size + self.cell_size / self._zoom_speed
        else:
            value = self._cell_size - self._cell_size / self._zoom_speed
            if value >= 1:
                return value
            else:
                return self._cell_size

    def _get_cursor_position_on_cell(self, cursor_position: Pair):
        converted_cursor_position = Coords(cursor_position.x - (self._start.x + self._width // 2) + int(self._offset.x),
                                           self._start.y + self._height // 2 - cursor_position.y + int(self._offset.y))
        cell_coords = self._get_abstract_coords(cursor_position)
        cell_start = Coords(cell_coords.x * self.cell_size, cell_coords.y * self.cell_size)
        return Coords(abs(converted_cursor_position.x - cell_start.x), abs(converted_cursor_position.y - cell_start.y))

    def _calculate_cell_offset(self, cursor_position: Pair, new_cell_size):
        if self.cell_size == 1:
            return Coords(0, 0)

        cursor_position_on_cell = self._get_cursor_position_on_cell(cursor_position)

        offset = Coords()
        offset.x = (cursor_position_on_cell.x / (self.cell_size - 1)) * (new_cell_size - self.cell_size)
        offset.y = -((cursor_position_on_cell.y / (self.cell_size - 1)) * (new_cell_size - self.cell_size))

        return offset

    def _change_zoom(self, data: tuple):
        event, position = data
        if not self._cursor_status.x:
            return
        if event == MouseEvents.WHEEL_MOVED_FORWARD:
            float_new_cell_size = self._get_next_cell_size_val(1)
        else:
            float_new_cell_size = self._get_next_cell_size_val(-1)

        new_cell_size = int(float_new_cell_size)
        if new_cell_size == self.cell_size:
            self.cell_size = float_new_cell_size
            return
        self._calculate_zoom_offset(data[1], new_cell_size)
        self.cell_size = float_new_cell_size

    def update(self, data: tuple):  # Keys pressed/realised, Focus get/lost position changed,mheel moved
        event, position = data
        if event == MouseEvents.WHEEL_MOVED_FORWARD or event == MouseEvents.WHEEL_MOVED_BACKWARD:
            self._change_zoom(data)
        if event == MouseEvents.POSITION_CHANGED or event == MouseEvents.FOCUS_REALISED or event == MouseEvents.FOCUS_GET:
            self._update_cursor(data)

        new_cell_coord = self._get_new_cells_coords(data)
        self._set_new_cells(new_cell_coord)

    def _get_new_cell_generation(self):  # возвращает поколение для отрисовки
        if not self._is_active:
            return self._field.current_generation()


        self._generation_timer += self._generation_clock.tick()
        if self._generation_timer > self._generation_speed:
            self._generation_timer = 0
            return self._field.new_generation()
        else:
            return self._field.current_generation()

    def change_play_mode(self):  # изменяет режим экрана на противоположный
        self._is_active = not self._is_active
        if self._is_active:
            self._field.remember_current_generation()

    def set_start_generation(self):
        self._field.set_start_generation()
        pass

    def get_new_step(self):
        self._field.new_generation()

    def clear_screen(self):
        self._field.clear_cells()

    def draw(self, display: pygame.Surface):

        self._calculate_offset()
        cells = self._get_new_cell_generation()

        screen_rect = pygame.Rect(self._start.x, self._start.y, self._width, self._height)
        pygame.draw.rect(display, self._background_color, screen_rect)

        for cell in cells:
            cell_rect = self._get_cell_rect(cell)
            if cell_rect is not None:
                pygame.draw.rect(display, self._cell_color, cell_rect)

    def _get_cell_rect(self, coords):
        absolute_coords = Coords()
        absolute_coords.x = coords.x * self.cell_size - int(self._offset.x) + self._width // 2 + self._start.x
        absolute_coords.y = -coords.y * self.cell_size + int(self._offset.y) + self._height // 2 + self._start.y
        rect_coords = Coords.calculate_intersection(self._start,
                                                    Coords(self._start.x + self._width, self._start.y + self._height),
                                                    absolute_coords,
                                                    Coords(absolute_coords.x + self.cell_size,
                                                           absolute_coords.y + self.cell_size))
        if rect_coords is not None:
            size = (rect_coords.y.x - rect_coords.x.x, rect_coords.y.y - rect_coords.x.y)
            return pygame.Rect(rect_coords.x.x, rect_coords.x.y, *size)

    def _calculate_offset(self):
        if self._cursor_status.y == Pair(0, 0):
            self._cursor_old_position = Pair(0, 0)
            return
        if self._cursor_status.y != self._cursor_old_position:
            self._cursor_old_position = self._cursor_status.y
            self._offset_clock.tick()
            return

        time = self._offset_clock.tick()
        distance = self._speed * time
        self._offset.x += distance * self._cursor_status.y.x
        self._offset.y += distance * self._cursor_status.y.y
        if self._build_mode.x:
            self._set_new_cells(self._cursor_continous_coord)
