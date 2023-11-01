import numpy as np
import pytest
from brightest_path_lib.cost.reciprocal import Reciprocal

@pytest.mark.parametrize("min_intensity, max_intensity", [
    (10, 20),
    (-100, 100),
    (459.10, 778.19)
])
def test_init_with_valid_input(min_intensity, max_intensity):
    reciprocal_cost_function = Reciprocal(min_intensity, max_intensity)
    assert reciprocal_cost_function is not None
    assert reciprocal_cost_function.min_intensity == min_intensity
    assert reciprocal_cost_function.max_intensity == max_intensity

@pytest.mark.parametrize("min_intensity, max_intensity", [
    (555.3, None),
    (None, 255.0),
    (None, None)
])
def test_init_with_invalid_input_type(min_intensity, max_intensity):
    with pytest.raises(TypeError):
        Reciprocal(min_intensity, max_intensity)

def test_init_when_min_intensity_greater_than_max():
    with pytest.raises(ValueError):
        Reciprocal(1960.0, 330.0)

@pytest.mark.parametrize("min_intensity, max_intensity, intensity_at_new_point, expected_cost", [
    (0, 100, 0, 1E6),
    (-100, 100, 0, 0.008),
    (0, 100, 75, 0.005)
])
def test_cost_of_moving_to(min_intensity, max_intensity, intensity_at_new_point, expected_cost):
    reciprocal_cost_function = Reciprocal(min_intensity, max_intensity)
    cost = reciprocal_cost_function.cost_of_moving_to(float(intensity_at_new_point))
    assert round(cost, 3) == round(expected_cost, 3)

def test_minimum_step_cost():
    reciprocal_cost_function = Reciprocal(0, 100)
    min_step_cost = reciprocal_cost_function.minimum_step_cost()
    assert round(min_step_cost, 4) ==  0.0039
