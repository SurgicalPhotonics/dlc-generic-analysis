try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

from .dlc_generic_analysis import MainWidget
from . import (
    analysis,
    dlc,
    dlc_generic_analysis,
    geometries,
    gui_objects,
    gui_utils,
    math_utils,
    trimmer,
    utils,
    video_tools,
    viewer,
)
