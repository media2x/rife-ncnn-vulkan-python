# RIFE ncnn Vulkan Python

A Python FFI of nihui/rife-ncnn-vulkan achieved with SWIG.

## Usages

```python
from rife_ncnn_vulkan import RIFE
from PIL import Image

with Image.open("input0.png") as image0:
    with Image.open("input1.png") as image1:
      rife = RIFE(gpuid=0)
      image = rife.process(image0, image1)
      image.save("output.png")
```

More descriptions are to be added.
