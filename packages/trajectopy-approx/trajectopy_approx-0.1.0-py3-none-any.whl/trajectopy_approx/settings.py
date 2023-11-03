from enum import Enum
from dataclasses import dataclass
from yaml_dataclass import Settings


class RotApprox(Enum):
    """
    Enumeration class handling different techniques for rpy approximation
    """

    WINDOW = 0
    INTERP = 1
    CUBIC = 2

    def __str__(self) -> str:
        if self.value == 0:
            return "window"

        return "lap_interp" if self.value == 1 else "cubic"


ROT_APPROX = {
    "lap_interp": RotApprox.INTERP,
    "window": RotApprox.WINDOW,
    "cubic": RotApprox.CUBIC,
}


@dataclass
class ApproximationSettings(Settings):
    """Dataclass defining approximation configuration"""

    fe_int_size: float = 0.15
    fe_min_obs: int = 25
    rot_approx_technique: int = 0
    rot_approx_win_size: float = 0.15
