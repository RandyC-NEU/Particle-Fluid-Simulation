from Vec import Vec2
import numpy as np
from Simulation import PhysicsConstants

density = PhysicsConstants.DENSITY_AIR_25C__1_ATM
dyn_visc = PhysicsConstants.DYNAMIC_VISCOSITY_AIR_25C__1_ATM
fluid_v = Vec2(1.0, 0.0)
particle_sizes = [1e-6, 5*1e-6, 10*1e-6, 50*1e-6, 100*1e-6]
particle_v = Vec2(2.0, 0)

def test_reynolds_number(f_density, p_diameter, p_vel, f_vel, f_dyn_visc):
    vel_delta : Vec2 = (p_vel - f_vel)
    reynolds = (f_density*p_diameter*vel_delta.magnitude()) / f_dyn_visc
    return reynolds

def run_reynolds_test():
    for p_size in particle_sizes:
        reynolds = test_reynolds_number(density, p_size, particle_v, fluid_v, dyn_visc)
        print(f'Particle size: {p_size} -> Reynolds Number: {reynolds}')

def run_drag_coeff_test():
    particle_sizes = [1e-6, 5*1e-6, 10*1e-6, 50*1e-6, 100*1e-6]

    for p_size in particle_sizes:
        reynolds = test_reynolds_number(density, p_size, particle_v, fluid_v, dyn_visc)
        a = 24/reynolds
        b = 1+(0.15*(reynolds**0.687))
        coeff = a*b
        print(f'a: {p_size} -> b: {coeff}')
        print(f'Particle size: {p_size} -> Coefficient of drag: {coeff}')
