"""
Script for generating sound by pretrained WaveGAN model from input value `z`
2019-07-19
author: Atsuya Kobayashi (cclab)
"""

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
from scripts.generator import Generator


# Set Parser
parser = argparse.ArgumentParser(description='WaveGAN Sound Generation')
parser.add_argument('-G', '--genre', type=str, default="birds",
                    help='Select the genre from "birds", "drums", "piano", "sc09", "timit"')
parser.add_argument('-N', '--n_files', type=int, default=50,
                    help='Limit of n of saved .wav files')
args = parser.parse_args()

assert args.genre in ["birds", "drums", "piano", "sc09", "timit"], "Select the correct genre"

# Set Logger
logging.basicConfig(level=logging.DEBUG)
logger = getLogger(__name__)

# Load Setting
with open("config.json", "r") as f:
    conf = json.load(f)

# set OSC client
client = udp_client.UDPClient(conf["ip"], conf["ports"]["send"])


def run():
    # OSC receive
    dsp = dispatcher.Dispatcher()
    dsp.map(conf["address"], generate)
    dsp.map(conf["type"], change_genre)
    server = osc_server.ThreadingOSCUDPServer(
        (conf["ip"], conf["ports"]["receive"]), dsp)
    server.serve_forever()


saved_data_pathes = [""] * args.n_files

generator = Generator()

def generate(*value) -> None:
    # Generator input variable `z`
    log("start generating")
    # cut value 256 -> 100
    input_z = value[1:101]
    assert len(input_z) == 100, f"invalid input z shape, expected dim is 100 != {len(input_z)}"
    input_z = np.array(list(map(float, input_z))).reshape(1, 100)
    global generator
    generated = generator.gen(input_z)
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


def _osc_send_msg(address: str, msg_value) -> None:
    msg = osc_message_builder.OscMessageBuilder(address=address)
    msg.add_arg(str(msg_value))
    client.send(msg.build())



# Max Python Logger
log_msg_max = [""] * 10

def log(msg_value: str) -> None:
    logger.info(msg_value)
    global log_msg_max
    log_msg_max.insert(0, msg_value)
    log_msg_max.pop(-1)
    msg = osc_message_builder.OscMessageBuilder(address="/maxlog")
    msg.add_arg("\n".join(log_msg_max))
    client.send(msg.build())


# Change Model Type
def change_genre(*genre_name):
    global generator
    generator.set_type(genre_name[1])
    log(f"Change model to {genre_name}")


if __name__ == "__main__":
    run()
