from Simulation import Simulation, Boundary, BoundaryFunction
from Fluid import Fluid
from Particle import Particle
from Vec import Vec2

import matplotlib.pyplot as plt
from typing import List
from math import pi, tan
from time import time, sleep

'''
    Main simulation object that represents a particle submersed in a flowing fluid

    The particle will update its position and velocity over time based on the forces experienced while in the fluid

    Assumptions:
        - Particle is not rotating
        - Particle is a perfect sphere
        - Fluid has a constant temparature
'''
class ParticleInFluidSimulation(Simulation):
    _particle           : Particle          = None
    _fluid              : Fluid             = None
    _quit               : bool              = False
    _elapsed_time       : float             = 0
    _sec_per_tick       : int               = None
    _particle_positions : List[List[float]] = None
    _num_iterations     : float               = None

    def create_boundary() -> Boundary:
        cotan = lambda theta : 1.0/tan(theta)
        pi_2  = 2*pi
        input_range = (15.5568, 176.891)

        a_x = lambda theta: (5*(3.7699111843077517 - theta) * cotan(theta))/pi_2
        a_y = lambda theta: (5*(3.7699111843077517 - theta))/pi_2

        b_x = lambda theta: (5*(4.39822971502571 - theta) * cotan(theta))/pi_2
        b_y = lambda theta: -(5*(4.39822971502571 - theta))/pi_2

        c_x = lambda theta: (5*(pi - theta) * cotan(theta))/pi_2
        c_y = lambda theta: -(5*(pi - theta))/pi_2

        d_x = lambda theta: (5*(pi - theta) * cotan(theta))/pi_2
        d_y = lambda theta: (5*(pi - theta))/pi_2

        return Boundary([BoundaryFunction(a_x, a_y, input_range),
                         BoundaryFunction(b_x, b_y, input_range),
                         BoundaryFunction(c_x, c_y, input_range),
                         BoundaryFunction(d_x, d_y, input_range)])

    def __init__(self, fluid_velocity: Vec2, fluid_density: float):
        self._fluid = Fluid(fluid_velocity, fluid_density, ParticleInFluidSimulation.create_boundary())
        self._elapsed_time = time()
        self._particle_positions = [[], []]

    '''
        Add a particle to the simulation
    '''
    def add_particle(self, position: Vec2, velocity: Vec2, mass: float):
        if self._particle is None:
            self._particle = Particle(position, velocity, mass)
            self._particle.add_to_fluid(self._fluid)
        else:
            assert "A particle has already been added to this simulation, this is not a multi-particle simuation (yet :))"

    '''
        Set a "tick rate" for the simulation. This is analogous to a frame rate for a graphics render where an update to the
        simulation happens every tick. Good for debugging
    '''
    def throttle_simulation(self, ticks_per_sec):
        self._sec_per_tick = 1.0/ticks_per_sec

    def limit_iterations(self, iters: int):
        self._num_iterations = iters

    def update_particle_trajectory(self):
        pos = self._particle.position()
        self._particle_positions[0].append(pos[0])
        self._particle_positions[1].append(pos[1])

    def update(self, dt):
        self._particle.update(dt)
        self._fluid.update(dt)

        self.update_particle_trajectory()
        self._elapsed_time += dt

    '''
        Get next time step; Note this is a raw time step.
        dt is always relative to the elapsed time of the simulation
    '''
    def get_time(self):
        if self._sec_per_tick is None:
            return time()
        else:
            elapsed = time() - self._elapsed_time
            sleep_time = elapsed - self._sec_per_tick
            if sleep_time > 0.0:
                sleep(sleep_time)
            return self._sec_per_tick + self._elapsed_time

    '''
        Start simulation loop
    '''
    def start(self):
        print("Sim start")
        assert all((x is not None) for x in [self._particle, self._fluid])

        dt = self.get_time() - self._elapsed_time
        while (not self._quit) and (self._num_iterations > 0 if (self._num_iterations is not None) else True):
            self.update(dt)
            dt = self.get_time() - self._elapsed_time
            if self._num_iterations is not None:
                self._num_iterations-=1

    def plot_boundary(self):
        markers = ['r+', 'b+', 'y+', 'y+']
        for i in range(len(self._fluid.boundary_functions())):
            points_x, points_y = self._fluid.boundary_functions().plot(i, granularity=0.01)
            plt.plot(points_x, points_y, markers[i], markersize=3)

    def plot_particle_trajectory(self):
        plt.plot(self._particle_positions[0], self._particle_positions[1], 'go', markersize=1)

    def plot(self):
        self.plot_boundary()
        self.plot_particle_trajectory()

        plt.show()