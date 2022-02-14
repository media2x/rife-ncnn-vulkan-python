#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: RIFE ncnn Vulkan Python wrapper
Author: ArchieMeng
Date Created: March 29, 2021
Last Modified: May 21, 2021

Dev: K4YT3X
Last Modified: August 17, 2021
"""

# built-in imports
import importlib
import pathlib
import sys

# third-party imports
from PIL import Image

# local imports
if __package__ is None:
    import rife_ncnn_vulkan_wrapper as wrapped
else:
    wrapped = importlib.import_module(f"{__package__}.rife_ncnn_vulkan_wrapper")


class Rife:
    def __init__(
        self,
        gpuid: int = -1,
        model: str = "rife-HD",
        scale: int = 2,
        tta_mode: bool = False,
        uhd_mode: bool = False,
        num_threads: int = 1,
    ):
        # scale must be a power of 2
        if (scale & (scale - 1)) == 0:
            self.scale = scale
        else:
            raise ValueError("scale should be a power of 2")

        # determine if rife-v2 is used
        rife_v2 = ("rife-v2" in model) or ("rife-v3" in model)

        # create raw RIFE wrapper object
        self._rife_object = wrapped.RifeWrapped(
            gpuid, tta_mode, uhd_mode, num_threads, rife_v2
        )
        self._load(model)

    def _load(self, model: str, model_dir: pathlib.Path = None):

        # if model_dir is not specified
        if model_dir is None:
            model_dir = pathlib.Path(model)
            if not model_dir.is_absolute() and not model_dir.is_dir():
                model_dir = pathlib.Path(__file__).parent / "models" / model

        # if the model_dir is specified and exists
        if model_dir.exists():
            modeldir_str = wrapped.StringType()
            if sys.platform in ("win32", "cygwin"):
                modeldir_str.wstr = wrapped.new_wstr_p()
                wrapped.wstr_p_assign(modeldir_str.wstr, str(model_dir))
            else:
                modeldir_str.str = wrapped.new_str_p()
                wrapped.str_p_assign(modeldir_str.str, str(model_dir))

            self._rife_object.load(modeldir_str)

        # if no model_dir is specified but doesn't exist
        else:
            raise FileNotFoundError(f"{model_dir} not found")

    def process(self, image0: Image, image1: Image) -> Image:
        image0_bytes = bytearray(image0.tobytes())
        image1_bytes = bytearray(image1.tobytes())
        channels = int(len(image0_bytes) / (image0.width * image0.height))
        output_bytes = bytearray(len(image0_bytes))

        # convert image bytes into ncnn::Mat Image
        raw_in_image0 = wrapped.Image(
            image0_bytes, image0.width, image0.height, channels
        )
        raw_in_image1 = wrapped.Image(
            image1_bytes, image1.width, image1.height, channels
        )
        raw_out_image = wrapped.Image(
            output_bytes, image0.width, image0.height, channels
        )

        self._rife_object.process(raw_in_image0, raw_in_image1, 0.5, raw_out_image)

        return Image.frombytes(
            image0.mode, (image0.width, image0.height), bytes(output_bytes)
        )


class RIFE(Rife):
    ...
