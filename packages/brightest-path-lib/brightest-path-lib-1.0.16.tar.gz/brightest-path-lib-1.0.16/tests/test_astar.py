import numpy as np
import pytest
from brightest_path_lib.algorithm.astar import AStarSearch
from brightest_path_lib.input import CostFunction, HeuristicFunction

two_dim_image = np.array([[ 4496,  5212,  6863, 10113,  7055],
       [ 4533,  5146,  7555, 10377,  5768],
       [ 4640,  6082,  8452, 10278,  4543],
       [ 5210,  6849, 10010,  8677,  3911],
       [ 5745,  7845, 11113,  7820,  3551]])
two_dim_start_point = np.array([0,0])
two_dim_goal_point = np.array([4,4])
two_dim_scale = (1.0, 1.0)
two_dim_result = np.array([np.array([0, 0]), np.array([0, 1]), np.array([1, 2]), np.array([2, 3]), np.array([3, 3]), np.array([4, 3]), np.array([4, 4])])

three_dim_image = np.array([[[ 4496,  5212,  6863, 10113,  7055],
        [ 4533,  5146,  7555, 10377,  5768],
        [ 4640,  6082,  8452, 10278,  4543],
        [ 5210,  6849, 10010,  8677,  3911],
        [ 5745,  7845, 11113,  7820,  3551]],

       [[ 8868,  6923,  5690,  6781,  5738],
        [ 7113,  5501,  5216,  4789,  5501],
        [ 5833,  7160,  5928,  5596,  5406],
        [ 6402,  6259,  5501,  4458,  6449],
        [ 6117,  6022,  7160,  7113,  7066]]])
three_dim_start_point = np.array([0,0,0])
three_dim_goal_point = np.array([0,4,4])
three_dim_scale = (1.0, 1.0, 1.0)
three_dim_result = np.array([np.array([0, 0, 0]), np.array([1, 1, 0]), np.array([1, 2, 1]), np.array([0, 3, 2]), np.array([0, 4, 3]), np.array([0, 4, 4])])

@pytest.mark.parametrize("image, start_point, goal_point, scale", [
    (two_dim_image, two_dim_start_point, two_dim_goal_point, two_dim_scale),
    (two_dim_image.astype(np.uint32), two_dim_start_point, two_dim_goal_point, two_dim_scale),
    ((two_dim_image/np.max(two_dim_image) * 255).astype(np.uint8), two_dim_start_point, two_dim_goal_point, two_dim_scale),
    (three_dim_image, three_dim_start_point, three_dim_goal_point, three_dim_scale),
    (three_dim_image.astype(np.uint32), three_dim_start_point, three_dim_goal_point, three_dim_scale),
    ((three_dim_image/np.max(three_dim_image) * 255).astype(np.uint8), three_dim_start_point, three_dim_goal_point, three_dim_scale),
])
def test_init_with_valid_input(image, start_point, goal_point, scale):
    astar = AStarSearch(image, start_point, goal_point, scale)
    assert astar is not None
    assert np.array_equal(astar.image, image)
    assert np.array_equal(astar.start_point, start_point)
    assert np.array_equal(astar.goal_point, goal_point)
    assert np.array_equal(astar.scale, scale)
    assert astar.cost_function is not None
    assert astar.heuristic_function is not None
    assert len(astar.result) == 0

@pytest.mark.parametrize("image, start_point, goal_point, scale", [
    (None, two_dim_start_point, two_dim_goal_point, two_dim_scale),
    (two_dim_image, None, two_dim_goal_point, two_dim_scale),
    (three_dim_image, three_dim_start_point, None, three_dim_scale),
])
def test_init_with_invalid_input(image, start_point, goal_point, scale):
    with pytest.raises(TypeError):
        AStarSearch(image, start_point, goal_point, scale)

@pytest.mark.parametrize("image, start_point, goal_point, scale", [
    (np.array([]), two_dim_start_point, two_dim_goal_point, two_dim_scale),
    (two_dim_image, np.array([]), two_dim_goal_point, two_dim_scale),
    (three_dim_image, three_dim_start_point, np.array([]), three_dim_scale),
])
def test_init_with_empty_input(image, start_point, goal_point, scale):
    with pytest.raises(ValueError):
        AStarSearch(image, start_point, goal_point, scale)

@pytest.mark.parametrize("image, start_point, goal_point, scale, expected_result", [
    (two_dim_image, two_dim_start_point, two_dim_goal_point, two_dim_scale, two_dim_result),
    (two_dim_image.astype(np.uint32), two_dim_start_point, two_dim_goal_point, two_dim_scale, two_dim_result),
    ((two_dim_image/np.max(two_dim_image) * 255).astype(np.uint8), two_dim_start_point, two_dim_goal_point, two_dim_scale, two_dim_result),
    (three_dim_image, three_dim_start_point, three_dim_goal_point, three_dim_scale, three_dim_result),
    (three_dim_image.astype(np.uint32), three_dim_start_point, three_dim_goal_point, three_dim_scale, three_dim_result),
    ((three_dim_image/np.max(three_dim_image) * 255).astype(np.uint8), three_dim_start_point, three_dim_goal_point, three_dim_scale, three_dim_result),
])
def test_search(image, start_point, goal_point, scale, expected_result):
    astar = AStarSearch(image, start_point, goal_point, scale)
    result = astar.search()
    assert np.array_equal(result, expected_result)
