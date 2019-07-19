"""
Test Script for run.py,
after exec run.py, run this script
"""
import json
import logging
import numpy as np
import threading
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
from logging import getLogger


# Set Logger
logging.basicConfig(level=logging.DEBUG)
log = getLogger(__name__)
# open config file
with open("config.json", "r") as f:
    conf = json.load(f)
# make client instance
client = udp_client.UDPClient(conf["ip"], conf["ports"]["receive"])


def osc_receive():
    disp = dispatcher.Dispatcher()
    disp.map(conf["address"], _osc_sample)
    server = osc_server.ThreadingOSCUDPServer(
        (conf["ip"], conf["ports"]["send"]), disp)
    server.serve_forever()
    return


def _osc_sample(*msg):
    log.info(f"Received: {msg[0]}, {msg[1]}")
    return


def osc_send():
    # make random input vector `z`
    z = (np.random.rand(1, 100) * 2.) - 1
    z = " ".join(list(map(str, z[0, :])))  # convert to_string
    msg = osc_message_builder.OscMessageBuilder(address=conf["address"])
    msg.add_arg(z)

    log.info("send `z` vector to {}:{}".format(
        conf['address'], conf['ports']['receive']))
    client.send(msg.build())
    return
 

if __name__ == '__main__':
    # port num conflict
    # osc_receive()
    osc_send()
