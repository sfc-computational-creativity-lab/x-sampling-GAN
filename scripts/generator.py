import os
import json
import argparse
import logging
import numpy as np
import tensorflow as tf
from logging import getLogger
from datetime import datetime as d
from pythonosc import osc_message_builder, udp_client
from pythonosc import dispatcher, osc_server
from scipy.io.wavfile import write as sound_write


class Generator:

    def __init__(self):
        return

    def 


def generate(*value) -> None:
    # Generator input variable `z`
    log("start generating")
    # cut value 256 -> 100
    input_z = value[1:101]
    assert len(input_z) == 100, f"invalid input z shape, expected dim is 100 != {len(input_z)}"
    input_z = np.array(list(map(float, input_z))).reshape(1, 100)

    generated = sess.run(G_z, {z: input_z})[0, :, 0]
    path = "sounds/{}.wav".format(d.now().strftime('%Y%m%d-%H%M%S'))
    log(f"saving .wav file...")
    sound_write(path, 16000, generated)
    log(f"saved: {path}")
    _osc_send_msg(conf["address"], os.getcwd() + "/" + path)

    # .wav file
    global saved_data_pathes
    saved_data_pathes.append(path)
    if os.path.exists(saved_data_pathes[0]):
        os.remove(saved_data_pathes[0])
    saved_data_pathes.pop(0)
