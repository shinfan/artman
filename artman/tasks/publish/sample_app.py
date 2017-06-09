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

from __future__ import absolute_import, unicode_literals
import functools
import os
import uuid

import github3

import six

from artman.tasks import task_base
from artman.utils.logger import logger

class _JavaSampleTask(task_base.TaskBase):
    def execute(self, gapic_code_dir=None, grpc_code_dir=None, proto_code_dir=None):
        
        if grpc_code_dir:
            self.exec_command(['cp', '-rf', grpc_code_dir, gapic_code_dir])
        else:
            raise Exception('GRPC package is not generated.')

        if proto_code_dir:
            self.exec_command(['cp', '-rf', proto_code_dir, gapic_code_dir])
        else:
            raise Exception('Proto package is not generated.')

        userhome = os.path.expanduser('~')
        gapic_loc = os.path.realpath(gapic_code_dir).replace(userhome, '~')
        logger.success('Sample client generated: {0}'.format(gapic_loc))
        self.exec_command([gapic_code_dir + '/gradlew', '-p', gapic_code_dir, 'jar'])
        logger.success('Jar file created: {0}/build/libs'.format(gapic_loc))

SAMPLE_TASK_DICT = {
    'java': _JavaSampleTask,
}

class SampleAppTask(task_base.TaskBase):
    """Create a sample GAPIC client that is ready to execute

    Args:
        language (str): The target language.
        gapic_code_dir (str): The current GAPIC code location, if any.
        grpc_code_dir (str): The current GRPC code location, if any.
        proto_code_dir (str): The current PROTO code location, if any.
    """
    def execute(self, language, gapic_code_dir=None, grpc_code_dir=None,
                proto_code_dir=None):
        if language in SAMPLE_TASK_DICT:
            task = SAMPLE_TASK_DICT[language]()
            return task.execute(gapic_code_dir=gapic_code_dir,
                                grpc_code_dir=grpc_code_dir,
                                proto_code_dir=proto_code_dir)
        else:
            ValueError('Sample app publish is not supported for %s.', language)


TASKS = (
    SampleAppTask,
)
