import numpy as np


class Body:
    def __init__(self, mass: float, position: np.ndarray, velocity: np.ndarray):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        return
