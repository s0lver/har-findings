import math
from typing import List

import numpy as np

from GravityFilterer import GravityFilterer
from entities.AccelerometerSample import AccelerometerSample

means = {
    "static": 0.08646747846470636,
    "walking": 3.379133914910735,
    "biking": 999,
    "vehicle": 0.5267873675845448,
}


def calculate_magnitude_vector(samples: List[AccelerometerSample]):
    vector = []
    for s in samples:
        sum = (s.x ** 2) + (s.y ** 2) + (s.z ** 2)
        magnitude = math.sqrt(sum)
        vector.append(magnitude)

    return vector


def get_cross_value(prior_sample, current_sample, cross_value, axis):
    prior_value = getattr(prior_sample, axis)
    current_value = getattr(current_sample, axis)
    if prior_value < cross_value <= current_value:
        return 1
    elif prior_value > cross_value >= current_value:
        return -1
    else:
        return 0


def calculate_zero_crossings(samples: List[AccelerometerSample], cross_value=0.0):
    samples_size = len(samples)
    crossings_x = 0
    crossings_y = 0
    crossings_z = 0

    for i in range(1, samples_size):
        prior_sample = samples[i - 1]
        current_sample = samples[i]

        crossing_x = get_cross_value(prior_sample, current_sample, cross_value, 'x')
        crossing_y = get_cross_value(prior_sample, current_sample, cross_value, 'y')
        crossing_z = get_cross_value(prior_sample, current_sample, cross_value, 'z')

        if crossing_x != 0:
            crossings_x += 1

        if crossing_y != 0:
            crossings_y += 1

        if crossing_z != 0:
            crossings_z += 1

    return {"crossings_x": crossings_x, "crossings_y": crossings_y, "crossings_z": crossings_z}


def normalize_time(samples: List[AccelerometerSample], factor=1000.0):
    start_time = samples[0].timestamp

    for sample in samples:
        sample.timestamp = (sample.timestamp - start_time) / factor

        # Try it without return :)


def filter_gravity(samples, alpha=0.8):
    g = GravityFilterer(samples, alpha)
    g.filter_gravity()


def filter_gravity_per_window(samples):
    first_window = samples[0].id_window
    last_window = samples[-1].id_window

    for i in range(first_window, last_window):
        id_window = i
        samples_of_window = list(filter(lambda x: x.id_window == id_window, samples))

        g = GravityFilterer(samples_of_window)
        g.filter_gravity()


def get_accumulated_range_size(ranges):
    sizes = []
    for r in ranges:
        sizes.append(math.fabs(r[0] - r[1]))

    return sum(sizes)


def get_average_max_range(ranges):
    acc_sum = 0.0
    for r in ranges:
        acc_sum += np.max([r[0], r[1]])

    return acc_sum / float(len(ranges))


def get_statistics_per_window(gravity_free_samples: List[AccelerometerSample], mean_to_add=0.0):
    statistics = []

    # List of dicts, each dict a dimension-attribute
    first_window = gravity_free_samples[0].id_window
    last_window = gravity_free_samples[-1].id_window

    for i in range(first_window, last_window + 1):
        id_window = i
        samples_of_window = list(filter(lambda x: x.id_window == id_window, gravity_free_samples))

        mv = np.array(calculate_magnitude_vector(samples_of_window))

        # Calculate each of the attributes, gravity has been already filtered
        signal_magnitude_area = sum(mv)
        ranges = get_ranges(mv)
        average_range_size = get_average_range_size(ranges)
        accumulated_range_size = get_accumulated_range_size(ranges)
        average_max_range = get_average_max_range(ranges)
        mean = my_mean(mv)
        mean_with_mean = mean + mean_to_add
        average_range_size_with_mean = average_range_size + mean_to_add
        std_dev = my_std_dev(mv, mean)
        median_value = np.median(mv)
        crossings = calculate_zero_crossings(samples_of_window, mean)

        sum_crossings = crossings["crossings_x"] + crossings["crossings_y"] + crossings["crossings_z"]
        d = {
            "mean": mean,
            "mean_with_mean": mean_with_mean,
            "std_dev": std_dev,
            "median": median_value,
            "signal_magnitude_area": signal_magnitude_area,
            "crossings_x": crossings["crossings_x"],
            "crossings_y": crossings["crossings_y"],
            "crossings_z": crossings["crossings_z"],
            "crossings": sum_crossings,
            "avg_crossings": sum_crossings / 3.0,
            "avg_range_size": average_range_size,
            "avg_range_size_with_mean": average_range_size_with_mean,
            "acc_range_size": accumulated_range_size,
            "avg_max_range": average_max_range
        }
        statistics.append(d)

    return statistics


def my_mean(vector):
    accumulated = 0.0
    for v in vector:
        accumulated += v

    return accumulated / float(len(vector))


def my_std_dev(mv, mean):
    sum = 0.0
    for v in mv:
        diff = v - mean
        sum += (diff ** 2)
    import math
    return math.sqrt(sum / float(len(mv)))


def get_average_range_size(ranges):
    sizes = []
    for r in ranges:
        sizes.append(math.fabs(r[0] - r[1]))

    return my_mean(sizes)


def get_ranges(mv):
    ranges = []
    if mv[0] < mv[1]:
        up = True
        down = False
        minimum = mv[0]
        maximum = mv[1]
    else:
        up = False
        down = True
        minimum = mv[1]
        maximum = mv[0]

    for v in mv[2:]:
        if down and v < minimum:
            minimum = v
        elif up and v > maximum:
            maximum = v
        elif down and v > minimum:
            down = False
            up = True
            range = (maximum, minimum)
            ranges.append(range)
            maximum = v
        elif up and v < maximum:
            down = True
            up = False
            range = (minimum, maximum)
            ranges.append(range)
            minimum = v

    return ranges
