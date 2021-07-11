from __future__ import annotations
import sys
from pathlib import Path

from PIL import Image

if __package__:
    import importlib

    raw = importlib.import_module(f"{__package__}.rife_ncnn_vulkan_wrapper")
else:
    import rife_ncnn_vulkan_wrapper as raw


class RIFE:
    def __init__(self,
                 gpuid: int = -1,
                 model: str = "rife-HD",
                 scale: int = 2,
                 tta_mode: bool = False,
                 uhd_mode: bool = False,
                 num_threads: int = 1):
        rife_v2 = ("rife-v2" in model) or ("rife-v3" in model)
        self.model = model

        if (scale & (scale -1)) == 0:
            self.scale = scale
        else:
            raise ValueError("scale should be powers of 2")

        self._raw_rife = raw.RIFEWrapper(gpuid, tta_mode, uhd_mode, num_threads, rife_v2)
        self.load()

    def load(self, model_dir: str = ""):
        if not model_dir:
            model_dir = Path(self.model)
            if not model_dir.is_absolute():
                if (
                        not model_dir.is_dir()
                ):  # try to load it from module path if not exists as directory
                    dir_path = Path(__file__).parent
                    model_dir = dir_path.joinpath("models", self.model)

        if model_dir.exists():
            modeldir_str = raw.StringType()
            if sys.platform in ("win32", "cygwin"):
                modeldir_str.wstr = raw.new_wstr_p()
                raw.wstr_p_assign(modeldir_str.wstr, str(model_dir))
            else:
                modeldir_str.str = raw.new_str_p()
                raw.str_p_assign(modeldir_str.str, str(model_dir))

            self._raw_rife.load(modeldir_str)
        else:
            raise FileNotFoundError(f"{model_dir} not found")

    def process(self, im0: Image, im1: Image) -> list[Image]:
        """
        interpolate frames between im0 and im1
        :param im0: First frame
        :param im1: Second frame
        :return: the interpolation frames between im0 and im1
        """
        def _proc(im0: Image, im1: Image, level) -> list[Image]:
            if level == 1:
                return []
            else:
                im = self._process(im0, im1)
                level /= 2
                return _proc(im0, im, level) + [im] + _proc(im, im1, level)

        return _proc(im0, im1, self.scale)

    def _process(self, im0: Image, im1: Image) -> Image:
        in_bytes0, in_bytes1 = bytearray(im0.tobytes()), bytearray(im1.tobytes())
        channels = int(len(in_bytes0) / (im0.width * im0.height))
        out_bytes = bytearray(len(in_bytes0))

        raw_in_image0 = raw.Image(in_bytes0, im0.width, im0.height, channels)
        raw_in_image1 = raw.Image(in_bytes1, im1.width, im1.height, channels)
        raw_out_image = raw.Image(out_bytes, im0.width, im0.height, channels)

        self._raw_rife.process(raw_in_image0, raw_in_image1, 0.5, raw_out_image)

        return Image.frombytes(im0.mode, (im0.width, im0.height), bytes(out_bytes))


if __name__ == "__main__":
    from time import time

    t = time()
    im0, im1 = Image.open("../images/0.png"), Image.open("../images/1.png")
    rife = RIFE(0)
    ims = rife.process(im0, im1)
    for i, im in enumerate(ims):
        im.save(f"../images/out_{i}.png")
    print(f"Elapsed time: {time() - t}s")