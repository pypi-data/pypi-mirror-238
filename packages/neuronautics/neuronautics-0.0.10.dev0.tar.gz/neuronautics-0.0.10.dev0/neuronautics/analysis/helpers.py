import numpy as np
import pandas as pd


def to_timeseries(data: pd.DataFrame, group_lvl:str, bin_ms: int = 100) -> pd.DataFrame:
    """
    Binarize a time series of events based on a specified bin size.

    This function takes a DataFrame containing timestamped events and
    converts it into a binarized time series. Each event is assigned to a
    bin, and within each bin, a binary array is created to represent the
    presence or absence of events. The resulting time series is grouped by
    a specified grouping level.

    Args:
        data (DataFrame): A DataFrame containing timestamped events.
        group_lvl (str): The column name used for grouping the time series.
        bin_ms (int, optional): The time window (in milliseconds) for binning
            the events. Default is 100 ms.

    Returns:
        DataFrame: A DataFrame containing the binarized time series with
            columns 'group_lvl' and 'events', where 'events' contains binary
            arrays representing event occurrences within each bin.

    Example:
        Given input data like this:

        ```
          ts_ms  channel_id
        0    100           1
        1    200           2
        2    300           1
        3    400           3
        4    500           2
        ```

        Calling `to_timeseries(data, 'channel_id', bin_ms=100)` would produce
        the following output:

        ```
          channel_id                        events
        0           1  [1, 1, 0, 0, 0]
        1           2  [0, 0, 1, 0, 1]
        2           3  [1, 0, 0, 0, 0]
        ```

    """
    data['bin'] = (data['ts_ms'] // bin_ms).astype(int)
    end_time = data['bin'].max()

    bin_df = data.groupby(group_lvl)['bin'].agg(list).reset_index()
    def _to_timeseries(events):
        bin = np.zeros(end_time + 1)
        bin[events] = 1
        return bin

    bin_df['events'] = bin_df.bin.map(_to_timeseries)
    return bin_df



