from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from acc_data_reader import read_csv_acc_samples_file
from entities.AccelerometerSample import AccelerometerSample
from plots.accelerometer_plots import plot_activity_data, plot_statistics, \
    plot_magnitude_vectors, plot_magnitude_vectors_per_alpha, plot_accelerations_and_mag_vectors, plot_three_dimensions
from preprocessing.tools import normalize_time, calculate_magnitude_vector, filter_gravity, get_statistics_per_window, \
    get_ranges, get_average_range_size


def show_different_filter_configurations(alpha=0.8):
    samples_vehicle_1 = read_csv_acc_samples_file(
        'c:\\users/rafael/desktop/vehicle/focus-guindo/vehicle-samples-2017-09-19-192509.csv')
    samples_power_on = read_csv_acc_samples_file('c:\\users/rafael/desktop/static-power-on.csv')
    # samples_power_off = read_csv_acc_samples_file('c:\\users/rafael/desktop/static-power-off.csv')
    new_start = 20
    samples_power_on = samples_power_on[new_start:]
    samples_vehicle_1 = samples_vehicle_1[new_start:]
    # samples_power_off = samples_power_off[new_start:]

    filter_gravity(samples_power_on, alpha=alpha)
    filter_gravity(samples_vehicle_1, alpha=alpha)
    # filter_gravity(samples_power_off, alpha=alpha)

    normalize_time(samples_power_on)
    normalize_time(samples_vehicle_1)
    # normalize_time(samples_power_off)

    ts_top_threshold = 150
    samples_power_on = list(filter(lambda x: x.timestamp < ts_top_threshold, samples_power_on))
    samples_vehicle_1 = list(filter(lambda x: x.timestamp < ts_top_threshold, samples_vehicle_1))
    # samples_power_off = list(filter(lambda x: x.timestamp < ts_top_threshold, samples_power_off))

    # samples_power_on = samples_power_on[:ts_top_threshold]
    # samples_power_off = samples_power_off[:ts_top_threshold]

    # plot_activity_data(samples_power_on, 'Powered on, alpha={}'.format(alpha))
    # plot_activity_data(samples_vehicle_1, 'V1, alpha={}'.format(alpha))
    # plot_activity_data(samples_power_off, 'Powered off, alpha={}'.format(alpha))

    # plot the magnitude vectors
    mv_static_1 = calculate_magnitude_vector(samples_power_on)
    mv_vehicle_1 = calculate_magnitude_vector(samples_vehicle_1)

    vectors = [mv_static_1, mv_vehicle_1]
    activities = ['Static', 'V1']
    vectors = [mv_static_1, mv_vehicle_1]
    activities = ['Static', 'V1']
    plot_magnitude_vectors(vectors, activities)


def do_work():
    home = str(Path.home()) + '/'
    desktop = home + 'desktop/'

    samples_vehicle_1 = read_csv_acc_samples_file(
        'c:\\users/rafael/desktop/vehicle/focus-guindo/vehicle-samples-2017-09-19-192509.csv')
    samples_vehicle_2 = read_csv_acc_samples_file(
        'c:\\users/rafael/desktop/vehicle/focus-guindo/vehicle-samples-2017-09-20-081651.csv')
    samples_vehicle_3 = read_csv_acc_samples_file(
        'c:\\users/rafael/desktop/vehicle/focus-guindo/vehicle-samples-2017-09-20-092617.csv')

    samples_vehicle_4 = read_csv_acc_samples_file(
        'c:\\users/rafael/desktop/vehicle/focus-arena/vehicle-samples-2017-09-20-131224.csv')
    samples_vehicle_5 = read_csv_acc_samples_file(
        'c:\\users/rafael/desktop/vehicle/focus-arena/vehicle-samples-2017-09-20-140314.csv')

    samples_static_1 = read_csv_acc_samples_file(
        'c:\\users/rafael/desktop/static/static-samples-2017-09-21-183652-ui.csv')

    # filter_gravity_per_window(samples_vehicle_1)
    # filter_gravity_per_window(samples_vehicle_2)
    # filter_gravity_per_window(samples_vehicle_3)
    # filter_gravity_per_window(samples_vehicle_4)
    # filter_gravity_per_window(samples_vehicle_5)
    # filter_gravity_per_window(samples_static_1)

    filter_gravity(samples_vehicle_1)
    filter_gravity(samples_vehicle_2)
    filter_gravity(samples_vehicle_3)
    filter_gravity(samples_vehicle_4)
    filter_gravity(samples_vehicle_5)
    filter_gravity(samples_static_1)

    # new_start = 20
    new_start = 15
    samples_vehicle_1 = samples_vehicle_1[new_start:]
    samples_vehicle_2 = samples_vehicle_2[new_start:]
    samples_vehicle_3 = samples_vehicle_3[new_start:]
    samples_vehicle_4 = samples_vehicle_4[new_start:]
    samples_vehicle_5 = samples_vehicle_5[new_start:]
    samples_static_1 = samples_static_1[new_start:]

    normalize_time(samples_vehicle_1)
    normalize_time(samples_vehicle_2)
    normalize_time(samples_vehicle_3)
    normalize_time(samples_vehicle_4)
    normalize_time(samples_vehicle_5)
    normalize_time(samples_static_1)

    plot_activity_data(samples_vehicle_1, 'Vehicle one')
    plot_activity_data(samples_vehicle_2, 'Vehicle two')
    plot_activity_data(samples_vehicle_3, 'Vehicle three')
    plot_activity_data(samples_vehicle_4, 'Vehicle four')
    plot_activity_data(samples_vehicle_5, 'Vehicle five')
    plot_activity_data(samples_static_1, 'Static one')

    # Plot of magnitude vectors
    top_threshold = 500
    static_1_portion = list(filter(lambda x: x.timestamp < top_threshold, samples_static_1))
    vehicle_1_portion = list(filter(lambda x: x.timestamp < top_threshold, samples_vehicle_1))
    vehicle_2_portion = list(filter(lambda x: x.timestamp < top_threshold, samples_vehicle_2))
    vehicle_3_portion = list(filter(lambda x: x.timestamp < top_threshold, samples_vehicle_3))
    vehicle_4_portion = list(filter(lambda x: x.timestamp < top_threshold, samples_vehicle_4))
    vehicle_5_portion = list(filter(lambda x: x.timestamp < top_threshold, samples_vehicle_5))

    mv_static_1 = calculate_magnitude_vector(static_1_portion)
    mv_vehicle_1 = calculate_magnitude_vector(vehicle_1_portion)
    mv_vehicle_2 = calculate_magnitude_vector(vehicle_2_portion)
    mv_vehicle_3 = calculate_magnitude_vector(vehicle_3_portion)
    mv_vehicle_4 = calculate_magnitude_vector(vehicle_4_portion)
    mv_vehicle_5 = calculate_magnitude_vector(vehicle_5_portion)
    vectors = [mv_static_1, mv_vehicle_1, mv_vehicle_2, mv_vehicle_3, mv_vehicle_4, mv_vehicle_5]
    activities = ['Static', 'V1', 'V2', 'V3', 'V4', 'V5']
    vectors = [mv_static_1, mv_vehicle_5]
    activities = ['Static', 'V5']
    # plot_magnitude_vectors(vectors, activities)

    # Plot of statistics
    statistics_static_1 = get_statistics_per_window(samples_static_1)
    statistics_vehicle_1 = get_statistics_per_window(samples_vehicle_1)
    statistics_vehicle_2 = get_statistics_per_window(samples_vehicle_2)
    statistics_vehicle_3 = get_statistics_per_window(samples_vehicle_3)
    statistics_vehicle_4 = get_statistics_per_window(samples_vehicle_4)
    statistics_vehicle_5 = get_statistics_per_window(samples_vehicle_5)

    statistics_ids = ['std_dev', 'mean']
    plot_statistics(statistics_static_1, statistics_vehicle_1, statistics_vehicle_2, statistics_vehicle_3,
                    statistics_ids, ['Static', 'Vehicle 1', 'Vehicle 2', 'Vehicle 3'])
    # plot_statistics(statistics_static, statistics_walking, statistics_running, statistics_vehicle, statistics_ids)
    plot_statistics(statistics_static_1, [], [], statistics_vehicle_1, statistics_ids,
                    ['Static', 'Vehicle 1', 'Vehicle 2', 'Vehicle 3'])
    plt.show()

    # top_threshold = 40
    # static_portion = list(filter(lambda x: x.timestamp < top_threshold, samples_static))
    # walking_portion = list(filter(lambda x: x.timestamp < top_threshold, samples_walking))
    # running_portion = list(filter(lambda x: x.timestamp < top_threshold, samples_running))
    # vehicle_portion = list(filter(lambda x: x.timestamp < top_threshold, samples_vehicle))
    # mv_static = calculate_magnitude_vector(static_portion)
    # mv_walking = calculate_magnitude_vector(walking_portion)
    # mv_running = calculate_magnitude_vector(running_portion)
    # mv_vehicle = calculate_magnitude_vector(vehicle_portion)
    # plot_magnitude_vectors([mv_static, mv_walking, mv_running, mv_vehicle], ['Static', 'Walking', 'Running', 'Vehicle'])
    # plt.show()


    # samples_static = read_csv_acc_samples_file('data/raw-static.csv')
    # samples_walking = read_csv_acc_samples_file('data/raw-walking.csv')
    # samples_running = read_csv_acc_samples_file('data/raw-running.csv')
    # samples_vehicle = read_csv_acc_samples_file('data/raw-vehicle.csv')

    # normalize_time(samples_static)
    # normalize_time(samples_walking)
    # normalize_time(samples_running)
    # normalize_time(samples_vehicle)

    # filter_gravity_per_window(samples_static)
    # filter_gravity_per_window(samples_walking)
    # filter_gravity_per_window(samples_running)
    # filter_gravity_per_window(samples_vehicle)

    # Visualization of x,y,z axes and magnitude vector
    # plot_activity_accelerations(samples_static, 'Static', desktop + 'static.pdf')
    # plot_activity_accelerations(samples_walking, 'Walking', desktop + 'walking.pdf')
    # plot_activity_accelerations(samples_running, 'Running', desktop + 'running.pdf')
    # plot_activity_accelerations(samples_vehicle, 'Vehicle', desktop + 'vehicle.pdf')
    # plot_all_activities_data(samples_static, samples_walking, samples_running, samples_vehicle)

    # Statistics per each activity
    # statistics_static = get_statistics_per_window(samples_static)
    # statistics_walking = get_statistics_per_window(samples_walking)
    # statistics_running = get_statistics_per_window(samples_running)
    # statistics_vehicle = get_statistics_per_window(samples_vehicle)
    # statistics_ids = ['std_dev', 'mean']
    # plot_statistics(statistics_static, statistics_walking, statistics_running, statistics_vehicle, statistics_ids)
    # plot_statistics(statistics_static, [], [], statistics_vehicle, statistics_ids)

    # Static vs Vehicle
    # top_threshold = 40000
    # static_portion = list(filter(lambda x: x.timestamp < top_threshold, samples_static))
    # vehicle_portion = list(filter(lambda x: x.timestamp < top_threshold, samples_vehicle))
    # plot_some_activities_data([static_portion, vehicle_portion], ['Static', 'Vehicle'])

    # Plot of magnitude vectors
    # top_threshold = 40
    # static_portion = list(filter(lambda x: x.timestamp < top_threshold, samples_static))
    # walking_portion = list(filter(lambda x: x.timestamp < top_threshold, samples_walking))
    # running_portion = list(filter(lambda x: x.timestamp < top_threshold, samples_running))
    # vehicle_portion = list(filter(lambda x: x.timestamp < top_threshold, samples_vehicle))
    # mv_static = calculate_magnitude_vector(static_portion)
    # mv_walking = calculate_magnitude_vector(walking_portion )
    # mv_running = calculate_magnitude_vector(running_portion)
    # mv_vehicle = calculate_magnitude_vector(vehicle_portion)
    # plot_magnitude_vectors([mv_static, mv_walking, mv_running, mv_vehicle], ['Static', 'Walking', 'Running', 'Vehicle'])
    # plt.show()


def show_normal_vs_ui(normal_file_path, ui_file_path):
    samples_static_normal = read_csv_acc_samples_file(
        normal_file_path)
    samples_static_ui = read_csv_acc_samples_file(ui_file_path)

    # ts_top_threshold = 150
    # samples_static_ui = list(filter(lambda x: x.timestamp < ts_top_threshold, samples_static_ui))
    # samples_static_normal = list(filter(lambda x: x.timestamp < ts_top_threshold, samples_static_normal))

    normalize_time(samples_static_normal)
    normalize_time(samples_static_ui)

    # samples_static_normal = samples_static_normal[10:]
    # samples_static_ui = samples_static_ui[10:]

    normalize_time(samples_static_normal, factor=1.0)
    normalize_time(samples_static_ui, factor=1.0)

    filter_gravity(samples_static_normal)
    filter_gravity(samples_static_ui)

    # normalize_time(samples_static_normal)
    # normalize_time(samples_static_ui)

    plot_activity_data(samples_static_normal, 'Static normal')
    plot_activity_data(samples_static_ui, 'Static UI')


def show_magnitude_vector_per_alpha(alpha_values, file_path):
    vectors = []
    samples = read_csv_acc_samples_file(file_path)
    normalize_time(samples)
    timestamps = list(map(lambda x: x.timestamp, samples))
    for alpha in alpha_values:
        samples = read_csv_acc_samples_file(file_path)
        normalize_time(samples)
        filter_gravity(samples, alpha=alpha)
        mv = calculate_magnitude_vector(samples)
        vectors.append(mv)

    plot_magnitude_vectors_per_alpha(vectors, timestamps, alpha_values, single=True)


def plot_new_values(files, activity_labels, remove_gravity=True):
    mvs = []
    stats = []
    i = 0
    for file in files:
        print('reading {}'.format(file))
        samples = read_csv_acc_samples_file(file)
        if remove_gravity:
            filter_gravity(samples)
            samples = samples[10:17500]

        mv = calculate_magnitude_vector(samples)
        mvs.append(mv)

        stat = get_statistics_per_window(samples, mean_to_add=means_are[i])
        stats.append(stat)
        i += 1

    # plot_magnitude_vectors(mvs, activity_labels)

    # statistics_ids = ['std_dev', 'acc_range_size']
    statistics_ids = ['std_dev', 'mean_with_mean']
    plot_statistics(stats[0], stats[1], stats[2], stats[3], statistics_ids, activity_labels)

    # statistics_ids = ['mean', 'acc_range_size']
    statistics_ids = ['median', 'mean_with_mean']
    plot_statistics(stats[0], stats[1], stats[2], stats[3], statistics_ids, activity_labels)


def plot_portion_of_data(files, activity_labels, remove_gravity=True):
    samples_list = []
    new_start = 20
    id_window_to_select = 90

    for f in files:
        samples = read_csv_acc_samples_file(f)
        if remove_gravity:
            filter_gravity(samples)
            samples = samples[new_start:]

        samples = list(filter(lambda x: x.id_window < id_window_to_select, samples))
        normalize_time(samples)

        samples_list.append(samples)

    plot_accelerations_and_mag_vectors(samples_list, activity_labels)


def calculate_global_statistics(files, remove_gravity=True):
    samples_list = []
    new_start = 20

    for f in files:
        samples = read_csv_acc_samples_file(f)
        if remove_gravity:
            filter_gravity(samples)
            samples = samples[new_start:]

        mv = calculate_magnitude_vector(samples)
        mean_value = np.mean(mv)
        print('For {} mean is {}'.format(f, mean_value))


def analyze_three_dimensions(files, activity_labels):
    new_start = 20
    statistics = []
    i = 0
    for f in files:
        samples = read_csv_acc_samples_file(f)
        filter_gravity(samples)
        samples = samples[new_start:]

        normalize_time(samples)
        stats = get_statistics_per_window(samples, mean_to_add=means_are[i])
        statistics.append(stats)
        i += 1

    attributes_to_plot = ['mean', 'std_dev', 'avg_range_size_with_mean']
    plot_three_dimensions(statistics, activity_labels, attributes_to_plot)


def different_filter_configurations():
    show_different_filter_configurations(alpha=0.3)
    show_different_filter_configurations(alpha=0.5)
    show_different_filter_configurations(alpha=0.95)


def normal_vs_ui():
    show_normal_vs_ui(normal_file_path='c:\\users/rafael/desktop/static/static-samples-2017-09-20-125440.csv',
                      ui_file_path='c:\\users/rafael/desktop/static/static-samples-2017-09-21-124838-ui.csv')
    show_normal_vs_ui(
        normal_file_path='c:\\users/rafael/desktop/vehicle/focus-arena/vehicle-samples-2017-09-20-131224.csv',
        ui_file_path='c:\\users/rafael/desktop/vehicle/focus-arena/vehicle-samples-2017-09-21-131545-ui.csv')


def magnitude_vectors_vs_alpha():
    show_magnitude_vector_per_alpha(alpha_values=[0.9, 0.95],
                                    file_path='c:\\users/rafael/desktop/static/static-samples-2017-09-21-183652-ui.csv')
    show_magnitude_vector_per_alpha(alpha_values=[0.9, 0.95],
                                    file_path='c:\\users/rafael/desktop/static/static-samples-2017-09-21-183652-ui.csv')


means_are = [0.09792535164706333, 0.44263381696905124, 0.4642997219313103, 0.52316091488281]

if __name__ == '__main__':
    files = [
        'c:\\users/rafael/desktop/static/static-samples-2017-09-21-183652-ui.csv',
        'c:\\users/rafael/desktop/vehicle/focus-guindo/vehicle-samples-2017-09-21-214800-ui.csv',
        'c:\\users/rafael/desktop/vehicle/focus-guindo/vehicle-samples-2017-09-22-081037-ui.csv',
        'c:\\users/rafael/desktop/vehicle/focus-guindo/vehicle-samples-2017-09-22-092518-ui.csv',
    ]
    activity_labels = [
        'static',
        'vehicle',
        'vehicle',
        'vehicle'
    ]

    # calculate_global_statistics(files, remove_gravity=True)

    # files = [
    #     'data/raw-static.csv',
    #     'data/raw-walking.csv',
    #     'data/raw-running.csv',
    #     'data/raw-vehicle.csv'
    # ]
    #
    # activity_labels = [
    #     'static',
    #     'walking',
    #     'running',
    #     'vehicle'
    # ]

    plot_new_values(files, activity_labels, remove_gravity=True)

    # do_work()
    # different_filter_configurations()
    # normal_vs_ui()
    # magnitude_vectors_vs_alpha()

    # plot_portion_of_data(files, activity_labels)
    # show_statistics_per_window(files)
    # analyze_three_dimensions(files, activity_labels)
    plt.show()

    # samples = read_csv_acc_samples_file(files[0])
    # filter_gravity(samples)
    # samples = samples[10:17500]
    #
    # filtered_samples = list(filter(lambda x: x.id_window==10, samples))
    # filtered_mvs = calculate_magnitude_vector(filtered_samples)
    #
    # # for s in filtered_samples:
    # #     print(s)
    # #
    # # print()
    # # for v in filtered_mvs:
    # #     print(v)
    #
    # stats = get_statistics_per_window(filtered_samples)
    # print(stats)
    #
    # samples = read_csv_acc_samples_file(files[1])
    # filter_gravity(samples)
    # samples = samples[10:17500]
    #
    # filtered_samples = list(filter(lambda x: x.id_window == 10, samples))
    # filtered_mvs = calculate_magnitude_vector(filtered_samples)
    #
    # # for s in filtered_samples:
    # #     print(s)
    # #
    # # print()
    # # for v in filtered_mvs:
    # #     print(v)
    #
    # stats = get_statistics_per_window(filtered_samples)
    # print(stats)
