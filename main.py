from FluidSimulation import ParticleInFluidSimulation
from tests.BoundaryTest import plot_boundary_funcs, get_inlet_outlet_areas
from Vec import Vec2
from sys import argv

def main():
    if ((len(argv) > 1)):
        if argv[1] == 'test_boundary':
            plot_boundary_funcs()
        if argv[1] == 'get_wall_areas':
            get_inlet_outlet_areas()
    else:
        sim = ParticleInFluidSimulation(fluid_velocity=Vec2(1.0, 0.0), fluid_density=1.0)
        sim.set_particle_count(4)
        sim.add_particle(position=Vec2(-10.0, -0.1), mass=1.0)
        sim.add_particle(position=Vec2(-10.0, 0.1), mass=1.0)
        sim.add_particle(position=Vec2(-10.0, 0.4), mass=1.0)
        sim.add_particle(position=Vec2(-10.0, -0.4), mass=1.0)
        sim.throttle_simulation(60)
        sim.limit_iterations(100)
        sim.start()
        sim.plot()

if __name__ == '__main__':
    main()