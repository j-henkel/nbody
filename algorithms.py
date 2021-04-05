import numpy as np


def fix(all_velocities: np.ndarray,
        all_masses: np.ndarray) -> np.ndarray:
    """Define the velocity of the centre of mass as zero. Returns the
    adjusted velocity of all objects within the masssystem.

    Parameters
    ----------
    all_velocities: np.ndarray
        An array that combines the velocity vectors of several bodys,
        typically a MassSystem.all_velocitys array
    all_masses: np.ndarray
        An array that combines the corresponding masses, typically
        a MassSystem.all_masses array

    Returns
    -------
    all_v_new: np.ndarray
        The adjusted all_velocities array
    """

    all_pulses = all_velocities * all_masses[:, None]
    total_pulse = all_pulses.sum(axis=0)
    total_mass = all_masses.sum()
    velocity_centre_of_mass = total_pulse / total_mass

    all_v_new = all_velocities - velocity_centre_of_mass
    return all_v_new


def centre_of_mass(all_positions: np.ndarray,
                   all_masses: np.ndarray) -> np.ndarray:
    """calculate the centre of mass"""
    pass
