try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

from .dlc_generic_analysis import MainWidget
from .trimmer import Trimmer
from . import (
    analysis,
    dlc,
    geometries,
    gui_objects,
    gui_utils,
    math_utils,
    utils,
    video_tools,
    viewer,
)
