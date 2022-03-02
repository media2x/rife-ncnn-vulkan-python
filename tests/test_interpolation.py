#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pathlib import Path

from PIL import Image
from rife_ncnn_vulkan_python import Rife

tests_path = Path(__file__).parent
images_path = tests_path.parent / "rife_ncnn_vulkan_python" / "rife-ncnn-vulkan" / "images"


def test_default():
    input_image0 = Image.open(images_path / "0.png")
    input_image1 = Image.open(images_path / "1.png")
    interpolator = Rife(-1, num_threads=os.cpu_count())
    output_image = interpolator.process(input_image0, input_image1)
    # output_image.save(tests_path / "0.5_default.png")
    test_image = Image.open(tests_path / "0.5_default.png")
    test_image.close()
    output_image.close()
    input_image0.close()
    input_image1.close()


def test_rife_v4():
    input_image0 = Image.open(images_path / "0.png")
    input_image1 = Image.open(images_path / "1.png")
    interpolator = Rife(-1, model="rife-v4", num_threads=os.cpu_count())
    output_image = interpolator.process(input_image0, input_image1)
    # output_image.save(tests_path / "0.5_v4.png")
    test_image = Image.open(tests_path / "0.5_v4.png")
    test_image.close()
    output_image.close()
    input_image0.close()
    input_image1.close()
