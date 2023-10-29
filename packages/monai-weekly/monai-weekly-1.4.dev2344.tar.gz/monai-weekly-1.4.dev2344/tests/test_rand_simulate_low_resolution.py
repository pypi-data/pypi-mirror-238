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

from monai.transforms import RandSimulateLowResolution
from tests.utils import TEST_NDARRAYS, assert_allclose

TESTS = []
for p in TEST_NDARRAYS:
    TESTS.append(
        [
            dict(prob=1.0, zoom_range=(0.8, 0.81)),
            p(
                np.array(
                    [
                        [
                            [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]],
                            [[16, 17, 18, 19], [20, 21, 22, 23], [24, 25, 26, 27], [28, 29, 30, 31]],
                            [[32, 33, 34, 35], [36, 37, 38, 39], [40, 41, 42, 43], [44, 45, 46, 47]],
                            [[48, 49, 50, 51], [52, 53, 54, 55], [56, 57, 58, 59], [60, 61, 62, 63]],
                        ]
                    ]
                )
            ),
            np.array(
                [
                    [
                        [
                            [0.0000, 0.6250, 1.3750, 2.0000],
                            [2.5000, 3.1250, 3.8750, 4.5000],
                            [5.5000, 6.1250, 6.8750, 7.5000],
                            [8.0000, 8.6250, 9.3750, 10.0000],
                        ],
                        [
                            [10.0000, 10.6250, 11.3750, 12.0000],
                            [12.5000, 13.1250, 13.8750, 14.5000],
                            [15.5000, 16.1250, 16.8750, 17.5000],
                            [18.0000, 18.6250, 19.3750, 20.0000],
                        ],
                        [
                            [22.0000, 22.6250, 23.3750, 24.0000],
                            [24.5000, 25.1250, 25.8750, 26.5000],
                            [27.5000, 28.1250, 28.8750, 29.5000],
                            [30.0000, 30.6250, 31.3750, 32.0000],
                        ],
                        [
                            [32.0000, 32.6250, 33.3750, 34.0000],
                            [34.5000, 35.1250, 35.8750, 36.5000],
                            [37.5000, 38.1250, 38.8750, 39.5000],
                            [40.0000, 40.6250, 41.3750, 42.0000],
                        ],
                    ]
                ]
            ),
        ]
    )


class TestRandGaussianSmooth(unittest.TestCase):
    @parameterized.expand(TESTS)
    def test_value(self, arguments, image, expected_data):
        randsimlowres = RandSimulateLowResolution(**arguments)
        randsimlowres.set_random_state(seed=0)
        result = randsimlowres(image)
        assert_allclose(result, expected_data, rtol=1e-4, type_test="tensor")


if __name__ == "__main__":
    unittest.main()
