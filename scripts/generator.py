import numpy as np
import tensorflow as tf
from scripts import model_loader
from logging import getLogger
from datetime import datetime as d


class Generator:

    def __init__(self, model_type="birds", useall=True):
        self.models = model_loader.all() if useall else model_loader.load(model_type)
        self.type = model_type

    def gen(self, input_z) -> "numpy.ndarray":
        
        v = self.models[self.type]["sess"].run(
            self.models[self.type]["G_z"],
            {self.models[self.type]["z"]: input_z})[0, :, 0]
        return v

    def set_type(self, model_type: str) -> None:
        assert model_type in ["birds", "drums", "piano", "sc09", "timit"],\
            f"invalid model type name {model_type}"
        self.type = model_type

if __name__ == "__main__":
    pass
