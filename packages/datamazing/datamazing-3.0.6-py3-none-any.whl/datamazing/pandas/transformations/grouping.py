import typing

import pandas as pd

from datamazing._conform import _concat, _list
from datamazing.pandas.transformations import resampling


class GrouperResampler:
    def __init__(
        self,
        gb: "Grouper",
        on: str,
        resolution: pd.Timedelta,
    ):
        self.gb = gb
        self.on = on
        self.resolution = resolution

    def agg(self, method: str, edge: str = "left"):
        """Aggregate (downsample) time series.
        For example, if the input is a time series H with
        hourly resolution, then we can aggregate, using
        the mean, to daily resolution, and produce a new
        time series D. In other words:

            - Input:    H(hour)
            - Output:   D(day) = mean( H(hour) for hour in day)

        Args:
            method (str): Aggregation method ("mean", "sum", etc.)
            edge (str, optional): Which side of the interval
                to use as label ("left" or "right").
                Defaults to "left".
        """
        # to aggregate (downsample), the largest
        # time interval in the original series must
        # be smaller or equal to the specified resolution
        df = self.gb.df.sort_values(by=self.on)
        max_time_diff = df.groupby(self.gb.by)[self.on].diff().max()
        if max_time_diff > self.resolution:
            raise ValueError(
                f"Aggregation is not possible since the "
                f"downsample resolution '{self.resolution}' "
                f"is smaller than the largest time difference "
                f"in time series ('{max_time_diff}')"
            )

        df = (
            df.set_index(self.on)
            .groupby(self.gb.by, dropna=False)
            .resample(rule=self.resolution, closed=edge, label=edge)
            .aggregate(method, numeric_only=True)
        )

        # depending on the resampling aggregation
        # method, pandas will include the group-by
        # columns in both the index and the columns
        df = df.drop(columns=self.gb.by, errors="ignore")

        df = df.reset_index()

        return df

    def interpolate(self, method: str = "interpolate", irregular: bool = False):
        """Interpolate (upsample) time series.
        For example, if the input is a time series D with
        daily resolution, then we can interpolate, using
        a linear function, to hourly resolution, and
        produce a new time series H. In other words:

            - Input:    D(day)
            - Output:   H(hour) = interpolate(hour between day+0 and day+1)

        Args:
            method (str): Interpolation method ("interpolate" (meaning linear),
                "ffill", etc.)
        """
        # to interpolate (upsample), the smallest
        # time interval in the original series must
        # be larger or equal to the specified resolution
        df = self.gb.df.sort_values(by=self.on)
        if not irregular:
            min_time_diff = df.groupby(self.gb.by)[self.on].diff().min()
            if min_time_diff < self.resolution:
                raise ValueError(
                    f"Interpolation on regular time series "
                    f"not possible since the "
                    f"upsample resolution '{self.resolution}' "
                    f"is larger than the smallest time difference "
                    f"in time series ('{min_time_diff}')"
                )

        start_time = df[self.on].min()
        end_time = df[self.on].max()

        df = (
            df.set_index(self.on)
            .groupby(self.gb.by, dropna=False)
            .resample(rule=self.resolution)
            .aggregate(method)
        )

        # depending on the resampling aggregation
        # method, pandas will include the group-by
        # columns in both the index and the columns
        df = df.drop(columns=self.gb.by, errors="ignore")

        df = df.reset_index()

        # after resampling, pandas might leave
        # timestamps outside of the original interval
        if not df.empty:
            df = df[df[self.on].between(start_time, end_time)]

        return df

    def granulate(self, edge: str = "left"):
        """Fine-grain (upsample) time series.
        For example, if the input is a time series D with
        daily resolution, then we can granulate to hourly
        resolution, and produce a new time series H.
        In other words:

            - Input:    D(day)
            - Output:   H(hour) = D(day containing hour)


        Args:
            edge (str, optional): Which side of the interval
                to use as label ("left" or "right").
                Defaults to "left".
        """
        # pandas doesn't handle empty dataframes very well
        if self.gb.df.empty:
            return self.gb.df

        df = self.gb.df.groupby(self.gb.by, dropna=False, group_keys=False).apply(
            lambda group: resampling.resample(
                group, self.on, self.resolution
            ).granulate(edge)
        )

        return df


class Grouper:
    def __init__(self, df: pd.DataFrame, by: list[str]):
        self.df = df
        self.by = by

    def agg(self, method: str):
        if method == "sum":
            aggregate_options = {"numeric_only": "True"}
        else:
            aggregate_options = {}
        return (
            self.df.set_index(self.by)
            .groupby(self.by, dropna=False)
            .aggregate(method, **aggregate_options)
            .reset_index()
        )

    def resample(self, on: str, resolution: pd.Timedelta):
        return GrouperResampler(self, on, resolution)

    def pivot(self, on: list[str], values: typing.Optional[list[tuple[str]]] = None):
        """
        Pivot table. Non-existing combinations will be filled
        with NaNs.

        Args:
            on (list[str]): Columns which to pivot
            values (list[tuple[str]], optional): Enforce
                the existence of columns with these names
                after pivoting. Defaults to None, in which
                case the values will be inferred from the
                pivoting column.
        """

        df = self.df.set_index(_concat(self.by, on))

        if values:
            by_vals = df.index.to_frame(index=False)[_list(self.by)].drop_duplicates()
            on_vals = pd.DataFrame(values, columns=_list(on))
            cross_vals = by_vals.merge(on_vals, how="cross")
            df = df.reindex(pd.MultiIndex.from_frame(cross_vals))

        df = df.unstack(on)

        # concatenate multiindex columns to single index columns
        concat_cols = []
        suffix = len(df.columns.levels[0]) > 1
        for col in df.columns:
            concat_col = "_".join([str(item) for item in col[1:]])
            if suffix:
                # if more than one remaning columns, suffix with that
                concat_col = concat_col + "_" + str(col[0])
            concat_col = concat_col.strip("_")
            concat_cols.append(concat_col)
        df.columns = concat_cols

        return df.reset_index()

    def latest(self, on: str):
        return (
            self.df.set_index(_concat(self.by, on))
            .sort_index(level=on)
            .groupby(self.by, dropna=False)
            .tail(1)
            .reset_index()
        )

    def earliest(self, on: str):
        return (
            self.df.set_index(_concat(self.by, on))
            .sort_index(level=on)
            .groupby(self.by, dropna=False)
            .head(1)
            .reset_index()
        )


def group(df: pd.DataFrame, by: list[str]):
    return Grouper(df, by)
