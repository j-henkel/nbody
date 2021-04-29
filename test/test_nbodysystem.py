from ..nbodysystem import NBodySystem
from ..pointmass import PointMass
import numpy as np
import pytest


class TestNBodySystem():

    def test_init_not_yet_initialized(self):
        body1 = PointMass('b1', 1.0, np.array([1, 2]), np.array([3, 4]))
        body2 = PointMass('b2', 2.0, np.array([5, 6]), np.array([7, 8]))
        system = NBodySystem(body1, body2)
        pos_compare = system.all_positions == np.array([[1, 2], [5, 6]])
        assert pos_compare.all()
        vel_compare = system.all_velocities == np.array([[3, 4], [7, 8]])
        assert vel_compare.all()
        mass_compare = system.all_masses == np.array([1, 2])
        assert mass_compare.all()
        assert system.bodyindex == {'b1': 0, 'b2': 1}

    def test_init_not_yet_initialized_name_repeat(self):
        body1 = PointMass('b1', 1.0, np.array([1, 2]), np.array([3, 4]))
        body2 = PointMass('b1', 2.0, np.array([5, 6]), np.array([7, 8]))
        with pytest.raises(AttributeError):
            system = NBodySystem(body1, body2)

    def test_init_not_yet_initialized_single_body(self):
        body1 = PointMass('b1', 1.0, np.array([1, 2]), np.array([3, 4]))
        system = NBodySystem(body1)
        pos_compare = system.all_positions == np.array([1, 2])
        assert pos_compare.all()
        vel_compare = system.all_velocities == np.array([3, 4])
        assert vel_compare.all()
        mass_compare = system.all_masses == np.array([1])
        assert mass_compare.all()
        assert system.bodyindex == {'b1': 0}
