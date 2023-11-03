"""
Gereon Tombrink, 2023
mail@gtombrink.de
"""
from yaml_dataclass import Settings, dataclass


@dataclass
class SortingSettings(Settings):
    """This class stores all sorting settings"""

    discard_missing: bool = True
    voxel_size: float = 0.05
    movement_threshold: float = 0.005
    k_nearest: int = 4
