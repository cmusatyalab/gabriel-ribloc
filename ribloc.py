#!/usr/bin/env python
#
# Cloudlet Infrastructure for Mobile Computing
#
#   Author: Kiryong Ha <krha@cmu.edu>
#           Zhuo Chen <zhuoc@cs.cmu.edu>
#           Junjue Wang <junjuew@cs.cmu.edu>
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

import numpy as np
import logging
from gabriel_server import cognitive_engine
from gabriel_protocol import gabriel_pb2
from .object_detect import FasterRCNNOpenCVDetector
import instruction_pb2
import instructions
import sys
import os
import cv2

# Max image width and height
IMAGE_MAX_WH = 720
PROTOTXT = 'model/faster_rcnn_test.pt'
CAFFEMODEL = 'model/model.caffemodel'

def _get_labels():
    with open('model/labels.txt', 'r') as f:
        content = f.read().splitlines()
        return content

class RiblocEngine(cognitive_engine.Engine):
    def __init__(self, cpu_only):
        super().__init__()
        self.detector = FasterRCNNOpenCVDetector(
            proto_path = PROTOTXT,
            model_path = CAFFEMODEL,
            labels = _get_labels(),
            gpu = not cpu_only
        )

    def handle(self, from_client):
        if from_client.payload_type != gabriel_pb2.PayloadType.IMAGE:
            return cognitive_engine.wrong_input_format_error(
                from_client.frame_id)

        engine_fields = cognitive_engine.unpack_engine_fields(
            instruction_pb2.EngineFields, from_client)

        img_array = np.asarray(bytearray(from_client.payload), dtype=np.int8)
        img = cv2.imdecode(img_array, -1)

        objects = []
        if max(img.shape) > IMAGE_MAX_WH:
            resize_ratio = float(IMAGE_MAX_WH) / max(img.shape[0], img.shape[1])
            img = cv2.resize(img, (0, 0), fx=resize_ratio, fy=resize_ratio,
                             interpolation=cv2.INTER_AREA)
            objects = self.detector.detect(img)
            if objects is not None:
                objects[:, :4] /= resize_ratio
        else:
            objects = self.detector.detect(img)
        logger.info("object detection result: %s", objects)

        # obtain client headers
        headers = {}
        vis_objects, instruction = self.task.get_instruction(objects, headers)

        # return results
        engine_fields.update_count += 1
        result_wrapper = gabriel_pb2.ResultWrapper()
        result_wrapper.engine_fields.Pack(engine_fields)

        result = gabriel_pb2.ResultWrapper.Result()
        result.payload_type = gabriel_pb2.PayloadType.IMAGE
        result.engine_name = ENGINE_NAME
        with open(image_path, 'rb') as f:
            result.payload = f.read()
        result_wrapper.results.append(result)

        result = gabriel_pb2.ResultWrapper.Result()
        result.payload_type = gabriel_pb2.PayloadType.TEXT
        result.engine_name = ENGINE_NAME
        result.payload = instruction.encode(encoding="utf-8")
        result_wrapper.results.append(result)

        result_wrapper.status = gabriel_pb2.ResultWrapper.Status.SUCCESS

        return result_wrapper

class RiblocEngineOld(gabriel.proxy.CognitiveProcessThread):

    def __init__(self, image_queue, output_queue, engine_id, init_state=None):
        super().__init__(image_queue, output_queue, engine_id)
        self.is_first_image = True
        self.first_n_cnt = 0
        self.last_msg = ""
        self.dup_msg_cnt = 0
        # task initialization
        self.task = task.Task(init_state=init_state)

    def add_to_byte_array(self, byte_array, extra_bytes):
        return struct.pack("!{}s{}s".format(len(byte_array), len(extra_bytes)), byte_array, extra_bytes)

    def add_output_item(self, header, data, itm_header_key, itm_data):
        header[itm_header_key] = (len(data), len(itm_data))
        return self.add_to_byte_array(data, itm_data)

    def gen_output(self, header, img, speech):
        rtn_data = ""
        if img is not None:
            _, buf = cv2.imencode(".jpg", img)
            rtn_data = self.add_output_item(header,
                                            rtn_data,
                                            gabriel.Protocol_result.JSON_KEY_IMAGE,
                                            buf.tobytes())
        if speech is not None:
            rtn_data = self.add_output_item(header,
                                            rtn_data,
                                            gabriel.Protocol_result.JSON_KEY_SPEECH,
                                            speech)
        return rtn_data

    @staticmethod
    def rotate_90(img):
        rows, cols, _ = img.shape
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), -90, 1)
        dst = cv2.warpAffine(img, M, (cols, rows))
        return dst

    def handle(self, header, data):
        # PERFORM Cognitive Assistance Processing
        LOG.info("processing: ")
        LOG.info("%s\n" % header)

        rtn_data = {}

        if self.first_n_cnt < 10:
            header['status'] = 'success'
            # rtn_data = self.gen_output(header, None, None)
            self.first_n_cnt += 1
            return json.dumps(rtn_data)

        ## preprocessing of input image
        img = util.raw2cv_image(data)
        if config.ROTATE_IMAGE:
            img = self.rotate_90(img)
        if config.RESIZE_IMAGE:
            img = cv2.resize(img, (720, 480))

        _, objects = caffe_detect.detect_object(img)
        LOG.info("object detection result: %s" % objects)

        ## get instruction based on state
        vis_objects, instruction = self.task.get_instruction(objects, header)
        print('cur state: {}'.format(self.task.current_state))
        header['status'] = 'success'

        if instruction['speech'] is not None:
            if instruction['speech'] == self.last_msg:
                print('duplicate speech')
                self.dup_msg_cnt += 1
                if self.dup_msg_cnt < 100:
                    return json.dumps(rtn_data)
                else:
                    self.dup_msg_cnt = 0
            self.last_msg = instruction['speech']

        if instruction.get('image', None) is not None:
            rtn_data['image'] = b64encode(util.cv_image2raw(instruction['image']))
        if instruction.get('speech', None) is not None:
            rtn_data['speech'] = instruction['speech']

        if len(vis_objects) > 0:
            print('visualizing: {}'.format(vis_objects))
        if config.VISUALIZE_ALL:
            vis_objects = objects
        img_object = util.vis_detections(img, vis_objects, config.LABELS)
        return json.dumps(rtn_data)
