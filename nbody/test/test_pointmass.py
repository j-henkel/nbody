from ..pointmass import PointMass
import pytest
import numpy as np


class TestPointMass():

    def test_init(self):
        with pytest.raises(AssertionError):
            body = PointMass('a', 1.0, np.array([1, 2]), np.array([1, 2, 3]))

    def test_init_wrong_shape(self):
        twodim_array = np.array([[1, 2], [3, 4]])
        with pytest.raises(AssertionError):
            body = PointMass('a', 1.0, twodim_array, np.array([1, 2]))

    def test_dist(self):
        body1 = PointMass('b1', 1.0, np.array([0, 0]), np.array([0, 0]))
        body2 = PointMass('b2', 1.0, np.array([1, 1]), np.array([0, 0]))
        assert body1.dist(body2) == np.sqrt(2)

    def test_dist_different_shape(self):
        body1 = PointMass('b1', 1.0, np.array([0, 0]), np.array([0, 0]))
        body2 = PointMass('b2', 1.0, np.array([1, 1, 1]), np.array([0, 0, 0]))
        with pytest.raises(AssertionError):
            assert body1.dist(body2) == np.sqrt(2)
