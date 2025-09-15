from Vec import Vec2
from Simulation import Simulation, Boundary

class Fluid(Simulation):
    _velocity : Vec2
    _density  : float
    _boundary : Boundary

    def __init__(self, v: Vec2, d: float, boundary: Boundary = None):
        self._velocity = v
        self._density  = d
        self._boundary = boundary

    def velocity(self) -> Vec2:
        return self._velocity

    def boundary_functions(self) -> Boundary:
        return self._boundary

    def update(self, dt):
        pass