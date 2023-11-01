import numpy as np
import pytest
from brightest_path_lib.node.bidirectional_node import BidirectionalNode

@pytest.mark.parametrize("point, g_score_from_start, g_score_from_goal, h_score_from_start, h_score_from_goal, f_score_from_start, f_score_from_goal, predecessor_from_start, predecessor_from_goal", [
    (np.array([13, 0]), 0, 12.10, 0, 22.9, 0, 10, None, None),
    (np.array([77, 99]), 55.8, 22.9, 92, 88, 32, 59, BidirectionalNode(np.array([10, 20])), None),
    (np.array([77, 99]), 55.8, 22.9, 92, 88, 32, 59, None, BidirectionalNode(np.array([10, 20])))
])
def test_init_with_valid_input(
    point, 
    g_score_from_start, 
    g_score_from_goal,
    h_score_from_start,
    h_score_from_goal,
    f_score_from_start,
    f_score_from_goal,
    predecessor_from_start,
    predecessor_from_goal
):
    node = BidirectionalNode(
        point,
        g_score_from_start,
        g_score_from_goal,
        h_score_from_start,
        h_score_from_goal,
        f_score_from_start,
        f_score_from_goal,
        predecessor_from_start,
        predecessor_from_goal
    )
    assert node is not None
    assert np.array_equal(node.point, point)
    assert node.g_score_from_start == g_score_from_start
    assert node.g_score_from_goal == g_score_from_goal
    assert node.h_score_from_start == h_score_from_start
    assert node.h_score_from_goal == h_score_from_goal
    assert node.f_score_from_start == f_score_from_start
    assert node.f_score_from_goal == f_score_from_goal
    assert node.predecessor_from_start == predecessor_from_start
    assert node.predecessor_from_goal == predecessor_from_goal

def test_init_with_invalid_input():
    with pytest.raises(TypeError):
        BidirectionalNode(point=None)

def test_init_with_empty_node_coordinates():
    with pytest.raises(ValueError):
        BidirectionalNode(point=np.array([]))
        