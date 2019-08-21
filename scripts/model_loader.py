"""Module: model loader

get the dictionary of tensorflow network models

networks = {
    'model_name': {
        'graph': tf.Graph instance
        'saver': tf.Saver instance
        'sess': tf.Session instance
        'z': vector (tensor)
        'G_z': vector (tensor)
    }
}

you can run (evaluate) the model

```
results = networks['model_name']['sess'].run(
    networks['model_name']['G_z'],
    {networks['model_name']['z']: input_value})
```

2019-08-22
author: Atsuya Kobayashi
"""

import os
import json
import argparse
import logging
import numpy as np
import tensorflow as tf
from logging import getLogger
from datetime import datetime as d

networks = dict()
model_names = ["birds", "drums", "piano", "sc09", "timit"]

# Set Logger
logging.basicConfig(level=logging.DEBUG)
logger = getLogger(__name__)

# Load Setting
with open("config.json", "r") as f:
    conf = json.load(f)


def load(model_name: str) -> dict:

    base_path = conf["model"]["dir"] + model_name

    global networks
    networks[model_name] = dict()
    logger.info(f"Loading Models {model_name}")

    with tf.Graph().as_default() as graph:

        networks[model_name]["graph"] = graph
        networks[model_name]["saver"] = tf.train.import_meta_graph(
            base_path + "/infer.meta")

        networks[model_name]["sess"] = tf.Session(graph=graph)
        networks[model_name]["saver"].restore(
            networks[model_name]["sess"], base_path + "/model.ckpt")

    networks[model_name]["z"] = networks[model_name]["graph"].get_tensor_by_name('z:0')
    networks[model_name]["G_z"] = networks[model_name]["graph"].get_tensor_by_name('G_z:0')

    return networks


def all():
    for n in model_names:
        load(n)

    return networks


if __name__ == "__main__":
    pass
