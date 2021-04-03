import numpy as np
from pointmass import PointMass


class MassSystem:
    """a gravitational system of several objects"""

    def __init__(self, not_yet_initialized=True, *args):
        # TODO: complete construcor
        if not_yet_initialized:
            pass
        else:
            pass

        pass

    def step(self, inplace=True):
        """calculate the next state of the gravitational system"""

        pass

    def centre_of_mass(self):
        """calculate the centre of mass"""

        pass

    def fix(self):
        """define the velocity of the centre of mass as zero"""

        pass

    def get_object(self, name: str):
        """return a PointMass object of the body named name"""

        pass
