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
    _x_deriv      : Callable[[float], float]
    _y_deriv      : Callable[[float], float]

    _boundary_lut : BoundaryLutEntry = None
    _input_range  : Tuple[float, float]

    def __init__(self,
                 x_func: Callable[[float], float],
                 y_func: Callable[[float], float],
                 d_x : Callable[[float], float],
                 d_y : Callable[[float], float],
                 input_range: Tuple[float, float]):
        self._x_func = x_func
        self._y_func = y_func
        self._x_deriv = d_x
        self._y_deriv = d_y
        self._input_range = input_range

    '''
        Evaluate the boundary function at a given theta
    '''
    def call(self, theta_rad: float) -> Tuple[float, float]:
        assert (theta_rad >= np.deg2rad(self._input_range[0])) and (theta_rad <= np.deg2rad(self._input_range[1]))
        return (self._x_func(theta_rad), self._y_func(theta_rad))

    '''
        Get the normalized tangent vector to the point on the boundary function at a given theta
    '''
    def get_tangent_at_point(self, theta_rad: float):
        assert (theta_rad >= np.deg2rad(self._input_range[0])) and (theta_rad <= np.deg2rad(self._input_range[1]))
        deriv: Vec2 = Vec2(self._x_deriv(theta_rad), self._y_deriv(theta_rad))
        return deriv.normalize()

    '''
        Get the normal vector to the point on the boundary function at a given theta
    '''
    def get_normal_at_point(self, theta_rad: float):
        tangent: Vec2 = self.get_tangent_at_point(theta_rad)
        return Vec2(tangent[1], -tangent[0])

    '''
        Initialize the lookup table for calculating the inverse values of the boundary function
        Meaning, for a given x or y, we can look up the closest value to that given x or y in the lookup table
    '''
    def init_lut(self):
            points_x, points_y, rads = self.plot(granularity=0.01)
            self._boundary_lut = [i for i in zip(points_x, points_y, rads)]

    '''
        Do a linear search on the lookup table for the boundary function to
        find the closest entry to a given x in the LUT
    '''
    def call_inv_x(self, x: float) -> float:
        for (x_lut, y_lut, rad_lut) in self._boundary_lut:
            if np.abs(x_lut - x) < 0.01:
                return (x_lut, y_lut, rad_lut)
        return None
    '''
        Do a linear search on the lookup table for the boundary function to
        find the closest entry to a given y in the LUT
    '''
    def call_inv_y(self, y: float) -> float:
        for (x_lut, y_lut, rad_lut) in self._boundary_lut:
            if np.abs(y_lut - y) < 0.01:
                return (x_lut, y_lut, rad_lut)
        return None

    '''
        Do a linear search on the lookup table for the boundary function to
        find the closest entry to a given x and y in the LUT
    '''
    def call_inv(self, x: float, y: float) -> Tuple[float, float, float]:
        for (x_lut, y_lut, rad_lut) in self._boundary_lut:
            if (np.abs(y_lut - y) < 0.01) and (np.abs(x_lut - x) < 0.01):
                return (x_lut, y_lut, rad_lut)
        return None

    '''
        Evaluate the boundary function along the input range with a specified granularity
        Records the evaluated x and y values, and the radian value

        Good for plotting and recording values for a lookup table
    '''
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

    '''
        Plot all of the bounrdary functions that make up the boundary
    '''
    def plot(self, i: int, granularity: float = 0.01) -> Tuple[List[float]]:
        assert i < len(self._funcs)
        return self._funcs[i].plot(granularity)
    '''
        Python iterator functions
    '''
    def __len__(self):
        return len(self._funcs)

    def __iter__(self):
        return self._funcs.__iter__()

    def __next__(self):
        return self._funcs.__next__()

    def __getitem__(self, key: int) -> BoundaryFunction:
        assert (key >= 0) and (key < len(self))
        return self._funcs[key]

    def get_coeffs_of_restitution(self) -> Tuple[float, float]:
        return (0.95, 0.78)

    def calc_wall_distance(self, boundary_idx_upper: int, boundary_idx_lower: int, x_val: float) -> float:
        assert (boundary_idx_upper != boundary_idx_lower) and (boundary_idx_upper in range(len(self))) and (boundary_idx_upper in range(len((self))))
        x_upper, y_upper, rad_upper = self._funcs[boundary_idx_upper].call_inv_x(x_val)
        x_lower, y_lower, rad_lower = self._funcs[boundary_idx_lower].call_inv_x(x_val)
        print(f'Boundary {boundary_idx_upper+1} theta: {np.rad2deg(rad_upper)} x: {x_upper} y: {y_upper}')
        print(f'Boundary {boundary_idx_lower+1} theta: {np.rad2deg(rad_lower)} x: {x_lower} y: {y_lower}')
        print('------------------------------------------------------')
        print(f'Boundary {boundary_idx_upper+1} x: {x_val} lut_x: {x_upper}' )
        print(f'Boundary {boundary_idx_lower+1} x: {x_val} lut_x: {x_lower}' )
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        return y_upper - y_lower
