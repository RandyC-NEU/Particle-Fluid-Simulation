from Vec import Vec2
from Simulation import Simulation, BoundaryFunction
from typing import List

class Fluid(Simulation):
    _velocity : Vec2
    _density  : float
    _boundary : List[BoundaryFunction]

    def __init__(self, v: Vec2, d: float, boundary_funcs: List[BoundaryFunction] = None):
        self._velocity = v
        self._density  = d
        self._boundary = boundary_funcs

    def update(self, dt):
        pass