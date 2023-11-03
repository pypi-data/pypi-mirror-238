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
                self.model = sio.loads(f['model'], True)
                self.params = orjson.loads(f['params'])
                if load_model_data:
                    self.input_data = utils.PdSerial.loads(f['input_data'])


    def _prep_data(self, data: pd.DataFrame):
        """

        """
        if 'datetime64' not in data.index.dtype.name:
            raise TypeError('The index of data must be a datetime.')

        freq = pd.infer_freq(data.index[-3:])
        if freq is None:
            freq = pd.infer_freq(data.index[:3])

        if freq is None:
            raise ValueError('Could not infer frequency. Please assign.')

        model_freq = self.params['freq']
        if model_freq != freq:
            raise ValueError('model freq and data freq are not the same.')

        data1 = data.copy()
        data1.index.name = 'time'

        return data1


    def load_features(self, data: pd.DataFrame):
        """

        """
        data = self._prep_data(data)
        features_df = data[self.params['feature_cols']].copy()

        model_freq = self.params['freq']

        feature_list = []
        for col, lag in self.params['feature_lags'].items():
            lag_start, lag_end, agg = lag
            data0 = utils.create_shifted_df(features_df[col], lag_start, lag_end, model_freq, agg, col)
            feature_list.append(data0)

        model_features_df = pd.concat(feature_list, axis=1).dropna()

        return model_features_df


    def load_targets(self, data: pd.DataFrame):
        """

        """
        data = self._prep_data(data)
        target_df = data[self.params['target_col']].copy()

        return target_df


    def set_params(self, feature_cols: List[str], target_col: str, freq: str, lags: dict):
        """

        """
        feature_lags = {}
        for col in feature_cols:
            if col not in lags:
                raise ValueError('{col} is not in the lags dict'.format(col=col))

            lag_start, lag_end, agg = lags[col]

            if (not isinstance(lag_start, int)) or (not isinstance(lag_end, int)) or (agg not in ('sum', 'mean')):
                raise TypeError('lags must be a tuple or list of integers and an aggregation method at the end.')

            feature_lags[col] = (lag_start, lag_end, agg)

        self.params = {'freq': freq, 'feature_cols': feature_cols, 'target_col': target_col, 'feature_lags': feature_lags}


    def set_model(self, model):
        """

        """
        self.model = model


    def train_model(self, data: pd.DataFrame=None, break_time=None):
        """

        """
        ## Prep input data
        if data is None:
            data = self.input_data
        features_df = self.load_features(data)
        target_df = self.load_targets(data)

        all_df = pd.concat([features_df, target_df], axis=1).dropna()

        if break_time is not None:
            break_time1 = pd.Timestamp(break_time)
            train_df = all_df.loc[:break_time1].copy()
            self.test_features = all_df.loc[break_time1:].iloc[:, :-1].copy()
            self.test_targets = all_df.loc[break_time1:].iloc[:, -1].copy()
            self.test_targets.name = 'Actual flow'
        else:
            train_df = all_df

        train_target_df = train_df.iloc[:, -1].copy()
        train_features_df = train_df.iloc[:, :-1].copy()

        self.model.fit(train_features_df, train_target_df)
        # self.train_target_df = train_target_df
        # self.train_features_df = train_features_df
        self.input_data = data


    def predict(self, data: pd.DataFrame):
        """

        """
        model_features_df = self.load_features(data)
        predictions1 = self.model.predict(model_features_df)
        predict1 = pd.Series(predictions1, index=model_features_df.index, name='Predicted flow')

        return predict1


    def test_model(self):
        """

        """
        predictions1 = self.model.predict(self.test_features)
        predict1 = pd.Series(predictions1, index=self.test_features.index, name='Predicted flow')

        combo1 = pd.concat([self.test_targets, predict1], axis=1)

        ### Process results
        max_index = argrelextrema(self.test_targets.values, np.greater, order=12)[0]

        upper_index = np.where(self.test_targets.values > np.percentile(self.test_targets.values, 80))[0]

        test_labels_index = max_index[np.in1d(max_index, upper_index)]

        max_data = combo1.iloc[test_labels_index]

        ## Estimate accuracy/errors
        p1 = max_data.iloc[:, 1]
        a1 = max_data.iloc[:, 0]

        errors = abs(p1 - a1)
        bias_errors = (p1 - a1)

        # Print out the mean absolute error (mae)
        print('Mean Absolute Error:', round(np.mean(errors), 2), 'm3/s.')
        print('Mean Error (Bias):', round(np.mean(bias_errors), 2), 'm3/s.')

        # Calculate mean absolute percentage error (MAPE)
        mape = 100 * (errors / a1)

        # Calculate and display accuracy
        accuracy = np.mean(mape)
        print('MANE:', round(accuracy, 2), '%.')

        bias1 = np.mean(100 * (bias_errors / a1))
        print('MNE:', round(bias1, 2), '%.')

        self.test_predictions = combo1
        self.test_max_values = max_data


    def importances(self, n_repeats=3, random_state=0):
        """

        """
        r = permutation_importance(self.model, self.test_features, self.test_targets,
                                    n_repeats=n_repeats,
                                    random_state=n_repeats)

        important0 = pd.DataFrame({'importances_mean': r.importances_mean, 'importances_std': r.importances_std}, index=self.test_features.columns).sort_values('importances_mean', ascending=False)

        return important0


    def cross_validation(self, n_cv_folds=5, scoring='neg_mean_absolute_percentage_error'):
        """

        """
        features_df = self.load_features(self.input_data)
        target_df = self.load_targets(self.input_data)

        all_df = pd.concat([features_df, target_df], axis=1).dropna()

        target_df = all_df.iloc[:, -1].copy()
        features_df = all_df.iloc[:, :-1].copy()

        native_result = cross_val_score(self.model, features_df, target_df, cv=n_cv_folds, scoring=scoring)

        mean_score = np.abs(native_result).mean()
        sd_score = np.abs(native_result).std()

        print('MANE cross-val:', round(mean_score * 100, 1), '%')
        print('STDEV cross-val:', round(sd_score * 100, 1), '%')

        return native_result


    def plot_model_timeseries(self):
        """

        """
        ax = self.test_predictions.plot(lw=2)
        max_data1 = self.test_max_values.reset_index()
        max_data1.plot.scatter('time', 'Actual flow', ax=ax, fontsize=15, lw=3)
        plt.tight_layout()


    def plot_model_regression(self):
        """

        """
        max_data2 = self.test_max_values.sort_values('Actual flow')
        max_data2 = np.log(max_data2).rename(columns={'Actual flow': 'Actual flow (log scale)', 'Predicted flow': 'Predicted flow (log scale)'})
        ax = max_data2.set_index('Actual flow (log scale)', drop=False)['Actual flow (log scale)'].plot.line(color='red', lw=2)
        max_data2.plot.scatter('Actual flow (log scale)', 'Predicted flow (log scale)', ax=ax, fontsize=15, lw=2)
        plt.tight_layout()


    def export(self, output_path):
        """

        """
        with booklet.open(output_path, 'n', value_serializer='zstd', key_serializer='str', n_buckets=100) as f:
            f['model'] = sio.dumps(self.model)
            f['input_data'] = utils.PdSerial.dumps(self.input_data)
            f['params'] = orjson.dumps(self.params)