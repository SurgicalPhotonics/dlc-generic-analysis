try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

from .dlc import dlc_analyze
try:
    from . import gui_objects, gui_utils, viewer
    from .trimmer import Trimmer
    from .dlc_generic_analysis import MainWidget

except (ModuleNotFoundError, ImportError) as e:
    pass

from . import (
    analysis,
    geometries,
    math_utils,
    utils,
    video_tools,
)


