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


# Set Parser
parser = argparse.ArgumentParser(description='WaveGAN Sound Generation')
parser.add_argument('-S', '--sum', type=int, default=max,
                    help='sum the integers (default: find the max)')
args = parser.parse_args()

# Set Logger
logging.basicConfig(level=logging.DEBUG)
logger = getLogger(__name__)

# Load Setting
with open("config.json", "r") as f:
    conf = json.load(f)

# Load the tensorflow graph
tf.reset_default_graph()
saver = tf.train.import_meta_graph(
    conf["model"]["meta_filepath"])
graph = tf.get_default_graph()
sess = tf.InteractiveSession()

if os.path.exists(conf["model"]["dir"] + "model.ckpt"):
    model_path = conf["model"]["dir"] + "model.ckpt"
else:
    model_path = tf.train.get_checkpoint_state(
        conf["model"]["dir"]).model_checkpoint_path

saver.restore(sess, model_path)

# Synthesize G(z): Generator Model
z = graph.get_tensor_by_name('z:0')
G_z = graph.get_tensor_by_name('G_z:0')

# set OSC client
client = udp_client.UDPClient(conf["ip"], conf["ports"]["send"])


def run():
    # OSC receive
    dsp = dispatcher.Dispatcher()
    dsp.map(conf["address"], generate)
    server = osc_server.ThreadingOSCUDPServer(
        (conf["ip"], conf["ports"]["receive"]), dsp)
    server.serve_forever()


def generate(*value) -> None:
    # Generator input variable `z`
    log("start generating")
    # cut value 256 -> 100
    input_z = value[50:150]
    assert len(input_z) == 100, f"invalid input z shape, expected dim is 100 != {len(input_z)}"
    input_z = np.array(list(map(float, input_z))).reshape(1, 100)

    generated = sess.run(G_z, {z: input_z})[0, :, 0]
    path = "sounds/{}.wav".format(d.now().strftime('%Y%m%d-%H%M%S'))
    log(f"Saving .wav file...")
    sound_write(path, 16000, generated)
    log(f"Saved!: {path}")
    _osc_send_msg(conf["address"], os.getcwd() + "/" + path)


def _osc_send_msg(address: str, msg_value) -> None:
    msg = osc_message_builder.OscMessageBuilder(address=address)
    msg.add_arg(str(msg_value))
    client.send(msg.build())


log_msg_max = [""] * 10

def log(msg_value: str) -> None:
    logger.info(msg_value)
    global log_msg_max
    log_msg_max.insert(0, msg_value)
    log_msg_max.pop(-1)
    msg = osc_message_builder.OscMessageBuilder(address="/maxlog")
    msg.add_arg("\n".join(log_msg_max))
    client.send(msg.build())


if __name__ == "__main__":
    run()
