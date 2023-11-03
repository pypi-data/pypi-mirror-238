"""
spatialsorter 

Gereon Tombrink, 2023
mail@gtombrink.de
"""
from typing import Callable
import numpy as np
import logging

logger = logging.getLogger("root")


def lengths_from_xyz(xyz: np.ndarray) -> np.ndarray:
    """
    Computes the cumulative distance along a path defined by a sequence of
    3D points.

    Args:
        xyz (np.ndarray): An array of shape (n, 3) containing the x, y, and z
            coordinates of the path.

    Returns:
        np.ndarray: An array of shape (n,) containing the cumulative distance
            along the path.
    """
    if not isinstance(xyz, np.ndarray):
        logger.error("Invalid data type %s", type(xyz))
        return np.array([])

    xyz_1 = xyz[0:-1, :]
    xyz_2 = xyz[1:, :]

    diff = xyz_2 - xyz_1

    dists = np.linalg.norm(diff, axis=1)
    return np.r_[0, np.cumsum(dists)]


def moving(
    *, x: np.ndarray, win_size: int, function: Callable[[np.ndarray], float]
) -> np.ndarray:
    """
    Computes values with a given window size and function.
    For example, if function=np.std this method computes the moving
    standard deviation.

    Args:
        x (np.ndarray): The input array.
        win_size (int): The size of the window.
        function (Callable[[np.ndarray], float]): The function to apply to the window.

    Returns:
        np.ndarray: An array containing the computed values.
    """
    if not callable(function):
        raise TypeError("'function' must be Callable[[np.ndarray], float]")

    if win_size in {1, 0, -1}:
        return x

    ext = int(win_size // 2)

    # extend array
    x_ext = np.pad(x, pad_width=(ext, ext + 1), mode="wrap")

    # moving
    mov = [
        function(x_ext[i - ext : i + ext + 1]) for i in range(ext, len(x_ext) - ext - 1)
    ]

    return np.array(mov)
