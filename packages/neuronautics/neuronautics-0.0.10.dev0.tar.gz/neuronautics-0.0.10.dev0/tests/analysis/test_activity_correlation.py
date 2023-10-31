import unittest
from unittest.mock import patch
from neuronautics.analysis.activity_correlation import ActivityCorrelation
import pandas as pd
import numpy as np


class TestActivityCorrelation(unittest.TestCase):
    def test_get_input_params(self):
        ac = ActivityCorrelation()
        params = ac.get_input_params()

        for param in params:
            self.assertTrue(param['default'] <= param['max'])
            self.assertTrue(param['min'] <= param['default'])
            self.assertTrue('name' in param)
            self.assertTrue('type' in param)

    def test_run(self):
        spikes = pd.DataFrame({'class': [0, 0, 0, 0, 0, 0, 0, 0],
                               'channel_id': [0, 0, 0, 0, 1, 1, 1, 1],
                               'ts_ms': [1, 2, 3, 4, 1, 2, 3, 4]})
        expected_correlation = np.array([[False, True], [True, False]])

        ac = ActivityCorrelation()
        output = ac.run(spikes, 1, 0.5)

        np.testing.assert_array_equal(expected_correlation, output)

    def test_plot(self):
        """parent plot is called with the plot title set"""
        with patch('neuronautics.analysis.activity_correlation.super') as spy_super:
            ac = ActivityCorrelation()
            ac.plot()
            spy_super().plot.assert_called_once_with('Activity Correlation')



if __name__ == '__main__':
    unittest.main()
