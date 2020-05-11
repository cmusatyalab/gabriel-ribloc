#!/usr/bin/env python
#
# Cloudlet Infrastructure for Mobile Computing
#   - Task Assistance
#
#   Author: Junjue Wang <junjuew@cs.cmu.edu>
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
import sys

import cv2
import numpy as np

from gabriel_protocol import gabriel_pb2
from gabriel_server import cognitive_engine
from logzero import logger

from . import config, instruction_pb2, util, task
from .object_detect import FasterRCNNOpenCVDetector


class RiblocEngine(cognitive_engine.Engine):
    def __init__(self, cpu_only):
        super().__init__()
        self.detector = FasterRCNNOpenCVDetector(
            proto_path=config.PROTOTXT,
            model_path=config.CAFFEMODEL,
            labels=config.LABELS,
            gpu=not cpu_only
        )
        self.task = task.Task()

    def _serialize_to_pb(self, headers, instruction, engine_fields):
        engine_fields.update_count += 1
        if 'clear_color' in headers:
            engine_fields.ribloc.clear_color = headers['clear_color']
        result_wrapper = gabriel_pb2.ResultWrapper()
        result_wrapper.engine_fields.Pack(engine_fields)

        if 'image' in instruction and instruction['image'] is not None:
            result = gabriel_pb2.ResultWrapper.Result()
            result.payload_type = gabriel_pb2.PayloadType.IMAGE
            result.engine_name = config.ENGINE_NAME
            result.payload = util.cv_image2raw(instruction['image'])
            result_wrapper.results.append(result)

        if 'speech' in instruction and instruction['speech'] is not None:
            result = gabriel_pb2.ResultWrapper.Result()
            result.payload_type = gabriel_pb2.PayloadType.TEXT
            result.engine_name = config.ENGINE_NAME
            result.payload = instruction['speech'].encode(encoding="utf-8")
            result_wrapper.results.append(result)

        result_wrapper.status = gabriel_pb2.ResultWrapper.Status.SUCCESS
        return result_wrapper

    def handle(self, from_client):
        if from_client.payload_type != gabriel_pb2.PayloadType.IMAGE:
            return cognitive_engine.wrong_input_format_error(
                from_client.frame_id)

        engine_fields = cognitive_engine.unpack_engine_fields(
            instruction_pb2.EngineFields, from_client)

        img_array = np.asarray(bytearray(from_client.payload), dtype=np.int8)
        img = cv2.imdecode(img_array, -1)

        objects = []
        if max(img.shape) > config.IMAGE_MAX_WH:
            resize_ratio = float(config.IMAGE_MAX_WH) / max(img.shape[0], img.shape[1])
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
        if engine_fields.ribloc.gauge_color:
            headers['gaugeColor'] = str(engine_fields.ribloc.gauge_color)
            logger.debug("received gaugeColor to be: %s", headers['gaugeColor'])
        vis_objects, instruction = self.task.get_instruction(objects, header=headers)
        result_wrapper = self._serialize_to_pb(headers, instruction, engine_fields)
        logger.info("result_wrapper: {}".format(result_wrapper))
        return result_wrapper
