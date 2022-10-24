#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from decimal import Decimal, getcontext

from PIL import Image, ImageChops, ImageStat
from rife_ncnn_vulkan_python import Rife, wrapped

tests_path = Path(__file__).parent
images_path = (
    tests_path.parent / "rife_ncnn_vulkan_python" / "rife-ncnn-vulkan" / "images"
)
# set Decimal precision
getcontext().prec = 4

# Use GPU 0 if available.
gpu_id = 0 if wrapped.get_gpu_count() > 0 else -1


def _calc_image_diff(image0: Image.Image, image1: Image.Image) -> float:
    """
    calculate the percentage of differences between two images

    :param image0 Image.Image: the first frame
    :param image1 Image.Image: the second frame
    :rtype float: the percent difference between the two images
    """
    difference = ImageChops.difference(image0, image1)
    difference_stat = ImageStat.Stat(difference)
    percent_diff = sum(difference_stat.mean) / (len(difference_stat.mean) * 255) * 100
    return percent_diff


def test_default():
    input_image0 = Image.open(images_path / "0.png")
    input_image1 = Image.open(images_path / "1.png")

    interpolator = Rife(gpu_id)
    output_image = interpolator.process(input_image0, input_image1)

    test_image = Image.open(tests_path / "0.5_default.png")
    percent_diff = _calc_image_diff(test_image, output_image)
    logging.getLogger().info(f"%diff: {percent_diff}")

    test_image.close()
    output_image.close()
    input_image0.close()
    input_image1.close()

    assert percent_diff < 0.5


def test_rife_v4():
    input_image0 = Image.open(images_path / "0.png")
    input_image1 = Image.open(images_path / "1.png")

    interpolator = Rife(gpu_id, model="rife-v4")
    output_image = interpolator.process(input_image0, input_image1)

    test_image = Image.open(tests_path / "0.5_v4.png")
    percent_diff = _calc_image_diff(test_image, output_image)
    logging.getLogger().info(f"%diff: {percent_diff}")

    input_image0.close()
    input_image1.close()
    output_image.close()
    test_image.close()

    assert percent_diff < 0.5


def test_rife_v4_6():
    input_image0 = Image.open(images_path / "0.png")
    input_image1 = Image.open(images_path / "1.png")

    interpolator = Rife(gpu_id, model="rife-v4.6")
    output_image = interpolator.process(input_image0, input_image1)

    test_image = Image.open(tests_path / "0.5_v4.6.png")
    percent_diff = _calc_image_diff(test_image, output_image)
    logging.getLogger().info(f"%diff: {percent_diff}")

    input_image0.close()
    input_image1.close()
    output_image.close()
    test_image.close()

    assert percent_diff < 0.5


def test_rife_v4_timestep():
    input_image0 = Image.open(images_path / "0.png")
    input_image1 = Image.open(images_path / "1.png")

    interpolator = Rife(gpu_id, model="rife-v4")
    step = Decimal(0)
    while step <= 1:
        output_image = interpolator.process(input_image0, input_image1, float(step))
        test_image = Image.open(tests_path / f"{float(step)}_v4.png")
        percent_diff = _calc_image_diff(test_image, output_image)
        logging.getLogger().info(f"%diff: {percent_diff}")
        assert percent_diff < 0.5
        test_image.close()
        step += Decimal(0.2)

    input_image0.close()
    input_image1.close()


def test_rife_v4_tta():
    # You might not pass this test if your GPU is weak. :) From poor developer Archie Meng
    input_image0 = Image.open(images_path / "0.png")
    input_image1 = Image.open(images_path / "1.png")

    interpolator = Rife(gpu_id, model="rife-v4", tta_mode=True)
    output_image = interpolator.process(input_image0, input_image1)

    test_image = Image.open(tests_path / "0.5_v4_tta.png")
    percent_diff = _calc_image_diff(test_image, output_image)
    logging.getLogger().info(f"%diff: {percent_diff}")

    input_image0.close()
    input_image1.close()
    output_image.close()
    test_image.close()

    assert percent_diff < 0.5


def test_rife_v4_temporal_tta():
    # You might not pass this test if your GPU is weak. :) From poor developer Archie Meng
    input_image0 = Image.open(images_path / "0.png")
    input_image1 = Image.open(images_path / "1.png")

    interpolator = Rife(gpu_id, model="rife-v4", tta_temporal_mode=True)
    output_image = interpolator.process(input_image0, input_image1)

    test_image = Image.open(tests_path / "0.5_v4_temporal_tta.png")
    percent_diff = _calc_image_diff(test_image, output_image)
    logging.getLogger().info(f"%diff: {percent_diff}")

    input_image0.close()
    input_image1.close()
    output_image.close()
    test_image.close()

    assert percent_diff < 0.5
