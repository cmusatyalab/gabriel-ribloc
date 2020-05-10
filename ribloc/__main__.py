#!/usr/bin/env python3
#
# Cloudlet Infrastructure for Mobile Computing
#   - Task Assistance
#
#   Author: Junjue Wang <junjuew@cs.cmu.edu>
#
#   Copyright (C) 2011-2019 Carnegie Mellon University
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
import fire
from gabriel_server.local_engine import runner

from ribloc import ENGINE_NAME, RiblocEngine

DEFAULT_PORT = 9099
DEFAULT_NUM_TOKENS = 1
INPUT_QUEUE_MAX_SIZE = 60


def main(tokens=DEFAULT_NUM_TOKENS, port=DEFAULT_PORT, use_gpu=True):
    def engine_setup():
        return RiblocEngine(use_gpu)

    runner.run(
        engine_setup, ENGINE_NAME, INPUT_QUEUE_MAX_SIZE, port, tokens)


if __name__ == "__main__":
    fire.Fire(main)
