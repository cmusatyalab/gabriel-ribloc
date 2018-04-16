#! /usr/bin/env python
from __future__ import print_function

import os
import sys
import time

import pyttsx
import zmq

engine = pyttsx.init()

port = "13000"
if len(sys.argv) > 1:
    port = sys.argv[1]
    int(port)

if len(sys.argv) > 2:
    port1 = sys.argv[2]
    int(port1)

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("listening to ribloc soundpub...")
socket.connect("tcp://128.2.211.75:%s" % port)

if len(sys.argv) > 2:
    socket.connect("tcp://128.2.211.75:%s" % port1)

topicfilter = "100"
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

last_msg = None
last_time = time.time()
while True:
    string = socket.recv()
    topic = string.split()[0]
    msg = string[len(topic):]
    print('msg: {}'.format(msg))
    if msg == last_msg and (time.time() - last_time) < 5:
        continue
    else:
        os.system("espeak '{}'".format(msg))
        last_time = time.time()
