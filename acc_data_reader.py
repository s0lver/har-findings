# The structure is:
# id_window, x, y, z, timestamp
# For instance:
# 1,-7.4529877,-6.203964,-3.3417053,1478123867539

# 1. Read data
# 2. Then plot each axis
# 3. Then plot the magnitude vector
# 4. Try to observe something
import csv
from typing import List

from entities.AccelerometerSample import AccelerometerSample


def build_sample_from_row(row):
    id_window = int(row[0])
    x = float(row[1])
    y = float(row[2])
    z = float(row[3])
    t = int(row[4])

    return AccelerometerSample(id_window, x, y, z, t)


def read_csv_acc_samples_file(file_path) -> List[AccelerometerSample]:
    samples = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        for row in reader:
            sample = build_sample_from_row(row)
            samples.append(sample)

    return samples
