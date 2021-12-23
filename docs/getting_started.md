# Getting Started

## Creating a Basic project

dlc_generic_analysis provides functions and generic class for creating performing more analyses after running DeepLabCut inference.

```python3
import dlc_generic_analysis as dga
from qtpy import QtWidgets
dlc_model_config_path = "~/model/config.yaml"

class Viewer(dga.ViewerWidget):
    def __init__(self):
        super(Viewer, self).__init__()
        
    def position_changed(self, position) -> None:
        super(Viewer, self).position_changed(position)

class MW(dga.MainWidget):
    def __init__(self):
        super(MW, self).__init__()
    
    def on_click_analyze(self):
        video_paths = dga.gui_utils.open_files(self, "Open Files")
        h5s, config = dga.dlc.dlc_analyze(dlc_model_config_path, video_paths)
        
    
    def on_click_view(self):
        video_paths = dga.gui_utils.open_files(self, "Open Files")
        viewer = Viewer()
        

    def on_click_trim(self):
        pass

if __name__ == '__main__':
    app =  QtWidgets.QApplication()
```

## Project Basics
### Tensorflow
to be able to use tensorflow GPU python needs to know where cuda is on your machine. To do this we use 
`os.add_dll_directory(<cuda directory>)` on Windows typically this will look like 
`os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/bin")`.
CUDA 11.2 is the version supported by tensorflow 2.7.0.
