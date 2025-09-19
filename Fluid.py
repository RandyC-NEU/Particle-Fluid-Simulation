from Vec import Vec2
from Simulation import Simulation, Boundary
'''
    Assumptions:
    Constant velocity throughout pipe
    Constant density  throughout pipe
    Constant temperature throughout pipe

'''
#Air @25C and 1 atm
class Fluid(Simulation):
    _velocity : Vec2
    _density  : float
    _boundary : Boundary
    _dynamic_viscosity : float = 1.849*1e-5

    def __init__(self, v: Vec2, d: float, boundary: Boundary = None):
        self._velocity = v
        self._density  = d
        self._boundary = boundary

    def velocity(self) -> Vec2:
        return self._velocity

    def density(self) -> float:
        return self._density

    def dynamic_viscosity(self) -> float:
        return self._dynamic_viscosity

    def boundary_functions(self) -> Boundary:
        return self._boundary

    def update(self, dt):
        pass