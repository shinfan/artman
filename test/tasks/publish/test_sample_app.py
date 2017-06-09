# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import os
import unittest

import mock

from artman.tasks.publish import sample_app
from artman.utils.logger import logger


class SampleAppTests(unittest.TestCase):
    @mock.patch.object(sample_app._JavaSampleTask, 'exec_command')
    @mock.patch('os.path.isdir')
    def test_execute(self, is_dir, exec_command):
        is_dir.return_value = True
        # Run the task.
        task = sample_app._JavaSampleTask()
        task.execute(
            gapic_code_dir='~/foo/bar/gapic',
            grpc_code_dir='~/foo/bar/grpc',
            proto_code_dir='~/foo/bar/proto',
        )

        # Ensure we executed the commands we expect.
        assert exec_command.call_count == 3
        _, cp_cmd, _ = exec_command.mock_calls[0]
        assert cp_cmd[0] == ['cp', '-rf', '~/foo/bar/grpc', '~/foo/bar/gapic']
        _, cp_cmd_2, _ = exec_command.mock_calls[1]
        assert cp_cmd_2[0] == ['cp', '-rf', '~/foo/bar/proto', '~/foo/bar/gapic']
        _, build_cmd, _ = exec_command.mock_calls[2]
        assert build_cmd[0] == ['~/foo/bar/gapic/gradlew', '-p', '~/foo/bar/gapic', 'jar']
