#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image
from rife_ncnn_vulkan_python import Rife
from pathlib import Path
import pytest

tests_path = Path(__file__).parent
images_path = tests_path.parent / "rife_ncnn_vulkan_python" / "rife-ncnn-vulkan" / "images"


def test_default():
    input_image0 = Image.open(images_path / "0.png")
    input_image1 = Image.open(images_path / "1.png")
    interpolator = Rife(0)
    output_image = interpolator.process(input_image0, input_image1)
    test_image = Image.open(tests_path / "0.5_default.png")
    assert test_image.tobytes() == output_image.tobytes()
    test_image.close()
    output_image.close()
    input_image0.close()
    input_image1.close()


def test_rife_v4():
    input_image0 = Image.open(images_path / "0.png")
    input_image1 = Image.open(images_path / "1.png")
    interpolator = Rife(0, model="rife-v4")
    output_image = interpolator.process(input_image0, input_image1)
    test_image = Image.open(tests_path / "0.5_v4.png")
    assert test_image.tobytes() == output_image.tobytes()
    test_image.close()
    output_image.close()
    input_image0.close()
    input_image1.close()
