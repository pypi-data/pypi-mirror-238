import numpy as np
import pytest
from brightest_path_lib.heuristic.euclidean import Euclidean

@pytest.mark.parametrize("scale, scale_x, scale_y, scale_z", [
    ((1.0, 1.0), 1.0, 1.0, 1.0),
    ((0.5, 0.5, 0.5), 0.5, 0.5, 0.5),
])
def test_init_with_valid_input(scale, scale_x, scale_y, scale_z):
    euclidean_heuristic = Euclidean(scale)
    assert euclidean_heuristic is not None
    assert euclidean_heuristic.scale_x == scale_x
    assert euclidean_heuristic.scale_y == scale_y
    assert euclidean_heuristic.scale_z == scale_z

def test_init_with_invalid_input():
    with pytest.raises(TypeError):
        Euclidean()

def test_init_with_empty_input():
    with pytest.raises(ValueError):
        Euclidean(np.array([]))

@pytest.mark.parametrize("scale, start, goal, expected_estimate", [
    # points of the form - y, x for 2D, and z, x, y for 3D
    ((1.0, 1.0), np.array([10, 20]), np.array([50, 40]), 44.721),
    ((1.0, 0.5, 0.2), np.array([10, 20, 30]), np.array([50, 40, 90]), 36.932)
])
def test_estimate_cost_to_goal_with_valid_input(scale, start, goal, expected_estimate):
    euclidean_heuristic = Euclidean(scale)
    estimate = euclidean_heuristic.estimate_cost_to_goal(start, goal) 
    round(estimate, 3) == expected_estimate

@pytest.mark.parametrize("start, goal", [
    (np.array([10, 20]), None),
    (None, np.array([20, 30])),
])
def test_estimate_cost_to_goal_with_invalid_inputs(start, goal):
    with pytest.raises(TypeError):
        euclidean_heuristic = Euclidean((1.0, 1.0))
        euclidean_heuristic.estimate_cost_to_goal(start, goal)

@pytest.mark.parametrize("start, goal", [
    (np.array([10, 20]), np.array([10, 20, 30])),
    (np.array([]), np.array([])),
])
def test_estimate_cost_to_goal_with_empty_inputs(start, goal):
    with pytest.raises(ValueError):
        euclidean_heuristic = Euclidean((1.0, 1.0))
        euclidean_heuristic.estimate_cost_to_goal(start, goal)
