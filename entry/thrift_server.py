import warnings

import thriftpy2

from ldm.generate import Generate
from thriftpy2.rpc import make_server
from pathlib import Path


service = thriftpy2.load("entry/service.thrift",
                          module_name="service_thrift")

def do_generate(model, output_path: str, text: str = "",  image_path: str = None,
                width: int = 512, height: int = 512, steps: int = 50, seed: int = None):
    output_path = Path(output_path)
    assert output_path.exists(), "Output path does not exist."
    assert width % 64 == 0, "Width must be multiple of 64"
    assert height % 64 == 0, "Height must be multiple of 64"
    kwargs = {
        "width": width,
        "height": height,
        "outdir": output_path,
        "steps": steps,
        "seed": seed,
    }
    if not text:
        assert Path(image_path).exists(), "Image prompt is required if text prompt is empty."
        kwargs["skip_normalize"] = True
    if image_path and Path(image_path).exists():
        model.img2img(text, **kwargs, init_img=image_path)
    else:
        model.txt2img(text, **kwargs)


class Dispatcher(object):

    def __init__(self) -> None:
        self.model = Generate()
        self.model.load_model()

    def generate(self, output_path: str, text_input: str = "", image_path: str = None, width: int = 512, height: int = 512, steps: int = 50, seed: int = None):
        do_generate(self.model, output_path, text_input, image_path, width, height, steps, seed)


def main():
    server = make_server(service.StableDiffusion, Dispatcher(),
                         '127.0.0.1', 6000, concurrent=1)
    print("serving...")
    server.serve()


if __name__ == '__main__':
    main()