try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

from .dlc_generic_analysis import MainWindow, MainWidget
