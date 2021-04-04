import numpy as np
from pointmass import PointMass


class MassSystem:
    """a gravitational system of several objects"""

    def __init__(self, not_yet_initialized=True, *args: PointMass):
        # TODO: make sure every args.name is unique
        if not_yet_initialized:
            bodyindex = {}
            for i, body in enumerate(args):
                bodyindex[body.name] = i

            shape = (len(args), len(args[0].position))

            all_positions = np.zeros(shape)
            for i, body in enumerate(args):
                all_positions[i] = body.position

            all_velocitys = np.zeros(shape)
            for i, body in enumerate(args):
                all_velocitys[i] = body.velocity

            all_masses = np.zeros(len(args))
            for i, body in enumerate(args):
                all_masses[i] = body.mass

        else:
            all_positions = args[0]
            all_velocitys = args[1]
            all_masses = args[2]
            bodyindex = args[3]

    def step(self, inplace=True):
        """calculate the next state of the gravitational system"""
        # TODO write step algorithm

        pass

    def centre_of_mass(self):
        """calculate the centre of mass"""
        # TODO centre_of_mass algorithm

        pass

    def fix(self):
        """define the velocity of the centre of mass as zero"""
        # TODO fix() algorithm
        pass

    def get_object(self, name: str):
        """return a PointMass object of the body named name"""
        # TODO get_object method

        pass
