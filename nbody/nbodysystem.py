import numpy as np
from .pointmass import PointMass
from scipy.constants import gravitational_constant
import pandas as pd


class NBodySystem:
    """a gravitational system containing several bodies

    Attributes
    ----------
    bodyindex: dict
        a dictionary that stores the index of each body in the arrays
        all_positions, all_velocitys, all_masses, so it is easy to
        track which column belongs to which body.
    all_positions: np.ndarray
        an array that stores all position arrays in a single array:
            >> body1.position = np.array([1, 2, 3])
            >> body2.position = np.array([4, 5, 6])
            >> NBodySystem(body1, body2).all_positions
            out: np.array([[1, 2, 3], [4, 5, 6]])
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
    stationary()
        define the velocity of the centre of mass as zero and adjust
        all single velocities accordingly
    get_body(name)
        return the PointMass object named name
    """

    def __init__(self, *args, not_yet_initialized=True):
        """
        Parameters
        ----------
        not_yet_initialized: bool
            True if a new MassSysem is initialized from PointMass
            objects. False if all attributes are already in their
            final shape (this is for example used by step method, if
            inplace=False)
        args:
            if not_yet_initialized is True: PointMass
            if not_yet_initialized is False:
                (np.ndarray, np.ndarray, np.ndarray, dict)
        """
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
            # this constructor is used by some methods
            self.all_positions = args[0]
            self.all_velocities = args[1]
            self.all_masses = args[2]
            self.bodyindex = args[3]

    def step(self,
             dt,
             grav_const=gravitational_constant,
             inplace=True,
             halfstep=False):
        """calculate the next state of the gravitational system

        Parameters
        ----------
        dt: float
            The timestep on which the simulation operates
        grav_const: float, optional
            The gravitational constant. Default is the newtonian
            gravitational constant.
        inplace: bool, optional
            If inplace is True, the existing StaticSystem object
            gets modified
            If inplace is False, a new StaticSystem instance is
            returned
            Default is True.
        halfstep: bool, optional
            If halfstep is True, self.all_velocities will be updated
            with a step of dt/2. self.all_positions will still be
            updated wit the full step of dt. This can reduce error.
            Only use halfstep=True in the first step of a simulation! All
            following steps must be computed wiht halfstep=False.

        Returns
        -------
        NBodySystem, if inplace is False
            The state of the system after dt has elapsed
        """
        # calculate connection vector map
        shape = self.all_positions.shape
        gridshape = (shape[0], shape[0], shape[1])
        horizontal_grid = np.full(gridshape, self.all_positions)
        vertical_grid = horizontal_grid.transpose((1, 0, 2))
        convec_map = vertical_grid - horizontal_grid

        # calculate distance map (and reshape for further computation)
        dist_map = np.sqrt((convec_map ** 2).sum(axis=2))
        dist_map_rs = dist_map.reshape((shape[0], shape[0], 1))
        # replace 0s wit 1s to avoid division by zero (does not affect result)
        dist_map_rs[dist_map_rs == 0] = 1

        # calculate acceleration
        mlen = len(self.all_masses)
        mass_matrix = np.full((mlen, mlen), self.all_masses)
        mass_matrix = mass_matrix.reshape((mlen, mlen, 1))
        mx = convec_map * mass_matrix / (dist_map_rs ** 3)  # div by zero
        accelleration = - grav_const * mx.sum(axis=1)

        # update position and velocity
        if inplace:
            if halfstep:
                self.all_velocities = self.all_velocities + accelleration * dt/2
            else:
                self.all_velocities = self.all_velocities + accelleration * dt
            self.all_positions = self.all_positions + self.all_velocities * dt
        else:
            if halfstep:
                all_velocities = self.all_velocities + accelleration * dt/2
            else:
                all_velocities = self.all_velocities + accelleration * dt
            all_positions = self.all_positions + all_velocities * dt
            new_system = NBodySystem(all_positions, 
                                     all_velocities,
                                     self.all_masses,
                                     self.bodyindex,
                                     not_yet_initialized=False)
            return new_system

    def simulate(self,
                 end: pd.Timedelta, 
                 step: pd.Timedelta, 
                 start='0s',
                 grav_const=gravitational_constant,
                 halfstep=True):
        """simulate the evolution of the NBodySystem over time.
        Note: after using simulate() self will be in the final state of t=end.
        If you want to keep theinitial condition make a copy of the 
        NBodySystem before using simulate().

        Parameters
        ----------
        end: pd.Timedelta
            The time at which the simulation terminates
        step: pd.Timedelta
            The timestep of each iteration
        start: pd.Timedelta, optional
            The time at the beginning of the simulation.
            Default is '0s'
        grav_const: float, optional
            the gravitational constant. Default is the Newtonian gravitational
            constant
        halfstep: bool, optional
            if halfstep=True the first iteration of the simulation will use
        """

        index = pd.timedelta_range(start=start, end=end, freq=step)
        names = list(self.bodyindex.keys())
        dim = self.all_positions.shape[1]
        coordinates = []
        for i in range(dim):
            coordinates.append('x' + str(i+1))
        hierarchy = [names, coordinates]
        columns = pd.MultiIndex.from_product(hierarchy, names=['body', 'pos'])
        results = pd.DataFrame(np.zeros((len(index), len(names) * dim)),
                               index=index,
                               columns=columns)

        dt = pd.Timedelta(step).value * 1e-9

        #run simulation and copy positions into results
        flat = self.all_positions.flatten()
        results.iloc[0] = flat
        self.step(dt=dt, grav_const=grav_const, inplace=True, halfstep=halfstep)
        for i in range(len(index) - 1):
            flat = self.all_positions.flatten()
            results.iloc[i + 1] = flat
            self.step(dt=dt, grav_const=grav_const, inplace=True, halfstep=False)

        return results

    def centre_of_mass(self):
        """calculate the centre of mass

        Returns
        -------
        np.ndarray
            The centre of mass
        """
        total_mass = self.all_masses.sum()
        mx = (self.all_positions * self.all_masses[:, None]).sum(axis=0)
        centreofmass = mx / total_mass
        return centreofmass

    def stationary(self):
        """define the velocity of the centre of mass as zero and
        adjust self.all_velocities accordingly"""

        all_pulses = self.all_velocities * self.all_masses[:, None]
        total_pulse = all_pulses.sum(axis=0)
        total_mass = self.all_masses.sum()
        velocity_centre_of_mass = total_pulse / total_mass
        self.all_velocities = self.all_velocities - velocity_centre_of_mass

    def get_body(self, name: str):
        """return a PointMass object of the body named name

        Parameters
        ----------
        name: str
            the name of the object to return

        Returns
        -------
        PointMass
            the current state of the PointMass object
        """
        index = self.bodyindex[name]
        body = PointMass(name=name,
                         mass=self.all_masses[index],
                         position=self.all_positions[index],
                         velocity=self.all_velocities[index])
        return body
