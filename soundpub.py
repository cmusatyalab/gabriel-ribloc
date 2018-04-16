#! /usr/bin/env python
#
# RibLoc Cognitive Assisstance
#
#   Author: Junjue Wang <junjuew@cs.cmu.edu>
#
#   Copyright (C) 2018 Carnegie Mellon University
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from __future__ import print_function

import time

import zmq


class SoundPub(object):
    def __init__(self, port=13000):
        super(self.__class__, self).__init__()
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://eth2:%s" % port)
        print('sound publish server initialized: {}'.format(self.socket))

    def pub(self, msg, topic=100):
        self.socket.send("%d %s" % (topic, msg))


if __name__ == '__main__':
    tPub = SoundPub()
    time.sleep(1)
    while True:
        tPub.pub('put the bone on the table.')
        time.sleep(1)
