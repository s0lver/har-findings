from entities.AccelerometerSample import AccelerometerSample


class GravityFilterer(object):
    def __init__(self, accelerometer_samples):
        self._current_gravity = [0, 0, 0]
        self._accelerometer_samples = accelerometer_samples

    def filter_gravity(self):
        for sample in self._accelerometer_samples:
            self._filter_sample(sample)

    def _filter_sample(self, sample: AccelerometerSample):
        ALPHA = 0.8
        self._current_gravity[0] = ALPHA * self._current_gravity[0] + (1 - ALPHA) * sample.x
        self._current_gravity[1] = ALPHA * self._current_gravity[1] + (1 - ALPHA) * sample.y
        self._current_gravity[2] = ALPHA * self._current_gravity[2] + (1 - ALPHA) * sample.z

        sample.x -= self._current_gravity[0]
        sample.y -= self._current_gravity[1]
        sample.z -= self._current_gravity[2]
