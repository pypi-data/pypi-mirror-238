#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 09:20:48 2023

@author: mike
"""
import io
import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split, cross_validate, cross_val_score
import booklet
from typing import List
import skops.io as sio
import matplotlib.pyplot as plt
import orjson
import copy
import xarray as xr

# import utils
from . import utils

#################################################
### Parameters



#################################################
### Main class


class FloodGB:
    """

    """
    def __init__(self, path=None, load_model_data=False):
        """

        """
        if path is not None:
            with booklet.open(path) as f:
                self.base_model = sio.loads(f['base_model'], True)

                self.params = orjson.loads(f['params'])

                models = {}
                if self.params['n_models'] > 1:
                    for i in range(1, self.params['n_models'] + 1):
                        models[i] = sio.loads(f[str(i)], True)
                else:
                    models[0] = sio.loads(f[str(0)], True)

                self.models = models

                if load_model_data:
                    self.input_data = utils.PdSerial.loads(f['input_data'])


    def set_params(self, feature_stns: List[str], target_stn: str, freq: str, lags: dict):
        """

        """
        feature_lags = {}
        for col in feature_stns:
            if col not in lags:
                raise ValueError('{col} is not in the lags dict'.format(col=col))

            lag_start, lag_end, agg = lags[col]

            if (not isinstance(lag_start, int)) or (not isinstance(lag_end, int)) or (agg not in ('sum', 'mean')):
                raise TypeError('lags must be a tuple or list of integers and an aggregation method at the end.')

            feature_lags[col] = (lag_start, lag_end, agg)

        if target_stn in feature_lags:
            n_models = feature_lags[target_stn][0]
        else:
            n_models = 1

        self.params = {'freq': freq, 'feature_stns': feature_stns, 'target_stn': target_stn, 'feature_lags': feature_lags, 'n_models': n_models, 'break_time': None, 'input_data': {}}


    def set_model(self, model):
        """

        """
        self.base_model = model


    def _check_data(self, data: xr.Dataset):
        """

        """
        ## structural checks
        if not all([var in data for var in ['time', 'station_id']]):
            raise ValueError('time and station_id must be in the Dataset.')
        if 'datetime64' not in data.time.dtype.name:
            raise TypeError('The index of data must be a numpy datetime64.')

        ## Determine main variable/parameter
        variable = None
        for var in data.data_vars:
            attrs = data[var].attrs
            if 'dataset_id' in attrs:
                variable = var

        if variable is None:
            raise ValueError('No variable was found with dataset_id in the attrs.')

        ## Check that all feature_stns and target_stn are in dataset
        all_stns = set(self.params['feature_stns'])
        all_stns.add(self.params['target_stn'])

        data_stns = data.station_id.values

        if not np.in1d(list(all_stns), data_stns).any():
            raise ValueError('No stations in feature_stns/target_stn are in the data.')

        filter_stns = data_stns[np.in1d(data_stns, list(all_stns))]

        if 'height' in data:
            data1 = data.where(data.station_id.isin(filter_stns), drop=True).isel(height=0, drop=True).copy()
        else:
            data1 = data.where(data.station_id.isin(filter_stns), drop=True).copy()

        freq = pd.infer_freq(data1.time[-3:])
        if freq is None:
            freq = pd.infer_freq(data1.time[:3])

        if freq is None:
            raise ValueError('Could not infer frequency. Please assign.')

        if hasattr(self, 'params'):
            model_freq = self.params['freq']
            if model_freq != freq:
                raise ValueError(f'model freq is {model_freq} and data freq is {freq}.')
        else:
            raise ValueError('Run the set_params method before this method.')

        return data1, variable


    def _to_dataframe(self, data, variable):
        """

        """
        df1 = data[['station_id', variable]].to_dataframe().reset_index()
        if 'geometry' in df1:
            df1.drop('geometry', axis=1, inplace=True)
        df2 = df1.set_index(['station_id', 'time'])[variable].unstack(0)

        return df2


    def load_input_data(self, data_list: List[xr.Dataset]):
        """

        """
        df_list = []
        for data in data_list:
            data1, variable = self._check_data(data)
            df1 = self._to_dataframe(data1, variable)
            df_list.append(df1)

        df2 = pd.concat(df_list, axis=1)
        self.input_data = df2


    def _load_features(self, input_data: pd.DataFrame):
        """

        """
        features_df = input_data[self.params['feature_stns']].copy()

        return features_df


    def _load_target(self, input_data: pd.DataFrame):
        """

        """
        target_df = input_data[self.params['target_stn']].copy()

        return target_df


    def _split_train_test(self, features_df, target_df, break_time):
        """

        """
        all_df = pd.concat([features_df, target_df], axis=1).dropna()

        if break_time is not None:
            break_time1 = pd.Timestamp(break_time)
            train_df = all_df.loc[:break_time1].copy()
            test_features = all_df.loc[break_time1:].iloc[:, :-1].copy()
            test_targets = all_df.loc[break_time1:].iloc[:, -1].copy()
        else:
            train_df = all_df
            test_features = all_df.iloc[:, :-1].copy()
            test_targets = all_df.iloc[:, -1].copy()

        test_targets.name = 'Actual flow'

        train_target_df = train_df.iloc[:, -1].copy()
        train_features_df = train_df.iloc[:, :-1].copy()

        return train_features_df, train_target_df, test_features, test_targets


    def _iter_features(self, features_df, time_steps=None):
        """

        """
        model_freq = self.params['freq']
        target_col = self.params['target_stn']

        if target_col in features_df:
            feature_lags = copy.deepcopy(self.params['feature_lags'])
            fore_len, target_period, target_agg = feature_lags.pop(target_col)

            feature_list = []
            for col, lag in feature_lags.items():
                lag_start, lag_end, agg = lag
                data0 = utils.create_shifted_df(features_df[col], lag_start, lag_end, model_freq, agg, col)
                feature_list.append(data0)

            for i in range(1, fore_len+1):
                if time_steps is not None:
                    if i not in time_steps:
                        continue
                fl1 = copy.deepcopy(feature_list)
                data1 = utils.create_shifted_df(features_df[target_col], i, i + target_period - 1, model_freq, target_agg, target_col)
                fl1.append(data1)

                model_features_df = pd.concat(fl1, axis=1)

                yield i, model_features_df

        else:
            feature_list = []
            for col, lag in self.params['feature_lags'].items():
                lag_start, lag_end, agg = lag
                data0 = utils.create_shifted_df(features_df[col], lag_start, lag_end, model_freq, agg, col)
                feature_list.append(data0)

            model_features_df = pd.concat(feature_list, axis=1)

            yield 0, model_features_df


    def train_models(self, data_list: List[xr.Dataset]=None, break_time=None):
        """

        """
        ## Prep input data
        if data_list is None:
            if not hasattr(self, 'input_data'):
                raise ValueError("data_list must be passed if input_data doesn't already exist.")
        else:
            self.load_input_data(data_list)

        features_df = self._load_features(self.input_data)
        target_df = self._load_target(self.input_data)

        model_dict = {}
        for i, model_features_df in self._iter_features(features_df):
            print(i)

            train_features_df, train_target_df, test_features, test_targets = self._split_train_test(model_features_df, target_df, break_time)

            new_model = copy.deepcopy(self.base_model)

            new_model.fit(train_features_df, train_target_df)
            model_dict[i] = new_model

        self.models = model_dict
        self.params['break_time'] = break_time


    def test_models(self, model_nums: list=None):
        """

        """
        if not isinstance(model_nums, list):
            model_nums = self.models.keys()

        features_df = self._load_features(self.input_data)
        target_df = self._load_target(self.input_data)

        hf_results_list = []
        max_data_list = []
        all_results_list = []
        predict_list = []
        for i, model_features_df in self._iter_features(features_df, model_nums):
            print(i)

            train_features_df, train_target_df, test_features, test_targets = self._split_train_test(model_features_df, target_df, self.params['break_time'])

            model = self.models[i]
            predictions1 = model.predict(test_features)
            predict1 = pd.Series(predictions1, index=test_features.index, name='Predicted flow')

            combo1 = pd.concat([test_targets, predict1], axis=1)

            combo2 = combo1.reset_index()
            combo2['model'] = i
            predict_list.append(combo2)

            ### Process results

            ## Use only high flow points
            max_index = argrelextrema(test_targets.values, np.greater, order=12)[0]

            upper_index = np.where(test_targets.values > np.percentile(test_targets.values, 80))[0]

            test_labels_index = max_index[np.in1d(max_index, upper_index)]

            max_data = combo1.iloc[test_labels_index]

            max_data2 = max_data.reset_index()
            max_data2['model'] = i
            max_data_list.append(max_data2)

            ## Estimate accuracy/errors
            p1 = max_data.iloc[:, 1].values
            a1 = max_data.iloc[:, 0].values

            mape = np.mean(np.abs(1 - p1/a1)) * 100
            bias = np.mean(1 - p1/a1) * 100

            hf_results_list.append([i, mape, bias])

            # Print out the mean absolute error (mae)
            # print('Mean Absolute Error:', round(np.mean(errors), 2), 'm3/s.')
            # print('Mean Error (Bias):', round(np.mean(bias_errors), 2), 'm3/s.')

            # Calculate mean absolute percentage error (MAPE)
            # print('MANE:', round(mape, 2), '%.')

            # print('MNE:', round(bias, 2), '%.')

            ## Use all data
            p1 = combo1.iloc[:, 1].values
            a1 = combo1.iloc[:, 0].values

            mape = np.mean(np.abs(1 - p1/a1)) * 100
            bias = np.mean(1 - p1/a1) * 100

            all_results_list.append([i, mape, bias])

        hf_results = pd.DataFrame(hf_results_list, columns=['model', 'MAPE', 'bias_perc']).set_index('model')
        all_results = pd.DataFrame(all_results_list, columns=['model', 'MAPE', 'bias_perc']).set_index('model')
        max_results = pd.concat(max_data_list).set_index(['model', 'time'])
        predict2 = pd.concat(predict_list).set_index(['model', 'time'])

        self.test_results_high_flow = hf_results
        self.test_results_all_flows = all_results
        self.test_max_flows = max_results
        self.test_predictions = predict2

        return all_results, hf_results, max_results, predict2


    def importances(self, n_repeats=3, random_state=0, model_nums: list=None):
        """

        """
        if not isinstance(model_nums, list):
            model_nums = self.models.keys()

        features_df = self._load_features(self.input_data)
        target_df = self._load_target(self.input_data)

        results_list = []
        for i, model_features_df in self._iter_features(features_df, model_nums):
            print(i)

            model = self.models[i]

            train_features_df, train_target_df, test_features, test_targets = self._split_train_test(model_features_df, target_df, self.params['break_time'])

            r = permutation_importance(model, test_features, test_targets, n_repeats=n_repeats, random_state=n_repeats)

            important0 = pd.DataFrame({'importances_mean': r.importances_mean, 'importances_std': r.importances_std}, index=test_features.columns).sort_values('importances_mean', ascending=False)

            important0.index.name = 'station'
            importances2 = important0['importances_mean'].reset_index().copy()
            importances2['time_step'] = importances2.station.apply(lambda x: x.split('_')[1]).astype('int16')
            importances2['station'] = importances2.station.apply(lambda x: x.split('_')[0])
            importances2['model'] = i
            importances4 = importances2.sort_values(['station', 'importances_mean'], ascending=False).set_index(['model', 'station', 'time_step']).copy()
            results_list.append(importances4)

        results = pd.concat(results_list)

        return results


    def cross_validation(self, n_cv_folds=5, scoring='neg_mean_absolute_percentage_error', model_nums: list=None):
        """

        """
        if not isinstance(model_nums, list):
            model_nums = self.models.keys()

        features_df = self._load_features(self.input_data)
        target_df = self._load_target(self.input_data)

        results_list = []
        for i, model_features_df in self._iter_features(features_df, model_nums):
            print(i)

            model = self.models[i]

            train_features_df, train_target_df, test_features, test_targets = self._split_train_test(model_features_df, target_df, None)

            native_result = cross_val_score(model, test_features, test_targets, cv=n_cv_folds, scoring=scoring)

            mean_score = np.abs(native_result).mean()
            # sd_score = np.abs(native_result).std()

            # print('MANE cross-val:', round(mean_score * 100, 1), '%')
            # print('STDEV cross-val:', round(sd_score * 100, 1), '%')

            results_list.append([i, mean_score])

        results = pd.DataFrame(results_list, columns=['model', scoring]).set_index('model')

        return results


    def predict(self, data_list: List[xr.Dataset]):
        """

        """
        if not hasattr(self, 'models'):
            raise ValueError('models have not been trained or loaded.')

        self.load_input_data(data_list)

        data = self.input_data.interpolate('time', limit_area='inside')
        features_df = self._load_features(data)
        target_stn = self.params['target_stn']

        if target_stn not in features_df:
            raise ValueError('target stn must be in data_list.')

        missing_index_bool = features_df[target_stn].isnull()
        missing_index = missing_index_bool[missing_index_bool].index
        missing_len = len(missing_index)

        if missing_len == 0:
            raise ValueError('There are no missing flow values to fill.')

        if 0 in self.models:
            raise NotImplementedError('Single model predict has not been implemented.')

        n_models = len(self.models)
        n_time_stamps = min([missing_len, n_models])

        print(f'{n_time_stamps} time stamps will be filled.')

        predict_list = []
        for i in range(1, n_time_stamps + 1):
            time_index = missing_index[i-1]
            model = self.models[i]
            for i2, features_df1 in self._iter_features(features_df, [i]):
                f1 = features_df1.loc[[time_index]]
                predict1 = model.predict(f1)
                predict_list.append([time_index, predict1[0]])

        predict1 = pd.DataFrame(predict_list, columns=['time', 'predicted'])

        return predict1


    def plot_test_timeseries(self, model_num: int):
        """

        """
        ax = self.test_predictions.loc[model_num].plot(lw=2)
        max_data1 = self.test_max_flows.loc[model_num].reset_index()
        max_data1.plot.scatter('time', 'Actual flow', ax=ax, fontsize=15, lw=3)
        plt.tight_layout()


    def plot_test_regression(self, model_num: int):
        """

        """
        max_data2 = self.test_max_flows.loc[model_num].sort_values('Actual flow')
        max_data2 = np.log(max_data2).rename(columns={'Actual flow': 'Actual flow (log scale)', 'Predicted flow': 'Predicted flow (log scale)'})
        ax = max_data2.set_index('Actual flow (log scale)', drop=False)['Actual flow (log scale)'].plot.line(color='red', lw=2)
        max_data2.plot.scatter('Actual flow (log scale)', 'Predicted flow (log scale)', ax=ax, fontsize=15, lw=2)
        plt.tight_layout()


    def export(self, output_path):
        """

        """
        with booklet.open(output_path, 'n', value_serializer='zstd', key_serializer='str', n_buckets=307) as f:
            for model_num, model in self.models.items():
                f[str(model_num)] = sio.dumps(model)
            f['base_model'] = sio.dumps(self.base_model)
            f['input_data'] = utils.PdSerial.dumps(self.input_data)
            f['params'] = orjson.dumps(self.params)


























































