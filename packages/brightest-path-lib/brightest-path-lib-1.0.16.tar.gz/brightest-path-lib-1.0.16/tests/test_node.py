import numpy as np
import pytest
from brightest_path_lib.node import Node

@pytest.mark.parametrize("point, g_score, h_score, predecessor", [
    (np.array([13, 0]), 12.10, 22.9, None),
    (np.array([77, 99]), 55.8, 22.9, Node(np.array([10, 20]), 12.1, 22.9, None)),
])
def test_init_with_valid_input(point, g_score, h_score, predecessor):
    node = Node(point, g_score, h_score, predecessor)
    assert node is not None
    assert np.array_equal(node.point, point)
    assert node.g_score == g_score
    assert node.h_score == h_score
    assert node.predecessor == predecessor

@pytest.mark.parametrize("point, g_score, h_score, predecessor", [
    (None, 12.10, 22.9, None),
    (np.array([22, 88]), None, 22.9, None),
    (np.array([55, 77]), 50.2, None, None),
])
def test_init_with_invalid_input(point, g_score, h_score, predecessor):
    with pytest.raises(TypeError):
        Node(point, g_score, h_score, predecessor)

def test_init_with_empty_node_coordinates():
    with pytest.raises(ValueError):
        Node(np.array([]), 12.10, 22.9, None)
        