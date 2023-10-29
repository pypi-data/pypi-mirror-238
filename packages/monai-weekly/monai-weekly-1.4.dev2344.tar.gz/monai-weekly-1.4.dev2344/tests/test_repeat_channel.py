# Copyright (c) MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import unittest

from parameterized import parameterized

from monai.transforms import RepeatChannel
from tests.utils import TEST_NDARRAYS

TESTS = []
for p in TEST_NDARRAYS:
    TESTS.append([{"repeats": 3}, p([[[0, 1], [1, 2]]]), (3, 2, 2)])


class TestRepeatChannel(unittest.TestCase):
    @parameterized.expand(TESTS)
    def test_shape(self, input_param, input_data, expected_shape):
        result = RepeatChannel(**input_param)(input_data)
        self.assertEqual(result.shape, expected_shape)


if __name__ == "__main__":
    unittest.main()
