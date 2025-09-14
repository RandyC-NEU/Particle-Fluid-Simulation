from abc import ABC, abstractmethod
from typing import Callable, Tuple, List
from math import pi

'''
    Interface for any object that needs its parameters updated at every time step
'''
class Simulation(ABC):
    @abstractmethod
    def update(self, dt):
        pass

deg2rad = lambda theta: theta * (pi/180)

class BoundaryFunction:
    _x_func      : Callable[[float], float]
    _y_func      : Callable[[float], float]
    _input_range : Tuple[float, float]

    def __init__(self,
                 x_func: Callable[[float], float],
                 y_func: Callable[[float], float],
                 input_range: Tuple[float, float]):
        self._x_func = x_func
        self._y_func = y_func
        self._input_range = input_range

    def plot(self, granularity: float = 0.1) -> Tuple[List[float]]:
        points_x = []
        points_y = []
        start = self._input_range[0]
        while start <= self._input_range[1]:
            points_x.append(self._x_func(deg2rad(start)))
            points_y.append(self._y_func(deg2rad(start)))
            start += granularity
        return (points_x, points_y)

class Boundary:
    _funcs : List[BoundaryFunction]

    def __init__(self, funcs: List[BoundaryFunction]):
        self._funcs = funcs

    def plot(self, i: int, granularity: float = 0.01) -> Tuple[List[float]]:
        assert i < len(self._funcs)
        return self._funcs[i].plot(granularity)

    def calc_wall_distance(x: float) -> float:
        return 0.0