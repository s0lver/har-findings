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


def calculate_patterns(samples_list, remove_gravity=True):
    """
    Calculate the statistics for each window in each samples list
    :param samples_list: A list of samples list
    :param remove_gravity: Whether gravity component should be removed from samples
    :return: A list of statistics. [[statistics for each window in first list],
    [statistics for each window in second list]], ...
    """
    all_patterns = []
    for samples in samples_list:
        if remove_gravity:
            filter_gravity(samples)
            samples = samples[10:17500]

        statistics = get_statistics_per_window(samples)
        all_patterns.append(statistics)

    return all_patterns


def calculate_nb_values_per_window_per_samples_list(patterns_list):
    sum_mean = 0.0
    sum_standard_deviation = 0.0
    patterns_counter = 0
    laplace_correction = 0.01

    # Means
    for patterns in patterns_list:
        for pattern in patterns:
            sum_mean += pattern["mean"]
            sum_standard_deviation += pattern["std_dev"]
            patterns_counter += 1

    mean_of_standard_deviation = (sum_standard_deviation / float(patterns_counter))
    mean_of_mean = (sum_mean / float(patterns_counter))

    # Variance
    accumulated_diff_mean = 0.0
    accumulated_diff_std_dev = 0.0

    for patterns in patterns_list:
        for pattern in patterns:
            accumulated_diff_std_dev += (pattern["std_dev"] - mean_of_standard_deviation) ** 2
            accumulated_diff_mean += (pattern["mean"] - mean_of_mean) ** 2

    variance_of_std_deviation = (accumulated_diff_std_dev / float(patterns_counter - 1.0))
    variance_of_mean = (accumulated_diff_mean / float(patterns_counter - 1.0))

    return [[mean_of_standard_deviation + laplace_correction, mean_of_mean + laplace_correction],
            [variance_of_std_deviation + laplace_correction, variance_of_mean + laplace_correction]]


def write_configuration_file(configurations_list, file_path):
    a_priori = 1.0 / len(configurations_list)

    with open(file_path, 'w') as text_file:
        for cf in configurations_list:
            text_file.write('%s\n' % a_priori)
            # text_file.write('%s,%s\n' % (cf[0][0], cf[0][1]))
            text_file.write('{},{}\n'.format(cf[0][0], cf[0][1]))
            # text_file.write('%s,%s\n' % (cf[1][0], cf[1][1]))
            text_file.write('{},{}\n'.format(cf[1][0], cf[1][1]))


def produce_training_configuration(files_for_static, files_for_walking, files_for_biking, files_for_vehicle):
    samples_for_static = read_samples(files_for_static)
    samples_for_walking = read_samples(files_for_walking)
    samples_for_biking = read_samples(files_for_biking)
    samples_for_vehicle = read_samples(files_for_vehicle)

    # patterns_static = calculate_patterns(samples_for_static, remove_gravity=False)
    # patterns_walking = calculate_patterns(samples_for_walking, remove_gravity=False)
    # patterns_biking = calculate_patterns(samples_for_biking, remove_gravity=False)
    # patterns_vehicle = calculate_patterns(samples_for_vehicle, remove_gravity=False)
    patterns_static = calculate_patterns(samples_for_static, remove_gravity=True)
    patterns_walking = calculate_patterns(samples_for_walking, remove_gravity=True)
    patterns_biking = calculate_patterns(samples_for_biking, remove_gravity=True)
    patterns_vehicle = calculate_patterns(samples_for_vehicle, remove_gravity=True)

    configuration_static = calculate_nb_values_per_window_per_samples_list(patterns_static)
    # configuration_walking = calculate_nb_values_per_window_per_samples_list(patterns_walking)
    # configuration_biking = calculate_nb_values_per_window_per_samples_list(patterns_biking)
    configuration_vehicle = calculate_nb_values_per_window_per_samples_list(patterns_vehicle)

    configuration_walking = [[999, 999], [999, 999]]
    configuration_biking = [[555, 555], [555, 555]]

    output_file_path = 'c:\\users/rafael/desktop/training-configuration.csv'
    write_configuration_file([configuration_static, configuration_walking,
                              configuration_biking, configuration_vehicle], output_file_path)


if __name__ == '__main__':
    files_for_static = ['data/static/static-samples-2017-09-21-183652-ui.csv']
    files_for_walking = []
    files_for_biking = []
    files_for_vehicle = ['data/vehicle/vehicle-samples-2017-09-21-214800-ui.csv',
                         'data/vehicle/vehicle-samples-2017-09-22-081037-ui.csv',
                         'data/vehicle/vehicle-samples-2017-09-22-092518-ui.csv']
    # files_for_static = ['data/raw-static.csv']
    # files_for_walking = ['data/raw-walking.csv']
    # files_for_biking = ['data/raw-running.csv']
    # files_for_vehicle = ['data/raw-vehicle.csv']

    produce_training_configuration(files_for_static, files_for_walking, files_for_biking, files_for_vehicle)
