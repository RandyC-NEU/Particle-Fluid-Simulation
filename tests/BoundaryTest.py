import matplotlib.pyplot as plt
from math import pi, tan
from FluidSimulation import ParticleInFluidSimulation

def plot_boundary_funcs():
    boundary_funcs = ParticleInFluidSimulation.create_boundary_funcs()
    markers = ['r+', 'b+', 'y+', 'y+']

    for i in range(4):
        points_x, points_y = boundary_funcs[i].plot(granularity=0.01)
        plt.plot(points_x, points_y, markers[i], markersize=3)

    plt.show()