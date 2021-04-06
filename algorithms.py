import numpy as np


def fix(all_velocities: np.ndarray,
        all_masses: np.ndarray) -> np.ndarray:
    """Define the velocity of the centre of mass as zero. Returns the
    adjusted all_velocities array.

    Parameters
    ----------
    all_velocities: np.ndarray
        An array that combines the velocity vectors of several
        bodys, typically a MassSystem.all_velocitys array
    all_masses: np.ndarray
        An array that combines the corresponding masses,
        typically a MassSystem.all_masses array

    Returns
    -------
    np.ndarray
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
    """calculate the centre of mass

    Parameters
    ----------
    all_positions: np.ndarray
        An array that combines several position arrays,
        typically MassSysem.all_positions
    all_masses: np.ndarray
        An array that combines the corresponding masses,
        typically MassSystem.all_masses

    Returns
    -------
    np.ndarray
        The centre of mass
    """

    total_mass = all_masses.sum()
    centreofmass = 1 / total_mass * (all_positions * all_masses[:, None]).sum()
    return centreofmass
