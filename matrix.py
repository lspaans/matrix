#!/usr/bin/env python

import math
import os
import random
import sys
import time

HEIGHT = 25
WIDTH = 50


class Move(object):

    def rotate(self, shape, angle):
        pass


class Shape(object):

    def __init__(self):
        self.points = []

    def __iter__(self):
        return iter(self.points)

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self._points = value

    def __str__(self):
        return str(self.points)

    def __repr__(self):
        return self.__str__()


class Circle(Shape):

    def __init__(self, x0=0, y0=0, radius=None):
        super().__init__()

        self.radius = min(HEIGHT, WIDTH) if radius is None else radius
        self._init_origin(x0, y0)
        self._init_points()

    def _init_origin(self, x0, y0):
        self.x0 = x0
        self.y0 = y0

    def _init_points(self):
        angle = .0
        while angle < 360:
            x = self.radius * math.cos(angle*(math.pi/180)) + self.x0
            y = (math.sin(angle*(math.pi/180)) * self.radius) + self.y0
            self.points.append((x, y))
            angle += 5 * (1.0 / self.radius)

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    @property
    def x0(self):
        return self._x0

    @x0.setter
    def x0(self, value):
        self._x0 = value

    @property
    def y0(self):
        return self._y0

    @y0.setter
    def y0(self, value):
        self._y0 = value


class Line(Shape):

    def __init__(self, x1=0, y1=0, x2=WIDTH, y2=HEIGHT):
        super().__init__()
        self._init_coordinates(x1, y1, x2, y2)
        self._init_points()

    def _get_sorted_coordinates(self, pos1, pos2):
            return min(pos1, pos2), max(pos1, pos2)

    def _init_coordinates(self, x1, y1, x2, y2):
        self.x_min, self.x_max = self._get_sorted_coordinates(x1, x2)
        self.y_min, self.y_max = self._get_sorted_coordinates(y1, y2)

    def _init_points(self):
        self.points = [(
            pos,
            (self.slope * pos) + self.pos_shift
        )[::self.direction] for pos in self.positions]

    @property
    def direction(self):
        return 1 if self.x_axis else -1

    @property
    def pos_shift(self):
        return self.y_min if self.x_axis else self.x_min

    @property
    def positions(self):
        return range(
            self.x_min if self.x_axis else self.y_min,
            (self.x_max if self.x_axis else self.y_max) + 1
        )

    @property
    def slope(self):
        return float(
            min(self.x_delta, self.y_delta)
        ) / max(self.x_delta, self.y_delta)

    @slope.setter
    def slope(self, value):
        self._slope = value

    @property
    def x_axis(self):
        return self.x_delta > self.y_delta

    @property
    def x_delta(self):
        return self.x_max - self.x_min

    @property
    def x_max(self):
        return self._x_max

    @x_max.setter
    def x_max(self, value):
        self._x_max = value

    @property
    def x_min(self):
        return self._x_min

    @x_min.setter
    def x_min(self, value):
        self._x_min = value

    @property
    def y_delta(self):
        return self.y_max - self.y_min

    @property
    def y_max(self):
        return self._y_max

    @y_max.setter
    def y_max(self, value):
        self._y_max = value

    @property
    def y_min(self):
        return self._y_min

    @y_min.setter
    def y_min(self, value):
        self._y_min = value


class Cell(object):

    _states = (".", "o", "O", "o")

    def __init__(self):
        self._state = None

        self.off()

    def inc(self):
        self.state = (self.state + 1) % len(self.states)

    def toggle(self):
        if self.state:
            self.off()
        else:
            self.on()

    def off(self):
        self.state = 0

    def on(self):
        self.state = 1

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value=0):
        self._state = value % len(self.states)

    @property
    def states(self):
        return Cell._states

    def __str__(self):
        return self.states[self.state]

    def __repr__(self):
        return self.__str__()


class Matrix(object):

    def __init__(self, height=HEIGHT, width=WIDTH):
        self.height = height
        self.width = width
        self.cells = [Cell() for _ in range(height * width)]

    def cell(self, col=0, row=0):
        return self.cols[col][row]

    @property
    def cells(self):
        return self._cells

    @cells.setter
    def cells(self, cells):
        self._cells = cells

    def col(self, col=0):
        return [self.cells[number] for number in range(
            col % self.width,
            self.height * self.width,
            self.width
        )]

    @property
    def cols(self):
        return [self.col(number) for number in range(self.width)]

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    def row(self, row=0):
        return [self.cells[number] for number in range(
            (row % self.height) * self.width,
            ((row % self.height) * self.width) + self.width
        )]

    @property
    def rows(self):
        return [self.row(number) for number in range(self.height)]

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    def __str__(self):
        return "\n".join([
            "".join(str(cell) for cell in row) for row in self.rows[::-1]
        ])

    def __repr__(self):
        return self.__str__()


class Projection(object):

    def __init__(self, height=HEIGHT, width=WIDTH):
        self.height = height
        self.width = width
        self.shapes = []

    def _init_matrix(self):
        self._matrix = Matrix(self.height, self.width)
        for shape in self.shapes:
            for x, y in shape:
                try:
                    #self._matrix.cell(x, y).inc()
                    self._matrix.cell(round(x), round(y)).on()
                except (IndexError,):
                    pass

    def add_shape(self, shape):
        self.shapes.append(shape)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def shapes(self):
        return self._shapes

    @shapes.setter
    def shapes(self, value):
        self._shapes = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    def __str__(self):
        self._init_matrix()
        return str(self._matrix)

    def __repr__(self):
        return self.__str__()


def main():
    projection = Projection()
    projection.shapes = [
        Line(5, 7, 14, 19),
        Line(3, 8, 25, 20),
        Circle(14, 12, 11)
    ]
    print(projection)


if __name__ == "__main__":
    main()
