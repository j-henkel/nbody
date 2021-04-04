import numpy as np


class PointMass:
    """point mass

    Attributes
    ----------
    mass: float
        the mass of the object in kg
    position: np.ndarray
        the position of the object in m
    velocity: np.ndarray
        the velocity of the object in m/s

    Methods
    -------
    dist(obj)
        calculates the distance to another object
    """

    def __init__(self,
                 name: str,
                 mass: float,
                 position: np.ndarray,
                 velocity: np.ndarray):
        """
        Parameters
        ----------
        name: str
            the name of the object
        mass: float
            the mass of the object in kg
        position: np.ndarray
            the position of the object in m
        velocity: np.ndarray
            the velocity of the object in m/s
        """

        assert np.shape(self.position) == np.shape(self.velocity), \
            "position and velocity must be of same shape"
        self.name = name
        self.mass = mass
        self.position = position
        self.velocity = velocity
        return

    def dist(self, obj):
        """Calculates the distance to another object

        Parameters
        ----------
        obj: PointMass
            the object the distance to is calculated

        Raises
        ------
        AssertionError
            if the shapes of self.position and obj.position don't match
        """

        assert np.shape(self.position) == np.shape(obj.position), \
            "positions must be of same dimension/shape"
        return np.sqrt(np.sum((self.position - obj.position) ** 2))
