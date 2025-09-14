from abc import ABC, abstractmethod

'''
    Interface for any object that needs its parameters updated at every time step
'''
class Simulation(ABC):
    @abstractmethod
    def update(self, dt):
        pass