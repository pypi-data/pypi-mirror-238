from brightest_path_lib import input, algorithm
from skimage import data
import numpy as np

def test_initialize_astar_search():
    cost_function = input.CostFunction.RECIPROCAL
    heuristic_function = input.HeuristicFunction.EUCLIDEAN

    twoDImage = data.cells3d()[30, 0] # darker image
    start_point = np.array([0,192])
    goal_point = np.array([198,9])

    astar = algorithm.AStarSearch(
        image=twoDImage,
        start_point=start_point,
        goal_point=goal_point,
        cost_function=cost_function,
        heuristic_function=heuristic_function
        )

    assert astar is not None
