from Vec import Vec2
from Simulation import Simulation

class Fluid(Simulation):
    _velocity : Vec2
    _density  : float

    def __init__(self, v: Vec2, d: float):
        self._velocity = v
        self._density = d

    def update(self, dt):
        pass