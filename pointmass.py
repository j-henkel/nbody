import numpy as np


class PointMass:
    """point mass"""

    def __init__(self, mass: float, position: np.ndarray, velocity: np.ndarray):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        return

    def dist(self, obj):
        """Calculates the distance to another object"""

        assert np.shape(self.position) == np.shape(obj.position), "positions must be of same dimension/shape"
        return np.sqrt(np.sum((self.position - obj.position) ** 2))
