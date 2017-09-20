from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np

from GravityFilterer import GravityFilterer
from acc_data_reader import read_csv_acc_samples_file
from entities.AccelerometerSample import AccelerometerSample
from plots.accelerometer_plots import plot_activity_data, plot_all_activities_data, plot_statistics, \
    plot_some_activities_data, plot_magnitude_vectors
from preprocessing.tools import normalize_time, calculate_magnitude_vector


def get_statistics_per_window(samples: List[AccelerometerSample]):
    statistics = []
    # List of dicts, each dict a dimension-attribute
    last_window = samples[-1].id_window

    for i in range(0, last_window):
        id_window = i + 1
        samples_of_window = list(filter(lambda x: x.id_window == id_window, samples))

        mv = np.array(calculate_magnitude_vector(samples_of_window))

        # Calculate each of the attributes, gravity has been already filtered
        mean = np.mean(mv)
        std_dev = np.std(mv)
        median = np.median(mv)

        d = {
            "mean": mean,
            "std_dev": std_dev,
            "median": median
        }
        statistics.append(d)

    return statistics


def do_work():
    home = str(Path.home()) + '/'
    desktop = home + 'desktop/'
    samples_static = read_csv_acc_samples_file('data/raw-static.csv')
    samples_walking = read_csv_acc_samples_file('data/raw-walking.csv')
    samples_running = read_csv_acc_samples_file('data/raw-running.csv')
    samples_vehicle = read_csv_acc_samples_file('data/raw-vehicle.csv')

    normalize_time(samples_static)
    normalize_time(samples_walking)
    normalize_time(samples_running)
    normalize_time(samples_vehicle)

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
    top_threshold = 40
    static_portion = list(filter(lambda x: x.timestamp < top_threshold, samples_static))
    walking_portion = list(filter(lambda x: x.timestamp < top_threshold, samples_walking))
    running_portion = list(filter(lambda x: x.timestamp < top_threshold, samples_running))
    vehicle_portion = list(filter(lambda x: x.timestamp < top_threshold, samples_vehicle))
    mv_static = calculate_magnitude_vector(static_portion)
    mv_walking = calculate_magnitude_vector(walking_portion )
    mv_running = calculate_magnitude_vector(running_portion)
    mv_vehicle = calculate_magnitude_vector(vehicle_portion)
    plot_magnitude_vectors([mv_static, mv_walking, mv_running, mv_vehicle], ['Static', 'Walking', 'Running', 'Vehicle'])
    plt.show()


def filter_gravity_per_window(samples):
    last_window = samples[-1].id_window

    for i in range(0, last_window):
        id_window = i + 1
        samples_of_window = list(filter(lambda x: x.id_window == id_window, samples))

        g = GravityFilterer(samples_of_window)
        g.filter_gravity()


if __name__ == '__main__':
    do_work()
