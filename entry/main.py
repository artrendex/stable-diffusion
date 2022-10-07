import argparse
from pathlib import Path
from ldm.simplet2i import T2I
from ldm.generate import Generate
from thriftpy2.rpc import make_server
from thrift_server import Dispatcher, service, do_generate


def main():
    parser = argparse.ArgumentParser(description='Do text to image')
    parser.add_argument("process", choices=['serve', "generate"])
    parser.add_argument('--output-path', type=Path, default="tmp", help='Outputs directory')
    parser.add_argument('--text', type=str, default="a rose", help='text content')
    parser.add_argument('--width', type=int, default=512, help='multiple of 64')
    parser.add_argument('--height', type=int, default=512, help='multiple of 64')
    parser.add_argument('--image-path', type=Path, default=None, help='image path')
    parser.add_argument('--steps', type=int, default=50, help='number of iterations')
    parser.add_argument('--seed', type=int, default=None, help='Seed, default to random')
    parser.add_argument("--address", type=str, default="127.0.0.1:6000", help="service address, format ip:port")
    args = parser.parse_args()
    if args.process == "generate":
        model = Generate()
        do_generate(model, args.output_path, args.text, args.image_path, args.width, args.height, args.steps, args.seed)
    else:
        ip, port = args.address.split(':')
        server = make_server(service.StableDiffusion, Dispatcher(),
                             ip, int(port), concurrent=1)
        print(f"serving at {args.address}...")
        server.serve()


if __name__ == "__main__":
    main()
