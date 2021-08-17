from Component import Component
from coords_cell import Pair, Coords
from field import Field
from mouse import MouseEvents
from Subscriber import Subscriber
import pygame


class Screen(Component, Subscriber):
    def __init__(self, start: Coords, width: int, height: int, cell_size: int, generation_speed=15,
                 cell_color=(255, 255, 255, 255), background_color=(0, 0, 0, 255)):
        super().__init__()
        self._field = Field()
        self._start = start
        self._width = width
        self._height = height
        self._cell_size = cell_size
        self._cell_color = cell_color
        self._background_color = background_color
        self._generation_speed = 1000 // generation_speed
        self._generation_timer = 0
        self._generation_clock = pygame.time.Clock()
        self._cursor_status = Pair(False, Pair(0, 0))  # (1,0) (1,0) (1,1)  # не на экране, зоны смещения
        self._is_active = False  # находится ли экран в активном режиме
        self._offset_zone_coefficient = 7
        self._build_mode = Pair(False, 0)  # активен ли режим добавления новых клеток и тип этого режима
        self._prev_coord = Coords(-1, -1)  # абстрактные координаты
        self._cells_rects = []
        self._cells_changed = False
        # offset
        self._offset = Coords(0, 0)  # при использовании округлять значения до целых чисел
        self._offset_clock = pygame.time.Clock()
        self._cursor_old_position = Coords(0, 0)
        self._speed = 0.3

    def _cursor_on_screen(self, position):
        if position.x < self._start.x or \
                position.x > self._start.x + self._width or \
                position.y < self._start.y or \
                position.y > self._start.y + self._height:
            self._cursor_status = Pair(False, Pair(0, 0))
            return False
        return True

    def _offset_zones_status(self, position):  # работает только если курсор на экране
        res = Pair(0, 0)
        if position.x < self._start.x + self._width / self._offset_zone_coefficient:
            res.x = 1
        if position.x > self._start.x + self._width * (
                (self._offset_zone_coefficient - 1) / self._offset_zone_coefficient):
            res.x = -1
        if position.y < self._start.y + self._height / self._offset_zone_coefficient:
            res.y = -1
        if position.y > self._start.y + self._height * (
                (self._offset_zone_coefficient - 1) / self._offset_zone_coefficient):
            res.y = 1
        return res

    def _update_cursor(self, data: tuple):  # типы событий:мышь подвинута и фокус получен/потерян
        event, position = data
        if event == MouseEvents.FOCUS_REALISED or not self._cursor_on_screen(position):
            self._cursor_status = Pair(False, Pair(0, 0))
            return
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

    def _get_abstract_coords(self, coords) -> Coords:
        x = (coords.x - (self._start.x + self._width // 2) - int(self._offset.x)) // self._cell_size
        y = (self._start.y + self._height // 2 - coords.y - int(self._offset.y)) // self._cell_size + 1
        return Coords(x, y)

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
        self._cells_changed = True  # улучшить

    def update(self, data: tuple):  # Keys pressed/realised, Focus get/lost position changed
        event, position = data

        if event == MouseEvents.POSITION_CHANGED or event == MouseEvents.FOCUS_REALISED or event == MouseEvents.FOCUS_GET:
            self._update_cursor(data)

        new_cell_coord = self._get_new_cells_coords(data)

        self._set_new_cells(new_cell_coord)

    def _get_new_cell_generation(
            self):  # возвращает новое поколение или None,если новое поколение не отличается от старого
        if self._cells_changed and not self._is_active:
            return self._field.current_generation()

        if not self._is_active:
            return

        self._generation_timer += self._generation_clock.tick()
        if self._generation_timer > self._generation_speed:
            self._generation_timer = 0
            self._cells_changed = True
            return self._field.next_generation()
        if self._cells_changed:
            return self._field.current_generation()

    def _update_cells_rects(self):  # Обновляет список прямоугольников,которые затем рисуются
        cells = self._get_new_cell_generation()
        if cells is None:
            return

        self._cells_rects = []
        for cell in cells:
            cell_rect = self._get_cell_rect(cell)
            if cell_rect is not None:
                self._cells_rects.append(cell_rect)

        self._cells_changed = False

    def change_play_mode(self):  # изменяет режим экрана на противоположный
        self._is_active = not self._is_active

    def draw(self, display: pygame.Surface):

        self._calculate_offset()
        self._update_cells_rects()

        screen_rect = pygame.Rect(self._start.x, self._start.y, self._width, self._height)
        pygame.draw.rect(display, self._background_color, screen_rect)

        for rect in self._cells_rects:
            pygame.draw.rect(display, self._cell_color, rect)

    def _get_cell_rect(self, coords):
        absolute_coords = Coords()
        absolute_coords.x = coords.x * self._cell_size + int(self._offset.x) + self._width // 2 + self._start.x
        absolute_coords.y = -coords.y * self._cell_size - int(self._offset.y) + self._height // 2 + self._start.y
        rect_coords = Coords.calculate_intersection(self._start,
                                                    Coords(self._start.x + self._width, self._start.y + self._height),
                                                    absolute_coords,
                                                    Coords(absolute_coords.x + self._cell_size,
                                                           absolute_coords.y + self._cell_size))
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
        self._cells_changed = True

    def reset(self):
        self._cells_changed = True
        self._field.clear()

    def reverse_game(self):
        self._field.reverse_game()
