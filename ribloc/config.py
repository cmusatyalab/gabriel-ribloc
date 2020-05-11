#!/usr/bin/env python
#
# Cloudlet Infrastructure for Mobile Computing
#   - Task Assistance
#
#   Author: Zhuo Chen <zhuoc@cs.cmu.edu>, Junjue Wang <junjuew@cs.cmu.edu>
#
#   Copyright (C) 2011-2013 Carnegie Mellon University
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

import os
ENGINE_NAME = 'instruction'

# Max image width and height
IMAGE_MAX_WH = 720

# model related info
cur_dir = os.path.dirname(os.path.realpath(__file__))
PROTOTXT = os.path.join(cur_dir, 'model/faster_rcnn_test_opencv.pt')
CAFFEMODEL = os.path.join(cur_dir, 'model/model_iter_20000.caffemodel')
LABELFILE = os.path.join(cur_dir, 'model/labels.txt')
with open(LABELFILE, 'r') as f:
    content = f.read().splitlines()
    LABELS = content
