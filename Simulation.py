from abc import ABC, abstractmethod

'''
    Interface for any object that needs its paramteres updated oat every time step
'''
class Simulation(ABC):
    @abstractmethod
    def update(self, dt):
        pass