from Simulation import Simulation
from Vec import Vec2
from Fluid import Fluid

'''
    Simple representation of a particle submersed in a fluid
    Paramters are updated via Euler's method (eventually)
'''
class Particle(Simulation):
    _position : Vec2
    _velocity : Vec2
    _mass     : float
    _fluid    : Fluid = None

    def __init__(self, p: Vec2, v: Vec2, m: float):
        self._position = p
        self._velocity = v
        self._mass     = m

    '''
        "Submerse" the particle into a fluid
    '''
    def add_to_fluid(self, f: Fluid):
        self._fluid = f

    def position(self) -> Vec2:
        return self._position

    def update(self, dt: float):
        displacement : Vec2 = Vec2.zeros()
        resultant_accel : Vec2 = Vec2.zeros()

        displacement += (self._velocity*dt)
        displacement += (self._fluid.velocity()*dt)
        displacement += (self._mass*resultant_accel)

        self._position += displacement
        pass