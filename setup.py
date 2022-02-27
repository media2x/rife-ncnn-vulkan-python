#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pathlib
import setuptools
import shutil
import sys
import tempfile
import zipfile

# the directory that contains all RIFE models
# required only for building wheels
MODELS_PATH = (
    pathlib.Path(__file__).parent
    / "rife_ncnn_vulkan_python"
    / "rife-ncnn-vulkan"
    / "models"
)

# HACK: allows pip to load user site packages when running setup
if "PYTHONNOUSERSITE" in os.environ:
    os.environ.pop("PYTHONNOUSERSITE")

sys.path.append(
    str(
        pathlib.Path.home()
        / ".local/lib/python{}.{}/site-packages".format(
            sys.version_info.major, sys.version_info.minor
        )
    )
)
sys.path.append(
    "/usr/lib/python{}.{}/site-packages".format(
        sys.version_info.major, sys.version_info.minor
    )
)

# external modules must be imported after the hack
import cmake_build_extension
import requests


def download(url, chunk_size=4096):
    # create a temporary file to contain the downloaded file
    handle, path_str = tempfile.mkstemp()
    path = pathlib.Path(path_str)

    # create download stream and size
    stream = requests.get(url, stream=True, allow_redirects=True)
    total_size = int(stream.headers.get("content-length", 0))

    # print download information summary
    print(f"Downloading: {url}")
    print(f"Total size: {total_size}")
    print(f"Chunk size: {chunk_size}")
    print(f"Saving to: {path}")

    # Write content into file
    with os.fdopen(handle, "wb") as output:
        for chunk in stream.iter_content(chunk_size=chunk_size):
            output.write(chunk) if chunk else None

    # return the full path of saved file
    return path


def download_models() -> None:
    rife_ncnn_vulkan_zip = download(
        "https://github.com/nihui/rife-ncnn-vulkan/archive/"
        "c26c90bb643f93953204e3f3fcd1adc347336150.zip"
    )

    with zipfile.ZipFile(rife_ncnn_vulkan_zip) as archive:
        with tempfile.TemporaryDirectory() as tempdir:
            archive.extractall(tempdir)
            shutil.move(
                pathlib.Path(tempdir) / archive.namelist()[0] / "models", MODELS_PATH
            )

    # remove the temporary files/dirs
    rife_ncnn_vulkan_zip.unlink()


# when building bdist wheels/installing the package
if sys.argv[1] == "bdist_wheel":

    # if the models are not present
    # download and extract the models from nihui/rife-ncnn-vulkan
    if not MODELS_PATH.exists():
        download_models()


setuptools.setup(
    ext_modules=[
        cmake_build_extension.CMakeExtension(
            name="rife-ncnn-vulkan-python",
            install_prefix="rife_ncnn_vulkan_python",
            write_top_level_init="from .rife_ncnn_vulkan import Rife, RIFE",
            source_dir=str(pathlib.Path(__file__).parent / "rife_ncnn_vulkan_python"),
            cmake_configure_options=[
                "-DBUILD_SHARED_LIBS:BOOL=OFF",
                "-DCALL_FROM_SETUP_PY:BOOL=ON",
            ],
        )
    ],
    cmdclass={"build_ext": cmake_build_extension.BuildExtension},
)
