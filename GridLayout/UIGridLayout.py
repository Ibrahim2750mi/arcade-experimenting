from typing import Iterable, NamedTuple

from arcade.gui import UILayout, UIWidget


# copied from https://github.com/pythonarcade/arcade/blob/development/arcade/gui/widgets.py no edits
class _Rect(NamedTuple):
    x: float
    y: float
    width: float
    height: float

    def move(self, dx: float = 0, dy: float = 0):
        """Returns new Rect which is moved by dx and dy"""
        return _Rect(self.x + dx, self.y + dy, self.width, self.height)

    def collide_with_point(self, x, y):
        left, bottom, width, height = self
        return left < x < left + width and bottom < y < bottom + height

    def scale(self, scale: float) -> "_Rect":
        """Returns a new rect with scale applied"""
        return _Rect(
            int(self.x * scale),
            int(self.y * scale),
            int(self.width * scale),
            int(self.height * scale),
        )

    def resize(self, width=None, height=None):
        width = width or self.width
        height = height or self.height
        return _Rect(self.x, self.y, width, height)

    @property
    def size(self):
        return self.width, self.height

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.width

    @property
    def bottom(self):
        return self.y

    @property
    def top(self):
        return self.y + self.height

    @property
    def center_x(self):
        return self.x + self.width / 2

    @property
    def center_y(self):
        return self.y + self.height / 2

    @property
    def center(self):
        return self.left, self.bottom

    @property
    def position(self):
        """Bottom left coordinates"""
        return self.left, self.bottom

    def align_top(self, value: float) -> "_Rect":
        """Returns new Rect, which is aligned to the top"""
        diff_y = value - self.top
        return self.move(dy=diff_y)

    def align_bottom(self, value: float) -> "_Rect":
        """Returns new Rect, which is aligned to the bottom"""
        diff_y = value - self.bottom
        return self.move(dy=diff_y)

    def align_left(self, value: float) -> "_Rect":
        """Returns new Rect, which is aligned to the left"""
        diff_x = value - self.left
        return self.move(dx=diff_x)

    def align_right(self, value: float) -> "_Rect":
        """Returns new Rect, which is aligned to the right"""
        diff_x = value - self.right
        return self.move(dx=diff_x)

    def align_center(self, center_x, center_y):
        """Returns new Rect, which is aligned to the center x and y"""
        diff_x = center_x - self.center_x
        diff_y = center_y - self.center_y
        return self.move(dx=diff_x, dy=diff_y)

    def align_center_x(self, value: float) -> "_Rect":
        """Returns new Rect, which is aligned to the center_x"""
        diff_x = value - self.center_x
        return self.move(dx=diff_x)

    def align_center_y(self, value: float) -> "_Rect":
        """Returns new Rect, which is aligned to the center_y"""
        diff_y = value - self.center_y
        return self.move(dy=diff_y)


class UIGridLayout(UILayout):
    """
    Places widget in a grid layout.

    :param float x: x coordinate of bottom left
    :param float y: y coordinate of bottom left
    :param align_horizontal: Align children in orthogonal direction (x: left, center, right)
    :param align_vertical: Align children in orthogonal direction (y: top, center, bottom)
    :param children: Initial children, more can be added
    :param size_hint: A hint for :class:`UILayout`, if this :class:`UIWidget` would like to grow
    :param size_hint_min: Min width and height in pixel
    :param size_hint_max: Max width and height in pixel
    :param horizontal_spacing: Space between columns
    :param vertical_spacing: Space between rows
    :param column_count: Number of columns in the grid, can be changed
    :param row_count: Number of rows in the grid, can be changed
    """
    def __init__(self, x=0,
                 y=0,
                 align_horizontal="center",
                 align_vertical="center",
                 children: Iterable[UIWidget] = tuple(),
                 size_hint=None,
                 size_hint_min=None,
                 size_hint_max=None,
                 horizontal_spacing: int = 0,
                 vertical_spacing: int = 0,
                 column_count: int = 1,
                 row_count: int = 1, style=None, **kwargs):

        super(UIGridLayout, self).__init__(x=x, y=y, width=0, height=0, children=children,
                                           size_hint=size_hint, size_hint_min=size_hint_min,
                                           size_hint_max=size_hint_max, style=style, **kwargs)

        self._horizontal_spacing = horizontal_spacing
        self._vertical_spacing = vertical_spacing

        self._child_dict = {}

        self.column_count = column_count
        self.row_count = row_count

        self.align_horizontal = align_horizontal
        self.align_vertical = align_vertical

    def add_widget(self, child: "UIWidget", col_num: int, row_num: int) -> "UIWidget":
        """
        Adds widgets in the grid.
        :param child: The widget which is to be addded in the grid
        :param col_num: The column number in which the widget is to be added (first column is numbered 0)
        :param row_num: The row number in which the widget is to be added (first row is numbered 0)
        """
        self._child_dict[child] = (col_num, row_num)
        super(UILayout, self).add(child)

    def do_layout(self):
        initial_top = self.top
        initial_left_x = self.left
        start_y = self.top

        if not self._child_dict:
            self.rect = _Rect(self.left, self.bottom, 0, 0)
            return

        # row
        max_width_per_column = [0 for _ in range(self.column_count)]
        max_height_per_row = [0 for _ in range(self.row_count)]

        child_sorted_row_wise = [[] for _ in range(self.row_count)]

        for child, (col_num, row_num) in self._child_dict.items():

            if child.width > max_width_per_column[col_num]:
                max_width_per_column[col_num] = child.width

            if child.height > max_height_per_row[row_num]:
                max_height_per_row[row_num] = child.height

            child_sorted_row_wise[row_num].append(child)


        # row wise rendering children
        new_height = sum(max_height_per_row) + (self.row_count - 1) * self._vertical_spacing
        new_width = sum(max_width_per_column) + (self.column_count - 1) * self._horizontal_spacing

        for row_num, row in enumerate(child_sorted_row_wise):
            max_height = max_height_per_row[row_num] + self._vertical_spacing
            center_y = start_y - (max_height // 2)

            start_x = initial_left_x

            for col_num, child in enumerate(row):
                max_width = max_width_per_column[col_num] + self._horizontal_spacing
                center_x = start_x +  max_width // 2

                if self.align_vertical == "top":
                    new_rect = child.rect.align_top(start_y)
                elif self.align_vertical == "bottom":
                    new_rect = child.rect.align_bottom(start_y - max_height)
                else:
                    new_rect = child.rect.align_center_y(center_y)

                if self.align_horizontal == "left":
                    new_rect = new_rect.align_left(start_x)
                elif self.align_horizontal == "right":
                    new_rect = new_rect.align_right(start_x + max_width)
                else:
                    new_rect = new_rect.align_center_x(center_x)

                if new_rect != child.rect:
                    child.rect = new_rect
                start_x += max_width

            start_y -= max_height

        self.rect = _Rect(self.left, initial_top - new_height, new_width, new_height).align_top(initial_top)
