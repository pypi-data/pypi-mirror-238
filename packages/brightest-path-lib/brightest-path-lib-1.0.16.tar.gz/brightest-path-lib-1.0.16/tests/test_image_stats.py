import numpy as np
import pytest
from brightest_path_lib.image import ImageStats

@pytest.mark.parametrize("image, min_intensity, max_intensity, x_min, y_min, z_min, x_max, y_max, z_max", [
    # 2D rectangular image
    (np.array([[ 4496,  5212,  6863], [ 4533,  5146,  7555],[ 4640,  6082,  8452],[ 5210, 6849, 10010]]), 4496, 10010, 0, 0, 0, 2, 3, 0),
    # 2D square image,
    (np.array([[4496, 5212, 6863], [4533, 5146, 7555], [4640, 6082, 8452]]), 4496, 8452, 0, 0, 0, 2, 2, 0),
    # 3D rectangular image,
    (np.array([[[4496], [4533], [4640]], [[8868], [7113], [5833]]]), 4496, 8868, 0, 0, 0, 0, 2, 1),
    # 3D square image
    (np.array([[[4496, 5212, 6863], [4533, 5146, 7555], [4640, 6082, 8452]], [[8868, 6923, 5690], [7113, 5501, 5216], [5833, 7160, 5928]]]), 4496, 8868, 0, 0, 0, 2, 2, 1)
])
def test_init_with_valid_input(image, min_intensity, max_intensity, x_min, y_min, z_min, x_max, y_max, z_max):
    image_stats = ImageStats(image)
    print(image.shape)
    assert image_stats is not None
    assert image_stats.min_intensity == min_intensity
    assert image_stats.max_intensity == max_intensity
    assert image_stats.x_min == x_min
    assert image_stats.y_min == y_min
    assert image_stats.z_min == z_min
    assert image_stats.x_max == x_max
    assert image_stats.y_max == y_max
    assert image_stats.z_max == z_max

def test_init_with_empty_image():
    with pytest.raises(ValueError):
        ImageStats(np.array([]))

def test_init_with_invalid_input():
    with pytest.raises(TypeError):
        ImageStats() # or you could pass ImageStats(None)

