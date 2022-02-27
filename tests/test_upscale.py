#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image
from rife_ncnn_vulkan_python import Rife
import time

start_time = time.time()
input_image0 = Image.open("input0.png")
input_image1 = Image.open("input1.png")
interpolator = Rife(0)
output_image = interpolator.process(input_image0, input_image1)
output_image.save("output.png")
print(f"Elapsed time: {time.time() - start_time} secs")
