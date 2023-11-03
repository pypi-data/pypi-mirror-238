#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 09:21:01 2023

@author: mike
"""
import io
import pandas as pd
import numpy as np


#######################################################
### Helper functions


class PdSerial:
    def dumps(obj):
        b1 = io.BytesIO()
        obj.reset_index().to_feather(b1)
        b1.seek(0)
        return b1.read()
    def loads(obj):
        b1 = io.BytesIO(memoryview(obj))
        out = pd.read_feather(b1)
        return out.set_index('time')


def grp_ts_agg(df, grp_col, ts_col, freq_code, agg_fun, discrete=False, **kwargs):
    """
    Simple function to aggregate time series with dataframes with a single column of stations and a column of times.

    Parameters
    ----------
    df : DataFrame
        Dataframe with a datetime column.
    grp_col : str, list of str, or None
        Column name that contains the stations.
    ts_col : str
        The column name of the datetime column.
    freq_code : str
        The pandas frequency code for the aggregation (e.g. 'M', 'A-JUN').
    discrete : bool
        Is the data discrete? Will use proper resampling using linear interpolation.

    Returns
    -------
    Pandas DataFrame
    """

    df1 = df.copy()
    if isinstance(df, pd.DataFrame):
        if df[ts_col].dtype.name == 'datetime64[ns]':
            df1.set_index(ts_col, inplace=True)
            if (grp_col is None) or (not grp_col):

                if discrete:
                    df3 = discrete_resample(df1, freq_code, agg_fun, True, **kwargs)
                    df3.index.name = 'time'
                else:
                    df3 = df1.resample(freq_code, **kwargs).agg(agg_fun)

                return df3

            elif isinstance(grp_col, str):
                grp_col = [grp_col]
            elif isinstance(grp_col, list):
                grp_col = grp_col[:]
            else:
                raise TypeError('grp_col must be a str, list, or None')

            if discrete:
                val_cols = [c for c in df1.columns if c not in grp_col]

                grp1 = df1.groupby(grp_col)

                grp_list = []

                for i, r in grp1:
                    s6 = discrete_resample(r[val_cols], freq_code, agg_fun, True, **kwargs)
                    s6[grp_col] = i

                    grp_list.append(s6)

                df2 = pd.concat(grp_list)
                df2.index.name = ts_col

                df3 = df2.reset_index().set_index(grp_col + [ts_col]).sort_index()

            else:
                grp_col.extend([pd.Grouper(level=ts_col, freq=freq_code, **kwargs)])
                df3 = df1.groupby(grp_col).agg(agg_fun)

            return df3

        else:
            raise ValueError('Make one column a timeseries!')
    else:
        raise TypeError('The object must be a DataFrame')


def discrete_resample(df, freq_code, agg_fun, remove_inter=False, **kwargs):
    """
    Function to properly set up a resampling class for discrete data. This assumes a linear interpolation between data points.

    Parameters
    ----------
    df: DataFrame or Series
        DataFrame or Series with a time index.
    freq_code: str
        Pandas frequency code. e.g. 'D'.
    agg_fun : str
        The aggregation function to be applied on the resampling object.
    **kwargs
        Any keyword args passed to Pandas resample.

    Returns
    -------
    Pandas DataFrame or Series
    """
    if isinstance(df, (pd.Series, pd.DataFrame)):
        if isinstance(df.index, pd.DatetimeIndex):
            reg1 = pd.date_range(df.index[0].ceil(freq_code), df.index[-1].floor(freq_code), freq=freq_code)
            reg2 = reg1[~reg1.isin(df.index)]
            if isinstance(df, pd.Series):
                s1 = pd.Series(np.nan, index=reg2)
            else:
                s1 = pd.DataFrame(np.nan, index=reg2, columns=df.columns)
            s2 = pd.concat([df, s1]).sort_index()
            s3 = s2.interpolate('time')
            s4 = (s3 + s3.shift(-1))/2
            s5 = s4.resample(freq_code, **kwargs).agg(agg_fun).dropna()

            if remove_inter:
                index1 = df.index.floor(freq_code).unique()
                s6 = s5[s5.index.isin(index1)].copy()
            else:
                s6 = s5
        else:
            raise ValueError('The index must be a datetimeindex')
    else:
        raise TypeError('The object must be either a DataFrame or a Series')

    return s6


def create_shifted_df(series, from_range, to_range, freq_code, agg_fun, ref_name, include_0=False, discrete=False, **kwargs):
    """

    """
    if not isinstance(series, pd.Series):
        raise TypeError('series must be a pandas Series.')
    if not isinstance(series.index, pd.DatetimeIndex):
        raise TypeError('The series index must be a pandas DatetimeIndex.')

    df = series.reset_index()
    data_col = df.columns[1]
    ts_col = df.columns[0]
    s2 = grp_ts_agg(df, None, ts_col, freq_code, agg_fun, discrete, **kwargs)[data_col]

    if include_0:
        f_hours = list(range(from_range-1, to_range+1))
        f_hours[0] = 0
    else:
        f_hours = list(range(from_range, to_range+1))

    df_list = []
    for d in f_hours:
        n1 = s2.shift(d, freq_code)
        n1.name = ref_name + '_' + str(d)
        df_list.append(n1)
    data = pd.concat(df_list, axis=1).dropna()

    return data




















































