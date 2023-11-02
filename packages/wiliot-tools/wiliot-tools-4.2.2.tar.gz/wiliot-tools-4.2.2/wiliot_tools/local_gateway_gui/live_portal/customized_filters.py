import math
import numpy as np


def tti_filter_function(tag_df, attribute, tag_id, filter_window_size):
    tag_tti_parameters = {
        'default': [0.45, 0],
        '000d40000719': [0.49, 0],
        'd4d4000002cb': [0.3, 0],
    }
    x_axis_values_df = tag_df['time_from_start']
    y_values_not_nan_mask = tag_df[attribute].notna()
    x_axis_values_df = x_axis_values_df[y_values_not_nan_mask]
    y_axis_values = tag_df[attribute][y_values_not_nan_mask]

    temprature_values = tag_df['temprature'][y_values_not_nan_mask]

    tag_parameters = tag_tti_parameters.get(tag_id, tag_tti_parameters['default'])
    y_filtered_axis_values = y_axis_values - temprature_values * tag_parameters[0]

    # y_filtered_axis_values = y_axis_values.rolling(self.filter_kernel).median()
    y_filtered_axis_values_nonan = y_filtered_axis_values[y_filtered_axis_values.notna()]

    return x_axis_values_df, y_filtered_axis_values_nonan


def median_filter_function(tag_df, attribute, tag_id, filter_window_size):
    x_axis_values_df = tag_df['time_from_start']
    y_values_not_nan_mask = tag_df[attribute].notna()
    x_axis_values_df = x_axis_values_df[y_values_not_nan_mask]
    y_axis_values = tag_df[attribute][y_values_not_nan_mask]
    y_filtered_axis_values = y_axis_values.rolling(filter_window_size).median()
    y_filtered_axis_values_nonan = y_filtered_axis_values[y_filtered_axis_values.notna()]

    return x_axis_values_df, y_filtered_axis_values_nonan

def mean_filter_function(tag_df, attribute, tag_id, filter_window_size):
    x_axis_values_df = tag_df['time_from_start']
    y_values_not_nan_mask = tag_df[attribute].notna()
    x_axis_values_df = x_axis_values_df[y_values_not_nan_mask]
    y_axis_values = tag_df[attribute][y_values_not_nan_mask]
    y_filtered_axis_values = y_axis_values.rolling(filter_window_size).mean()
    y_filtered_axis_values_nonan = y_filtered_axis_values[y_filtered_axis_values.notna()]

    return x_axis_values_df, y_filtered_axis_values_nonan