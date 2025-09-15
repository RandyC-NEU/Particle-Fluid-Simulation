import matplotlib.pyplot as plt
from FluidSimulation import ParticleInFluidSimulation
from Simulation import Boundary

def plot_boundary_funcs():
    boundary = ParticleInFluidSimulation.create_boundary()
    markers = ['r+', 'b+', 'y+', 'y+']

    for i in range(4):
        points_x, points_y = boundary.plot(i, granularity=0.01)
        plt.plot(points_x, points_y, markers[i], markersize=3)

    plt.show()