from FluidSimulation import ParticleInFluidSimulation
from tests.BoundaryTest import plot_boundary_funcs
from Vec import Vec2
from sys import argv

def main():
    if ((len(argv) > 1)):
        if argv[1] == 'test_boundary':
            plot_boundary_funcs()
    else:
        sim = ParticleInFluidSimulation(1.0, 1.0)
        sim.add_particle(Vec2(0.0, 0.0), Vec2(1.0, 1.0), 1.0)
        #sim.throttle_simulation(60)
        #sim.start()

if __name__ == '__main__':
    main()