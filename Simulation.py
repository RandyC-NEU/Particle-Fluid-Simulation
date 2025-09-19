from abc import ABC, abstractmethod
from typing import Callable, Tuple, List, Dict
from math import pi, tan
from scipy.optimize import root_scalar
import numpy as np
from Vec import Vec2

'''
    Interface for any object that needs its parameters updated at every time step
'''
class Simulation(ABC):
    @abstractmethod
    def update(self, dt):
        pass

SimulationParameterFunc = Callable[[Simulation, Simulation], float]
deg2rad = lambda theta: theta * (pi/180)

class PhysicsConstants:
    GRAVITY_M_S__2:                   Vec2 = Vec2(0, -9.81)
    DENSITY_AIR_25C__1_ATM:           float = 1.184
    DYNAMIC_VISCOSITY_AIR_25C__1_ATM: float = 1.849*1e-5
    DENSITY_SAND__KG_M__3:            float = 1600

class MathConstants:
    find_sphere_volume: Callable[[float], float] = lambda radius: (4/3)*np.pi*(radius**3)

class BoundaryFunction:
    BoundaryLutEntry = List[Tuple[float, float, float]]
    _x_func       : Callable[[float], float]
    _y_func       : Callable[[float], float]

    _boundary_lut : BoundaryLutEntry = None
    _input_range  : Tuple[float, float]

    def __init__(self,
                 x_func: Callable[[float], float],
                 y_func: Callable[[float], float],
                 input_range: Tuple[float, float],
                 x_inv : Callable[[float], float] = None,
                 y_inv : Callable[[float], float] = None):
        self._x_func = x_func
        self._y_func = y_func
        self._x_inv = x_inv
        self._y_inv = y_inv
        self._input_range = input_range

    def call(self, theta_rad: float) -> Tuple[float, float]:
        return (self._x_func(theta_rad), self._y_func(theta_rad))

    def init_lut(self):
            points_x, points_y, rads = self.plot(granularity=0.01)
            self._boundary_lut = [i for i in zip(points_x, points_y, rads)]

    def call_inv(self, x) -> float:
        for (x_lut, y_lut, rad_lut) in self._boundary_lut:
            #print(f'Entry: {(x_lut, y_lut, rad_lut)}')
            if np.abs(x_lut - x) < 0.01:
                return (x_lut, y_lut, rad_lut)

    def plot(self, granularity: float = 0.01) -> Tuple[List[float]]:
        points_x = []
        points_y = []
        rads     = []
        start = self._input_range[0]
        while start <= self._input_range[1]:
            rad = deg2rad(start)
            points_x.append(self._x_func(rad))
            points_y.append(self._y_func(rad))
            rads.append(rad)
            start += granularity
        return (points_x, points_y, rads)

class Boundary:
    _funcs : List[BoundaryFunction]

    def __init__(self, funcs: List[BoundaryFunction]):
        self._funcs = funcs
        for func in self._funcs:
            func.init_lut()

    def plot(self, i: int, granularity: float = 0.01) -> Tuple[List[float]]:
        assert i < len(self._funcs)
        return self._funcs[i].plot(granularity)

    def __len__(self):
        return len(self._funcs)

    def calc_wall_distance(self, boundary_idx_upper: int, boundary_idx_lower: int, x_val: float) -> float:
        assert (boundary_idx_upper != boundary_idx_lower) and (boundary_idx_upper in range(len(self))) and (boundary_idx_upper in range(len((self))))
        x_upper, y_upper, rad_upper = self._funcs[boundary_idx_upper].call_inv(x_val)
        x_lower, y_lower, rad_lower = self._funcs[boundary_idx_lower].call_inv(x_val)
        print(f'Boundary {boundary_idx_upper+1} theta: {np.rad2deg(rad_upper)} x: {x_upper} y: {y_upper}')
        print(f'Boundary {boundary_idx_lower+1} theta: {np.rad2deg(rad_lower)} x: {x_lower} y: {y_lower}')
        print('------------------------------------------------------')
        print(f'Boundary {boundary_idx_upper+1} x: {x_val} lut_x: {x_upper}' )
        print(f'Boundary {boundary_idx_lower+1} x: {x_val} lut_x: {x_lower}' )
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        return y_upper - y_lower
