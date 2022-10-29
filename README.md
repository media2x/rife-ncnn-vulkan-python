# RIFE ncnn Vulkan Python

![CI](https://github.com/ArchieMeng/rife-ncnn-vulkan-python/workflows/CI/badge.svg)

## Introduction
[rife-ncnn-vulkan](https://github.com/nihui/rife-ncnn-vulkan) is nihui's ncnn implementation of Real-Time Intermediate Flow Estimation for Video Frame Interpolation.

rife-ncnn-vulkan-python wraps [rife-ncnn-vulkan project](https://github.com/nihui/rife-ncnn-vulkan) by SWIG to make it easier to integrate rife-ncnn-vulkan with existing python projects.

## Downloads

Linux/Windos/Mac X86_64 binary build [releases](https://github.com/media2x/rife-ncnn-vulkan-python/releases) are available now.

## Build

First, you have to install python, python development package (Python native development libs in Visual Studio), vulkan SDK and SWIG on your platform. And then, there are two ways to build it:
- Install source distribution from PyPI (Currently in developing, need to download models before build.)
- Use setuptools to build and install into python package directly.
- Use CMake directly (The old way)

### Install from PyPI

```shell
pip install rife-ncnn-vulkan-python
```

### Use setuptools
```shell
python setup.py install
```

### Use CMake

#### Linux
```shell
git clone https://github.com/ArchieMeng/rife-ncnn-vulkan-python.git
cd rife-ncnn-vulkan-python
git submodule update --init --recursive
cmake -B build src
cd build
make
```

#### Windows
I used Visual Studio 2019 and msvc v142 to build this project for Windows.

Install visual studio and open the project directory, and build. Job done.

The only problem on Windows is that, you cannot use [CMake for Windows](https://cmake.org/download/) GUI to generate the Visual Studio solution file and build it. This will make the lib crash on loading.

One way is [using Visual Studio to open the project as directory](https://www.microfocus.com/documentation/visual-cobol/vc50/VS2019/GUID-BE1C48AA-DB22-4F38-9644-E9B48658EF36.html), and build it from Visual Studio. 
And another way is build it from powershell just like what is written in the [release.yml](.github/workflows/release.yml)

## About RIFE

RIFE (Real-Time Intermediate Flow Estimation for Video Frame Interpolation)

https://github.com/hzwer/arXiv2020-RIFE

Huang, Zhewei and Zhang, Tianyuan and Heng, Wen and Shi, Boxin and Zhou, Shuchang

https://rife-vfi.github.io

https://arxiv.org/abs/2011.06294
## Usages

### Example Program

```python
from rife_ncnn_vulkan_python import Rife
from PIL import Image

with Image.open("input0.png") as image0:
    with Image.open("input1.png") as image1:
      rife = Rife(gpuid=0) # or RIFE(0) like upstream
      image = rife.process(image0, image1)
      image.save("output.png")
```

If you encounter a crash or error, try upgrading your GPU driver:

- Intel: https://downloadcenter.intel.com/product/80939/Graphics-Drivers
- AMD: https://www.amd.com/en/support
- NVIDIA: https://www.nvidia.com/Download/index.aspx

### Model

| model | upstream version |
|---|---|
| rife | 1.2 |
| rife-HD | 1.5 |
| rife-UHD | 1.6 |
| rife-anime | 1.8 |
| rife-v2 | 2.0 |
| rife-v2.3 | 2.3 |
| rife-v2.4 | 2.4 |
| rife-v3.0 | 3.0 |
| rife-v3.1 | 3.1 |
| rife-v4 | 4.0 |
| rife-v4.6 | 4.6 |

## Original RIFE Project

- https://github.com/hzwer/arXiv2020-RIFE

## Other Open-Source Code Used

- https://github.com/Tencent/ncnn for fast neural network inference on ALL PLATFORMS
- https://github.com/webmproject/libwebp for encoding and decoding Webp images on ALL PLATFORMS
- https://github.com/nothings/stb for decoding and encoding image on Linux / MacOS
- https://github.com/tronkko/dirent for listing files in directory on Windows
- https://github.com/nihui/rife-ncnn-vulkan the original rife-ncnn-vulkan project
