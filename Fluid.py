from Vec import Vec2
from Simulation import Simulation, Boundary
from typing import List

class Fluid(Simulation):
    _velocity : Vec2
    _density  : float
    _boundary : Boundary #List[BoundaryFunction]

    def __init__(self, v: Vec2, d: float, boundary: Boundary = None):
        self._velocity = v
        self._density  = d
        self._boundary = boundary

    def update(self, dt):
        pass