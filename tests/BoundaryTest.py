import matplotlib.pyplot as plt
from FluidSimulation import ParticleInFluidSimulation
from Simulation import Boundary

boundary = ParticleInFluidSimulation.create_boundary()

def plot_boundary_funcs():
    markers = ['r+', 'b+', 'y+', 'y+']

    for i in range(4):
        points_x, points_y = boundary.plot(i, granularity=0.01)
        plt.plot(points_x, points_y, markers[i], markersize=3)

    plt.show()

def get_inlet_outlet_areas():
    inlet_area        = boundary.calc_wall_distance(0, 1, -9.0)
    print(" > inlet area: ",        inlet_area)
    outlet_area_upper = boundary.calc_wall_distance(0, 3, 8.0)
    print(" > upper outlet area: ", outlet_area_upper)
    outlet_area_lower = boundary.calc_wall_distance(2, 1, 8.0)
    print(" > lower outlet area: ", outlet_area_lower)