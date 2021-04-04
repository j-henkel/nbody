import numpy as np


def fix(all_velocities: np.ndarray,
        all_masses: np.ndarray) -> np.ndarray:
    """define the velocity of the centre of mass as zero. Returns the
    adjusted velocity of all objects within the masssystem
    """

    all_pulses = all_velocities * all_masses[:, None]
    total_pulse = all_pulses.sum(axis=0)
    total_mass = all_masses.sum()
    velocity_centre_of_mass = total_pulse / total_mass

    all_v_new = all_velocities - velocity_centre_of_mass
    return all_v_new
