import unittest
from neuronautics.analysis.helpers import to_timeseries
import pandas as pd
import numpy as np


class TestHelpers(unittest.TestCase):

    def test_to_timeseries(self):
        # Create sample data
        data = pd.DataFrame({
            'ts_ms': [100, 200, 300, 400, 500],
            'channel_id': [1, 2, 1, 3, 2]
        })

        group_lvl = 'channel_id'
        bin_ms = 100

        result = to_timeseries(data, group_lvl, bin_ms)

        expected_result = pd.DataFrame(
            {'channel_id': [1, 2, 3],
             'bin': [[1, 3], [2, 5], [4]],
             'events': [[0., 1., 0., 1., 0., 0.],
                        [0., 0., 1., 0., 0., 1.],
                        [0., 0., 0., 0., 1., 0.]]}
        )

        pd.testing.assert_frame_equal(expected_result, result)


if __name__ == '__main__':
    unittest.main()
