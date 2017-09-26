from typing import List

import math

from entities.AccelerometerSample import AccelerometerSample


def calculate_magnitude_vector(samples: List[AccelerometerSample]):
    vector = []
    for s in samples:
        magnitude = math.sqrt((s.x ** 2) + (s.y ** 2) + (s.z ** 2))
        vector.append(magnitude)

    return vector


def normalize_time(samples: List[AccelerometerSample], factor=1000.0):
    start_time = samples[0].timestamp

    for sample in samples:
        sample.timestamp = (sample.timestamp - start_time) / factor

        # Try it without return :)
