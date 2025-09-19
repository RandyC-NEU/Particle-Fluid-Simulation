from Simulation import Simulation, SimulationParameterFunc, PhysicsConstants, MathConstants
from Vec import Vec2
from Fluid import Fluid
from typing import Callable
from random import random

'''
    Simple representation of a particle submersed in a fluid
    Paramters are updated via Euler's method (eventually)

    Assumptions:
    Is a sphere of constant diameter
    Not rotating
    Interactions between particles can be ignored
    Initial velocity of particle
'''
class Particle(Simulation):
    _position : Vec2
    #TODO : Make this a function on the pipe area
    _velocity : Vec2
    _mass     : float
    _density  : float
    _diameter_nm : float
    _relaxation_time : float
    _fluid    : Fluid = None
    _get_reynolds : SimulationParameterFunc
    _get_drag_coeff : SimulationParameterFunc

    def __init__(self,
                 p: Vec2,
                 d_nm: float,
                 density: float,
                 relaxation_time: float,
                 get_reynolds: Callable[[Simulation, Simulation], float],
                 get_drag_coeff: Callable[[Simulation, Simulation], float]):
        self._position = p
        self._mass     = density * MathConstants.find_sphere_volume((d_nm*1e-6)/2)
        self._diameter_nm = d_nm
        self._density = density
        self._relaxation_time = relaxation_time
        self._get_reynolds = get_reynolds
        self._get_drag_coeff = get_drag_coeff

    '''
        "Submerse" the particle into a fluid
    '''
    def add_to_fluid(self, f: Fluid):
        self._fluid = f
        self._velocity = self._fluid.velocity() + Vec2(0.1, 0)

    def position(self) -> Vec2:
        return self._position

    def velocity(self) -> Vec2:
        return self._velocity

    def diameter_in_m(self) -> float:
        return self._diameter_nm / 1e6

    def update(self, dt: float):
        drag_force      : Vec2 = Vec2.zeros()
        delta_velocity  : Vec2 = Vec2.zeros()

        a = (18*self._fluid.dynamic_viscosity())/(self._density*(self.diameter_in_m()**2))
        b = (self._get_drag_coeff(self, self._fluid)*self._get_reynolds(self, self._fluid))/24
        drag_force = a*b

        drag_dependent_force : Vec2 = drag_force*(self._fluid.velocity() - self._velocity)
        grav_dependent_force : Vec2 = ((self._density - self._fluid.density())/self._density)*PhysicsConstants.GRAVITY_M_S__2

        dv_dt : Vec2 = drag_dependent_force + (grav_dependent_force if self._relaxation_time > 0.1 else Vec2(0, 0))

        delta_velocity += dv_dt*dt

        self._velocity += delta_velocity
        self._position += self._velocity*dt
        pass