#!/usr/bin/env python
#
# Cloudlet Infrastructure for Mobile Computing
#   - Task Assistance
#
#   Author: Zhuo Chen <zhuoc@cs.cmu.edu>
#   Modified by: Junjue Wang <junjuew@cs.cmu.edu>
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

'''
This is a simple library file for common CV tasks
'''
from __future__ import absolute_import, division, print_function

import cv2
import numpy as np


def raw2cv_image(raw_data, gray_scale=False):
    img_array = np.asarray(bytearray(raw_data), dtype=np.int8)
    if gray_scale:
        cv_image = cv2.imdecode(img_array, 0)
    else:
        cv_image = cv2.imdecode(img_array, -1)
    return cv_image


def cv_image2raw(img, jpeg_quality=95):
    result, data = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality])
    raw_data = data.tostring()
    return raw_data


def vis_detections(img, dets, labels, thresh=0.5):
    # dets format should be: [x1, y1, x2, y2, confidence, cls_idx]
    if len(dets.shape) < 2:
        return img
    inds = np.where(dets[:, -2] >= thresh)[0]

    img_detections = img.copy()
    if len(inds) > 0:
        for i in inds:
            cls_name = labels[int(dets[i, -1] + 0.1)]
            bbox = dets[i, :4]
            score = dets[i, -2]
            text = "%s : %f" % (cls_name, score)
            cv2.rectangle(img_detections, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 0, 255), 8)
            cv2.putText(img_detections, text, (int(bbox[0]), int(bbox[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    return img_detections
