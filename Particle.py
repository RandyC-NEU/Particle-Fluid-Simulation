from Simulation import Simulation, SimulationParameterFunc, PhysicsConstants, MathConstants
from Vec import Vec2
from Fluid import Fluid
from typing import Callable, Tuple
from random import random

'''
    Simple representation of a particle submersed in a fluid
    Paramters are updated via Euler's method (eventually)

    Assumptions:
    Is a sphere of constant diameter
    Not rotating
    Interactions between particles can be ignored
    Initial velocity of particle is about a 5% difference to the fluid
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

    def collided(self) -> bool:
        return self._collided

    def reflect_off_boundary(self, boundary_idx: int, collision_theta: Tuple, dt: float):
        normal: Vec2 = self._fluid.boundary_functions()[boundary_idx].get_normal_at_point(collision_theta)

        velocity_normal = normal * Vec2.dot(self._velocity, normal)
        velocity_tan = self._velocity - velocity_normal

        coeff_restution_norm, coeff_resitution_tan = self._fluid.boundary_functions().get_coeffs_of_restitution()

        velocity_normal *= -1*coeff_restution_norm
        velocity_tan *= coeff_resitution_tan
        self._velocity = (velocity_normal + velocity_tan)
        self._position += self._velocity*dt

        self._collided = True
        pass

    def detect_collision(self, dt: float):
        for i, f in enumerate(self._fluid.boundary_functions()):
            collision = f.call_inv(self._position[0], self._position[1])
            if collision is not None:
                print("Boundary", i, ":: ")
                print(collision)
                self.reflect_off_boundary(i, collision[2], dt)

    def update(self, dt: float):
        self._collided         = False
        drag_force      : Vec2 = Vec2.zeros()
        delta_velocity  : Vec2 = Vec2.zeros()

        self.detect_collision(dt)

        a = (18*self._fluid.dynamic_viscosity())/(self._density*(self.diameter_in_m()**2))
        b = (self._get_drag_coeff(self, self._fluid)*self._get_reynolds(self, self._fluid))/24
        drag_force = a*b

        drag_dependent_force : Vec2 = drag_force*(self._fluid.velocity() - self._velocity)
        grav_dependent_force : Vec2 = ((self._density - self._fluid.density())/self._density)*PhysicsConstants.GRAVITY_M_S__2

        dv_dt : Vec2 = drag_dependent_force #+ (grav_dependent_force if self._relaxation_time > 0.8 else Vec2(0, 0))

        delta_velocity += dv_dt*dt

        self._velocity += delta_velocity
        self._position += self._velocity*dt
