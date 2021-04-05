import numpy as np
import algorithms
# noinspection PyUnresolvedReferences
from pointmass import PointMass


class MassSystem:
    """a gravitational system of several bodies

    Attributes
    ----------
    bodyindex: dict
        a dictionary that stores the index of each body in the arrays
        all_positions, all_velocitys, all_masses, so it is easy to track
        which column belongs to which body.
    all_positions: np.ndarray
        an array that stores all position arrays in a single array. E.g:
            body1.position = np.array([1, 2, 3])
            body2.position = np.array([4, 5, 6])
            MassSystem(body1, body2).all_positions == \
                np.array([[1, 2, 3], [4, 5, 6]])
    all_velocitys: np.ndarray
        an array that stores all velocity arrays in a single array
    all_masses: np.ndarray
        an array that stores all masses

    Methods
    -------
    step(inplace)
        run the simulation one timestep
    centre_of_mass()
        calculate the centre of mass of the mass-system
    fix()
        define the velocity of the centre of mass as zero and adjust
        all single velocities accordingly
    get_object(name)
        return the PointMass object named name
    """

    def __init__(self, not_yet_initialized=True, *args):
        if not_yet_initialized:
            self.bodyindex = {}
            for i, body in enumerate(args):
                if body.name in self.bodyindex:
                    raise AttributeError("there are several objects called "
                                         + body.name)
                else:
                    self.bodyindex[body.name] = i

            shape = (len(args), len(args[0].position))

            self.all_positions = np.zeros(shape)
            for i, body in enumerate(args):
                self.all_positions[i] = body.position

            self.all_velocities = np.zeros(shape)
            for i, body in enumerate(args):
                self.all_velocities[i] = body.velocity

            self.all_masses = np.zeros(len(args))
            for i, body in enumerate(args):
                self.all_masses[i] = body.mass

        else:
            self.all_positions = args[0]
            self.all_velocities = args[1]
            self.all_masses = args[2]
            self.bodyindex = args[3]

    def step(self, inplace=True):
        """calculate the next state of the gravitational system"""
        # TODO write step algorithm

        pass

    def centre_of_mass(self):
        """calculate the centre of mass"""
        # TODO centre_of_mass algorithm

        pass

    def fix(self):
        """define the velocity of the centre of mass as zero and
        adjust self.all_velocities accordingly"""
        self.all_velocities = algorithms.fix(self.all_velocities,
                                             self.all_masses)

    def get_object(self, name: str):
        """return a PointMass object of the body named name"""
        # TODO get_object method

        pass
