import numpy as np

from acc_data_reader import read_csv_acc_samples_file
from launcher import filter_gravity, get_statistics_per_window
from preprocessing.tools import calculate_magnitude_vector


def read_samples(file_paths):
    sample_list = []
    for path in file_paths:
        samples = read_csv_acc_samples_file(path)
        sample_list.append(samples)

    return sample_list


def calculate_patterns(samples_list):
    """
    Calculate the statistics for each window in each samples list
    :param samples_list: A list of samples list
    :return: A list of statistics lists. [[statistics for each window in first list],
    [statistics for each window in second list]], ...
    """
    all_statistics = []
    for samples in samples_list:
        filter_gravity(samples)
        samples = samples[10:17500]

        statistics = get_statistics_per_window(samples)
        all_statistics.append(statistics)


def calculate_nb_values_per_window_per_samples_list(patterns_list):
    sum_mean = 0.0
    sum_standard_deviation = 0.0

    patterns_counter = 0
    # Means
    for patterns in patterns_list:
        for pattern in patterns:
            sum_mean += pattern["mean"]
            sum_standard_deviation += pattern["std_dev"]
            patterns_counter += 1

    mean_of_mean = sum_mean / float(patterns_counter)
    mean_of_standard_deviation = sum_standard_deviation / float(patterns_counter)

    # Variance
    accum_diff_mean = 0.0
    accum_diff_std_dev = 0.0

    for patterns in patterns_list:
        for pattern in patterns:
            accum_diff_std_dev += (pattern["std_dev"] - mean_of_standard_deviation) ** 2
            accum_diff_mean += (pattern["mean"] - mean_of_mean) ** 2

    variance_of_mean = accum_diff_mean / float(patterns_counter - 1)
    variance_of_std_deviation = accum_diff_std_dev / float(patterns_counter - 1)

    # TODO work this better
    return [[mean_of_mean, mean_of_standard_deviation], [variance_of_mean, variance_of_std_deviation]]


def produce_training_configuration():
    statistics_ids = ['std_dev', 'mean']
    files_for_static = ['data/static/static-samples-2017-09-21-183652-ui.csv']
    files_for_vehicle = ['data/vehicle/vehicle-samples-2017-09-21-214800-ui.csv',
                         'data/vehicle/vehicle-samples-2017-09-22-081037-ui.csv',
                         'data/vehicle/vehicle-samples-2017-09-22-092518-ui.csv']

    files_for_walking = []
    files_for_biking = []

    samples_for_static = read_samples(files_for_static)
    samples_for_walking = read_samples(files_for_walking)
    samples_for_biking = read_samples(files_for_biking)
    samples_for_vehicle = read_samples(files_for_vehicle)

    patterns_static = calculate_patterns(samples_for_static)
    means_static = calculate_nb_values_per_window_per_samples_list(patterns_static)


if __name__ == '__main__':
    produce_training_configuration()
