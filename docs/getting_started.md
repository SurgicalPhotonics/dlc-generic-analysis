# Getting Started

## Project Basics
### Tensorflow
to be able to use tensorflow GPU python needs to know where cuda is on your machine. To do this we use 
`os.add_dll_directory(<cuda directory>)` on Windows typically this will look like 
`os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/bin")`.
CUDA 11.2 is the version supported by tensorflow 2.7.0.
