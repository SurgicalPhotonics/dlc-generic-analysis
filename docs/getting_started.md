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
        video_paths = dga.gui_utils.open_files(self, "Open Files")[0]
        viewer = Viewer()
        viewer.load_video(video_paths)
        viewer.play()

    def on_click_trim(self):
        pass

if __name__ == '__main__':
    app =  QtWidgets.QApplication()
```

## Project Basics
### Tensorflow GPU
to be able to use tensorflow GPU on Windows, python needs to know where cuda is on your machine. To do this we use 
`os.add_dll_directory(<cuda directory>)` on Windows CUDA adds an environment variable called `CUDA_PATH` or 
`CUDA_PATH_V11_2` to get the specific cuda version we want if you have multiple cuda versions installed. Typically this 
will look like `os.add_dll_directory(os.environ['CUDA_PATH_V11_2'])`.
CUDA 11.2 is selected here as it is the version supported by tensorflow 2.7.0.
