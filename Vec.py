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

    def __sub__(self, other):
        return Vec2(self._x - other._x, self._y - other._y)

    def magnitude(self):
        return sqrt(self._x**2 + self._y**2)