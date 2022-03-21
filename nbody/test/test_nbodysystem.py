from ..nbodysystem import NBodySystem
from ..pointmass import PointMass
import numpy as np
import pytest
import pandas as pd


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

    def test_step_inplace(self):
        body1 = PointMass('b1', 1, np.array([1, 0, 0]), np.array([0, 1, 1]))
        body2 = PointMass('b2', 2, np.array([0, 0, 0]), np.array([0, 1, 1]))
        body3 = PointMass('b3', 1, np.array([-1, 0, 0]), np.array([0, 1, 1]))
        system = NBodySystem(body1, body2, body3)
        system.step(dt=0.1, grav_const=1, halfstep=False)
        pos_compare1 = system.get_body('b1').position 
        pos_compare1 = pos_compare1 == np.array([0.9775, 0.1, 0.1])
        assert pos_compare1.all()
        pos_compare2 = system.get_body('b2').position 
        pos_compare2 = pos_compare2 == np.array([0, 0.1, 0.1])
        assert pos_compare2.all()
        pos_compare3 = system.get_body('b3').position 
        pos_compare3 = pos_compare3 == np.array([-0.9775, 0.1, 0.1])
        assert pos_compare3.all()
        vel_compare1 = system.get_body('b1').velocity
        vel_compare1 = vel_compare1 == np.array([-0.225, 1, 1])
        assert vel_compare1.all()
        vel_compare2 = system.get_body('b2').velocity
        vel_compare2 = vel_compare2 == np.array([0, 1, 1])
        assert vel_compare1.all()
        vel_compare3 = system.get_body('b3').velocity
        vel_compare3 = vel_compare3 == np.array([0.225, 1, 1])
        assert vel_compare1.all()

    def test_step_inplacefalse(self):
        body1 = PointMass('b1', 1, np.array([1, 0, 0]), np.array([0, 1, 1]))
        body2 = PointMass('b2', 2, np.array([0, 0, 0]), np.array([0, 1, 1]))
        body3 = PointMass('b3', 1, np.array([-1, 0, 0]), np.array([0, 1, 1]))
        system = NBodySystem(body1, body2, body3)
        system = system.step(dt=0.1,
                             grav_const=1, 
                             inplace=False, 
                             halfstep=False)
        pos_compare1 = system.get_body('b1').position 
        pos_compare1 = pos_compare1 == np.array([0.9775, 0.1, 0.1])
        assert pos_compare1.all()
        pos_compare2 = system.get_body('b2').position 
        pos_compare2 = pos_compare2 == np.array([0, 0.1, 0.1])
        assert pos_compare2.all()
        pos_compare3 = system.get_body('b3').position 
        pos_compare3 = pos_compare3 == np.array([-0.9775, 0.1, 0.1])
        assert pos_compare3.all()
        vel_compare1 = system.get_body('b1').velocity
        vel_compare1 = vel_compare1 == np.array([-0.225, 1, 1])
        assert vel_compare1.all()
        vel_compare2 = system.get_body('b2').velocity
        vel_compare2 = vel_compare2 == np.array([0, 1, 1])
        assert vel_compare1.all()
        vel_compare3 = system.get_body('b3').velocity
        vel_compare3 = vel_compare3 == np.array([0.225, 1, 1])
        assert vel_compare1.all()

    def test_step_halfstep(self):
        body1 = PointMass('b1', 1, np.array([1, 0, 0]), np.array([0, 1, 1]))
        body2 = PointMass('b2', 2, np.array([0, 0, 0]), np.array([0, 1, 1]))
        body3 = PointMass('b3', 1, np.array([-1, 0, 0]), np.array([0, 1, 1]))
        system = NBodySystem(body1, body2, body3)
        system.step(dt=0.1, grav_const=1, halfstep=True)
        pos_compare1 = system.get_body('b1').position 
        pos_compare1 = pos_compare1 == np.array([0.98875, 0.1, 0.1])
        assert pos_compare1.all()
        pos_compare2 = system.get_body('b2').position 
        pos_compare2 = pos_compare2 == np.array([0, 0.1, 0.1])
        assert pos_compare2.all()
        pos_compare3 = system.get_body('b3').position 
        pos_compare3 = pos_compare3 == np.array([-0.98875, 0.1, 0.1])
        assert pos_compare3.all()
        vel_compare1 = system.get_body('b1').velocity
        vel_compare1 = vel_compare1 == np.array([-0.1125, 1, 1])
        assert vel_compare1.all()
        vel_compare2 = system.get_body('b2').velocity
        vel_compare2 = vel_compare2 == np.array([0, 1, 1])
        assert vel_compare1.all()
        vel_compare3 = system.get_body('b3').velocity
        vel_compare3 = vel_compare3 == np.array([0.1125, 1, 1])
        assert vel_compare1.all()

    def test_simulate(self):
        body1 = PointMass('b1', 1, np.array([1, 0, 0]), np.array([0, 1, 1]))
        body2 = PointMass('b2', 2, np.array([0, 0, 0]), np.array([0, 1, 1]))
        body3 = PointMass('b3', 1, np.array([-1, 0, 0]), np.array([0, 1, 1]))
        system = NBodySystem(body1, body2, body3)
        system2 = NBodySystem(body1, body2, body3)
        results = system2.simulate(start='0s',
                                  end='0.2s', 
                                  step='100ms', 
                                  grav_const=1)
        index = pd.timedelta_range(start='0s', end='0.2s', freq='100ms')
        hierarchy = [['b1', 'b2', 'b3'], ['x1', 'x2', 'x3']]
        columns = pd.MultiIndex.from_product(hierarchy, names=['body', 'pos'])
        df = pd.DataFrame(np.zeros((len(index), 9)), 
                          index=index, 
                          columns=columns)
        df.iloc[0] = system.all_positions.flatten()
        system.step(dt=0.1, grav_const=1, halfstep=True)
        df.iloc[1] = system.all_positions.flatten()
        system.step(dt=0.1, grav_const=1)
        df.iloc[2] = system.all_positions.flatten()
        assert df.equals(results)


    def test_centre_of_mass(self):
        body1 = PointMass('b1', 1, np.array([1, 0, 0]), np.array([0, 1, 1]))
        body2 = PointMass('b2', 2, np.array([0, 0, 0]), np.array([0, 1, 1]))
        body3 = PointMass('b3', 1, np.array([-1, 0, 0]), np.array([0, 1, 1]))
        system = NBodySystem(body1, body2, body3)
        centre_of_mass = system.centre_of_mass()
        compare = centre_of_mass == np.array([0, 0, 0])
        assert compare.all()

    def test_stationary(self):
        body1 = PointMass('b1', 1, np.array([1, 0, 0]), np.array([0, 1, 1]))
        body2 = PointMass('b2', 2, np.array([0, 0, 0]), np.array([0, 1, 1]))
        body3 = PointMass('b3', 1, np.array([-1, 0, 0]), np.array([0, 1, 1]))
        system = NBodySystem(body1, body2, body3)
        system.stationary()
        compare = system.all_velocities == np.array([[0, 0, 0], 
                                                    [0, 0, 0],
                                                    [0, 0, 0]])
        assert compare.all()

    def test_getbody(self):
        body1 = PointMass('b1', 1, np.array([1, 0, 0]), np.array([0, 1, 1]))
        body2 = PointMass('b2', 2, np.array([0, 0, 0]), np.array([0, 1, 1]))
        body3 = PointMass('b3', 1, np.array([-1, 0, 0]), np.array([0, 1, 1]))
        system = NBodySystem(body1, body2, body3)
        b2 = system.get_body('b2')
        assert body2.name == b2.name
        assert body2.mass == b2.mass
        pos_compare = body2.position == b2.position
        assert pos_compare.all()
        vel_compare = body2.velocity == b2.velocity
        assert vel_compare.all()
