from FluidSimulation import ParticleInFluidSimulation
from Vec import Vec2

def main():
    sim = ParticleInFluidSimulation(1.0, 1.0)
    sim.add_particle(Vec2(0.0, 0.0), Vec2(1.0, 1.0), 1.0)
    #sim.throttle_simulation(60)
    sim.start()

if __name__ == '__main__':
    main()