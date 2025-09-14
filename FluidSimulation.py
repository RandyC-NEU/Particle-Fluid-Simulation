from Simulation import Simulation
from Particle import Particle
from Fluid import Fluid
from Vec import Vec2
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
    _particle      : Particle = None
    _fluid         : Fluid    = None
    _quit          : bool     = False
    _elapsed_time  : float    = 0
    _sec_per_tick  : int      = None

    def __init__(self, fluid_v: Vec2, fluid_d: float):
        self._fluid = Fluid(fluid_v, fluid_d)
        self._elapsed_time = time()

    '''
        Add a particle to the simulation
    '''
    def add_particle(self, particle_p: Vec2, particle_v: Vec2, particle_m: float):
        if self._particle is None:
            self._particle = Particle(particle_p, particle_v, particle_m)
            self._particle.add_to_fluid(self._fluid)
        else:
            assert "A particle has already been added to this simulation, this is not a multi-particle simuation (yet :))"

    '''
        Set a "tick rate" for the simulation. This is analogous to a frame rate for a graphics render where an update to the
        simulation happens every tick. Good for debugging
    '''
    def throttle_simulation(self, ticks_per_sec):
        self._sec_per_tick = 1.0/ticks_per_sec

    def update(self, dt):
        self._particle.update(dt)
        self._fluid.update(dt)
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
        while (not self._quit):
            self.update(dt)
            dt = self.get_time() - self._elapsed_time