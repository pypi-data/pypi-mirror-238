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

import numpy as np
from parameterized import parameterized

from monai.transforms import get_extreme_points
from tests.utils import TEST_NDARRAYS

TESTS = []
for p in TEST_NDARRAYS:
    TESTS.append(
        [
            {
                "img": p(np.array([[0, 1, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0]])),
                "rand_state": np.random,
                "background": 0,
                "pert": 0.0,
            },
            [(0, 1), (3, 0), (3, 0), (1, 2)],
        ]
    )

    TESTS.append(
        [
            {
                "img": p(np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0], [0, 1, 0]])),
                "rand_state": np.random,
                "background": 0,
                "pert": 0.0,
            },
            [(0, 1), (3, 1), (1, 0), (1, 2)],
        ]
    )


class TestGetExtremePoints(unittest.TestCase):
    @parameterized.expand(TESTS)
    def test_type_shape(self, input_data, expected):
        result = get_extreme_points(**input_data)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
