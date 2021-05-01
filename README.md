# RIFE ncnn Vulkan Python

![CI](https://github.com/ArchieMeng/rife-ncnn-vulkan-python/workflows/CI/badge.svg)

## Introduction
[rife-ncnn-vulkan](https://github.com/nihui/rife-ncnn-vulkan) is nihui's ncnn implementation of Real-World Super-Resolution via Kernel Estimation and Noise Injection super resolution.

rife-ncnn-vulkan-python wraps [rife-ncnn-vulkan project](https://github.com/nihui/rife-ncnn-vulkan) by SWIG to make it easier to integrate rife-ncnn-vulkan with existing python projects.

## Downloads

Linux/Windos/Mac X86_64 build releases are available now. **However, for Linux (Like Ubuntu 18.04) with an older GLIBC (version < 2.29), you may try to use the ubuntu-1804 release or just compile it on your own.**

## Build

First, you have to install python, python development package (Python native development libs in Visual Studio), vulkan SDK and SWIG on your platform. And then:

### Linux
```shell
git clone https://github.com/ArchieMeng/rife-ncnn-vulkan-python.git
cd rife-ncnn-vulkan-python
git submodule update --init --recursive
cmake -B build src
cd build
make
```

### Windows
I used Visual Studio 2019 and msvc v142 to build this project for Windows.

Install visual studio and open the project directory, and build. Job done.

The only problem on Windows is that, you cannot use [CMake for Windows](https://cmake.org/download/) to generate the Visual Studio solution file and build it. This will make the lib crash on loading.

The only way is [use Visual Studio to open the project as directory](https://www.microfocus.com/documentation/visual-cobol/vc50/VS2019/GUID-BE1C48AA-DB22-4F38-9644-E9B48658EF36.html), and build it from Visual Studio.

## About RIFE

RIFE (Real-Time Intermediate Flow Estimation for Video Frame Interpolation)

https://github.com/hzwer/arXiv2020-RIFE

Huang, Zhewei and Zhang, Tianyuan and Heng, Wen and Shi, Boxin and Zhou, Shuchang

https://rife-vfi.github.io

https://arxiv.org/abs/2011.06294
## Usages

### Example Program

```Python
from PIL import Image
from rife_ncnn_vulkan import RIFE

im0, im1 = Image.open("0.png"), Image.open("1.png")
rife = RIFE(0)
im = rife.process(im0, im1)
im.save("interframe.png")
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

## Sample Images

### Original Image

![origin0](images/0.png)
![origin1](images/1.png)

### Interpolate with rife rife-anime model

![rife](images/out.png)

### Interpolate with rife rife-anime model + TTA-s

![rife](images/outx.png)

## Original RIFE Project

- https://github.com/hzwer/arXiv2020-RIFE

## Other Open-Source Code Used

- https://github.com/Tencent/ncnn for fast neural network inference on ALL PLATFORMS
- https://github.com/webmproject/libwebp for encoding and decoding Webp images on ALL PLATFORMS
- https://github.com/nothings/stb for decoding and encoding image on Linux / MacOS
- https://github.com/tronkko/dirent for listing files in directory on Windows
- https://github.com/nihui/rife-ncnn-vulkan the original rife-ncnn-vulkan project
