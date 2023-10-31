from ..analysis.type.graph_analysis import GraphAnalysis
from ..analysis.helpers import to_timeseries
import numpy as np


class ActivityCorrelation(GraphAnalysis):
    """A class for performing activity correlation analysis.

    This class provides methods for analyzing the correlation of activity
    between different channels based on input spike data.

    Args:
        spikes (DataFrame): A DataFrame containing spike data.
        bin_window_ms (int): The time window (in milliseconds) for binning spikes.
        corr_thr (float): The correlation threshold for considering correlations.

    Attributes:
        spikes (DataFrame): The input spike data.
        bin_window_ms (int): The time window for binning spikes (in milliseconds).
        corr_thr (float): The correlation threshold.

    """

    def get_input_params(self):
        """Get the input parameters for the activity correlation analysis.

        Returns:
            list: A list of dictionaries, each describing an input parameter.
                Each dictionary includes 'name', 'min', 'max', 'default', and 'type' keys.

        """
        return [
            {'name': 'bin_window_ms', 'min': 1, 'max': 1_000, 'default': 100, 'type': 'int'},
            {'name': 'corr_thr', 'min': 0, 'max': 1, 'default': 0.3, 'type': 'float'}
        ]

    def run(self, spikes, bin_window_ms, corr_thr, *args, **kwargs):
        """Run the activity correlation analysis.

        Args:
            spikes (DataFrame): A DataFrame containing spike data.
            bin_window_ms (int): The time window (in milliseconds) for binning spikes.
            corr_thr (float): The correlation threshold for considering correlations.

        Returns:
            ndarray: A boolean matrix indicating correlations above the threshold.

        """
        spikes['class'] = spikes['class'].astype(int)
        spikes = spikes[spikes['class'] >= 0]  # remove noise
        spikes = spikes[['channel_id', 'ts_ms']].copy().reset_index(drop=True)

        bin_df = to_timeseries(spikes, group_lvl='channel_id', bin_ms=bin_window_ms)

        w_ij = np.zeros((120, 120))  # (len(bin_df), len(bin_df)))
        for i, (ch_id_i, bin_i, events_i) in bin_df.iterrows():
            max_i = events_i.sum()
            for j, (ch_id_j, bin_j, events_j) in bin_df.iterrows():
                max_j = events_j.sum()
                shift_0 = (events_i[:-1] * events_j[1:]).sum()
                shift_1 = (events_i[1:] * events_j[:-1]).sum()
                shift_2 = (events_i * events_j).sum()
                w_ij[ch_id_i, ch_id_j] = (shift_0 + shift_1 + shift_2) / (3 * max(max_i, max_j))
                w_ij[ch_id_i, ch_id_j] = 0 if ch_id_i == ch_id_j else w_ij[ch_id_i, ch_id_j]

        return w_ij > corr_thr
    
    def plot(self, *args, **kwargs):
        """Plot the activity correlation analysis.

        Args:
            *args: Variable-length positional arguments.
            **kwargs: Variable-length keyword arguments.

        Returns:
            object: matplotlib figure

        """
        return super().plot('Activity Correlation', *args, **kwargs)
