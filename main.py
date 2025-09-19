from FluidSimulation import ParticleInFluidSimulation
from Simulation import PhysicsConstants, MathConstants
from tests.BoundaryTest import plot_boundary_funcs, get_inlet_outlet_areas
from tests.TestReynoldsNumber import run_reynolds_test, run_drag_coeff_test
from Vec import Vec2
from sys import argv

def main():
    if ((len(argv) > 1)):
        if argv[1] == 'test_boundary':
            plot_boundary_funcs()
        if argv[1] == 'get_wall_areas':
            get_inlet_outlet_areas()
        if argv[1] == 'test_reynolds_number':
            run_reynolds_test()
        if argv[1] == 'test_drag_coeff':
            run_drag_coeff_test()
    else:
        particle_sizes_nm = [1, 5, 10, 50, 100]
        relaxation_times  = [8.65*1e-5, 2.16*1e-3, 8.65*1e-3, 0.216, 0.865]
        positions = [Vec2(-8.0, 0.0), Vec2(-10.0, 0.1), Vec2(-10.0, 0.4), Vec2(-10.0, -0.4)]
        sim = ParticleInFluidSimulation(fluid_velocity=Vec2(1.0, 0.0), fluid_density=PhysicsConstants.DENSITY_AIR_25C__1_ATM)

        sim.set_particle_count(4)
        #sim.add_particle(position=positions[0], diameter=particle_sizes_nm[0], density=PhysicsConstants.DENSITY_SAND__KG_M__3, relaxation_time=relaxation_times[0])
        #sim.add_particle(position=positions[1],  diameter=particle_sizes_nm[1], density=PhysicsConstants.DENSITY_SAND__KG_M__3, relaxation_time=relaxation_times[0])
        sim.add_particle(position=positions[0],
                         diameter_nm=particle_sizes_nm[2],
                         density=PhysicsConstants.DENSITY_SAND__KG_M__3,
                         relaxation_time=relaxation_times[4])
        #sim.add_particle(position=positions[3], diameter=particle_sizes_nm[3], density=PhysicsConstants.DENSITY_SAND__KG_M__3, relaxation_time=relaxation_times[0])

        sim.throttle_simulation(10000)
        sim.limit_iterations(100000)

        sim.start()
        sim.plot()

if __name__ == '__main__':
    main()