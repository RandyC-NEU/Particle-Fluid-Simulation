from math import sqrt

'''
    Simple 2-element vector class that supports
        -Adding two vectors
        -Subtracting two vectors
        -Finding the magnitude of a vector
'''
class Vec2:
    _x : float
    _y : float
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def zeros():
        return Vec2(0.0, 0.0)

    def ones():
        return Vec2(1.0, 1.0)

    def __add__(self, other):
        return Vec2(self._x + other._x, self._y + other._y)

    def __mul__(self, multiple):
        return Vec2(self._x * multiple, self._y * multiple)

    def __rmul__(self, multiple):
        return self * multiple

    def __sub__(self, other):
        return Vec2(self._x - other._x, self._y - other._y)

    def __getitem__(self, i) -> float:
        assert(i < 2)
        return (self._y if (i == 1) else self._x)

    def __str__(self):
        return f'[x = {self._x}, y = {self._y}]'

    def magnitude(self):
        return sqrt(self._x**2 + self._y**2)