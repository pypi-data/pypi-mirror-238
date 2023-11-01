import numpy as np

class ImageStats:
    """Class holding metadata about an image

    Parameters
    ----------
    image : numpy ndarray
        the image who's metadata is being stored

    Attributes
    ----------
    min_intensity : float
        the minimum intensity of a pixel/voxel in the given image
    max_intensity : float
        the maximum intensity of a pixel/voxel in the given image
    x_min : int
        the smallest x-coordinate of the given image
    y_min : int
        the smallest y-coordinate of the given image
    z_min : int
        the smallest z-coordinate of the given image
    x_max : int
        the largest x-coordinate of the given image
    y_max : int
        the largest y-coordinate of the given image
    z_max : int
        the largest z-coordinate of the given image
    """

    def __init__(self, image: np.ndarray):
        # checks
        if image is None:
            raise TypeError
        if len(image) == 0:
            raise ValueError

        self.min_intensity = float(np.min(image))
        self.max_intensity = float(np.max(image))

        self.x_min = 0
        self.y_min = 0
        self.z_min = 0

        if len(image.shape) == 3:
            # will be in the form (z, y, x)
            self.z_max = image.shape[0] - 1
            self.y_max = image.shape[1] - 1
            self.x_max = image.shape[2] - 1
        elif len(image.shape) == 2:
            # will be in the form (y, x)
            self.z_max = 0
            self.y_max = image.shape[0] - 1
            self.x_max = image.shape[1] - 1

    @property
    def min_intensity(self) -> float:
        return self._min_intensity

    @min_intensity.setter
    def min_intensity(self, value: float):
        if value is None:
            raise TypeError
        self._min_intensity = value 
    
    @property
    def max_intensity(self) -> float:
        return self._max_intensity
    
    @max_intensity.setter
    def max_intensity(self, value: float):
        if value is None:
            raise TypeError
        self._max_intensity = value
    
    @property
    def x_min(self) -> float:
        return self._x_min
    
    @x_min.setter
    def x_min(self, value: float):
        if value is None:
            raise TypeError
        self._x_min = value
    
    @property
    def y_min(self) -> float:
        return self._y_min
    
    @y_min.setter
    def y_min(self, value: float):
        if value is None:
            raise TypeError
        self._y_min = value
    
    @property
    def z_min(self) -> float:
        return self._z_min
    
    @z_min.setter
    def z_min(self, value: float):
        if value is None:
            raise TypeError
        self._z_min = value
    
    @property
    def x_max(self) -> float:
        return self._x_max
    
    @x_max.setter
    def x_max(self, value: float):
        if value is None:
            raise TypeError
        self._x_max = value
    
    @property
    def y_max(self) -> float:
        return self._y_max
    
    @y_max.setter
    def y_max(self, value: float):
        if value is None:
            raise TypeError
        self._y_max = value
    
    @property
    def z_max(self) -> float:
        return self._z_max
    
    @z_max.setter
    def z_max(self, value: float):
        if value is None:
            raise TypeError
        self._z_max = value