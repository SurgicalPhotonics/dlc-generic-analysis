import os
import sys

try:
    cuda_bin = os.path.join(os.environ.get("CUDA_PATH_V11_2"), "bin")
    os.add_dll_directory(cuda_bin)
except TypeError as e:
    pass
try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
from logging import info
import matplotlib as mpl

try:
    import qtpy
except (ModuleNotFoundError, ImportError) as e:
    info("aemotrics gui not loaded")
if "qtpy" in sys.modules and ("PySide2" in sys.modules or "PyQt5" in sys.modules):
    from dlc_generic_analysis import gui_objects, gui_utils
    from dlc_generic_analysis.trimmer import Trimmer
    from dlc_generic_analysis.dlc_generic_analysis import MainWidget
    from dlc_generic_analysis.viewer import ViewerWidget

    mpl.use("QtAgg")
else:
    info("dlc-generic-analysis GUI not loaded")
    mpl.use("agg")
from dlc_generic_analysis import geometries, math_utils, utils, video_tools, filter
from dlc_generic_analysis.dlc import dlc_analyze
from dlc_generic_analysis.analysis import Analysis
from dlc_generic_analysis import line
