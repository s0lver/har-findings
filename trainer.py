import numpy as np

from acc_data_reader import read_csv_acc_samples_file
from launcher import filter_gravity, get_statistics_per_window
from preprocessing.tools import calculate_magnitude_vector, means


def read_samples(file_paths):
    sample_list = []
    for path in file_paths:
        samples = read_csv_acc_samples_file(path)
        sample_list.append(samples)

    return sample_list


def calculate_patterns(samples_list, mean_to_add, remove_gravity=True):
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

        statistics = get_statistics_per_window(samples, mean_to_add)
        all_patterns.append(statistics)

    return all_patterns


def calculate_nb_values_per_window(patterns_list, feature_one, feature_two):
    sum_feature_one = 0.0
    sum_feature_two = 0.0
    patterns_counter = 0
    laplace_correction = 0.01

    # Means
    for patterns in patterns_list:
        for pattern in patterns:
            sum_feature_one += pattern[feature_one]
            sum_feature_two += pattern[feature_two]
            patterns_counter += 1

    mean_of_feature_two = (sum_feature_two / float(patterns_counter))
    mean_of_feature_one = (sum_feature_one / float(patterns_counter))

    # Variance
    accumulated_diff_feature_one = 0.0
    accumulated_diff_feature_two = 0.0

    for patterns in patterns_list:
        for pattern in patterns:
            accumulated_diff_feature_two += (pattern[feature_two] - mean_of_feature_two) ** 2
            accumulated_diff_feature_one += (pattern[feature_one] - mean_of_feature_one) ** 2

    variance_of_feature_two = (accumulated_diff_feature_two / float(patterns_counter - 1.0))
    variance_of_feature_one = (accumulated_diff_feature_one / float(patterns_counter - 1.0))

    return [[mean_of_feature_one + laplace_correction, mean_of_feature_two + laplace_correction],
            [variance_of_feature_one + laplace_correction, variance_of_feature_two + laplace_correction]]


def write_configuration_file(configurations_list, means_to_write, file_path):
    a_priori = 1.0 / len(configurations_list)
    i = 0
    with open(file_path, 'w') as text_file:
        for cf in configurations_list:
            text_file.write('{},{}\n'.format(a_priori, means_to_write[i]))
            # text_file.write('%s,%s\n' % (cf[0][0], cf[0][1]))
            text_file.write('{},{}\n'.format(cf[0][0], cf[0][1]))
            # text_file.write('%s,%s\n' % (cf[1][0], cf[1][1]))
            text_file.write('{},{}\n'.format(cf[1][0], cf[1][1]))
            i += 1


def produce_training_configuration(static_files, walking_files, biking_files, vehicle_files):
    samples_for_static = read_samples(static_files)
    samples_for_walking = read_samples(walking_files)
    samples_for_biking = read_samples(biking_files)
    samples_for_vehicle = read_samples(vehicle_files)

    # patterns_static = calculate_patterns(samples_for_static, remove_gravity=False)
    # patterns_walking = calculate_patterns(samples_for_walking, remove_gravity=False)
    # patterns_biking = calculate_patterns(samples_for_biking, remove_gravity=False)
    # patterns_vehicle = calculate_patterns(samples_for_vehicle, remove_gravity=False)
    patterns_static = calculate_patterns(samples_for_static, mean_to_add=means["static"], remove_gravity=True)
    patterns_walking = calculate_patterns(samples_for_walking, mean_to_add=means["walking"], remove_gravity=True)
    patterns_biking = calculate_patterns(samples_for_biking, mean_to_add=0.0, remove_gravity=True)
    patterns_vehicle = calculate_patterns(samples_for_vehicle, mean_to_add=means["vehicle"], remove_gravity=True)

    feature_one = "std_dev"
    feature_two = "mean_with_mean"

    configuration_static = calculate_nb_values_per_window(patterns_static, feature_one, feature_two)
    configuration_walking = calculate_nb_values_per_window(patterns_walking, feature_one, feature_two)
    # configuration_biking = calculate_nb_values_per_window_per_samples_list(patterns_biking)
    configuration_vehicle = calculate_nb_values_per_window(patterns_vehicle, feature_one, feature_two)

    # configuration_walking = [[999, 999], [999, 999]]
    configuration_biking = [[555, 555], [555, 555]]

    output_file_path = 'c:\\users/rafael/desktop/training-configuration.csv'
    write_configuration_file([configuration_static, configuration_walking, configuration_biking, configuration_vehicle],
                             [means["static"], means["walking"], means["biking"], means["vehicle"]],
                             output_file_path)


if __name__ == '__main__':
    # files_for_static = ['data/static/static-samples-2017-09-21-183652-ui.csv']
    files_for_static = ['data/static/static-samples-2017-09-21-183652-ui-clean.csv']
    files_for_walking = ['data/walking/walking-samples-2017-09-30-101645-ui-clean.csv']
    files_for_biking = []
    # files_for_vehicle = ['data/vehicle/vehicle-samples-2017-09-21-214800-ui.csv',
    #                      'data/vehicle/vehicle-samples-2017-09-22-081037-ui.csv',
    #                      'data/vehicle/vehicle-samples-2017-09-22-092518-ui.csv']
    files_for_vehicle = ['data/vehicle/vehicle-samples-2017-09-21-214800-ui-clean.csv',
                         'data/vehicle/vehicle-samples-2017-09-22-081037-ui-clean.csv',
                         'data/vehicle/vehicle-samples-2017-09-22-092518-ui-clean.csv']
    # files_for_static = ['data/raw-static.csv']
    # files_for_walking = ['data/raw-walking.csv']
    # files_for_biking = ['data/raw-running.csv']
    # files_for_vehicle = ['data/raw-vehicle.csv']

    produce_training_configuration(files_for_static, files_for_walking, files_for_biking, files_for_vehicle)
