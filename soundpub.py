#! /usr/bin/env python
import zmq
import random
import sys
import time

class SoundPub(object):
    def __init__(self, port=13000):
        super(self.__class__, self).__init__()
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://eth2:%s" % port)
        print 'sound publish server initialized: {}'.format(self.socket)

    def pub(self, msg, topic=100):
        self.socket.send("%d %s" % (topic, msg))

if __name__ == '__main__':
    tPub = SoundPub()
    time.sleep(1)
    while True:
        tPub.pub('put the bone on the table.')
        time.sleep(1)

