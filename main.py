from FluidSimulation import ParticleInFluidSimulation
from Simulation import PhysicsConstants
from tests.BoundaryTest import plot_boundary_funcs, get_inlet_outlet_areas
from tests.TestReynoldsNumber import run_reynolds_test, run_drag_coeff_test
from Vec import Vec2
from sys import argv
import numpy as np

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
        sim = ParticleInFluidSimulation(fluid_velocity=Vec2(1.0, 0.0), fluid_density=PhysicsConstants.DENSITY_AIR_25C__1_ATM)

        particle_sizes_nm = [1, 5, 10, 50, 100]
        relaxation_times  = [8.65*1e-5, 2.16*1e-3, 8.65*1e-3, 0.216, 0.865]
        probabilities = [0.1, 0.3, 0.25, 0.2, 0.15]
        positions = [Vec2(-10.0, 0.25), Vec2(-10.0, -0.5)]

        particle_data = []
        position_prob = [1/(len(positions))] * (len(positions))
        idxs = list(range(len(probabilities)))

        particle_data.append((np.random.choice(idxs, p=probabilities), np.random.choice(positions, p=position_prob)))
        particle_data.append((np.random.choice(idxs, p=probabilities), np.random.choice(positions, p=position_prob)))
        particle_data.append((np.random.choice(idxs, p=probabilities), np.random.choice(positions, p=position_prob)))
        particle_data.append((np.random.choice(idxs, p=probabilities), np.random.choice(positions, p=position_prob)))

        sim.set_particle_count(4)
        #sim.add_particle(position=particle_data[0][1], diameter_nm=particle_sizes_nm[particle_data[0][0]], density=PhysicsConstants.DENSITY_SAND__KG_M__3, relaxation_time=relaxation_times[particle_data[0][0]])
        #sim.add_particle(position=particle_data[1][1], diameter_nm=particle_sizes_nm[particle_data[1][0]], density=PhysicsConstants.DENSITY_SAND__KG_M__3, relaxation_time=relaxation_times[particle_data[1][0]])
        #sim.add_particle(position=particle_data[2][1], diameter_nm=particle_sizes_nm[particle_data[2][0]], density=PhysicsConstants.DENSITY_SAND__KG_M__3, relaxation_time=relaxation_times[particle_data[2][0]])
        sim.add_particle(position=particle_data[3][1], diameter_nm=particle_sizes_nm[particle_data[3][0]], density=PhysicsConstants.DENSITY_SAND__KG_M__3, relaxation_time=relaxation_times[particle_data[3][0]])

        sim.throttle_simulation(1000)
        sim.limit_iterations(10000)

        sim.start()
        sim.plot()

if __name__ == '__main__':
    main()