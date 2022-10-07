import thriftpy2
from ldm.simplet2i import T2I
from thriftpy2.rpc import client_context
from pathlib import Path

api_thrift = thriftpy2.load("entry/service.thrift",
                            module_name="service_thrift")


if __name__ == '__main__':
    with client_context(api_thrift.StableDiffusion, "0.0.0.0", 6000, socket_timeout=30000) as client:
        client.generate("tmp", imagePath="tmp/input.png", seed=None, steps=None)