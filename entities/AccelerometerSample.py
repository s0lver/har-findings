class AccelerometerSample(object):
    def __init__(self, id_window, x, y, z, timestamp):
        self.id_window = id_window
        self.x = x
        self.y = y
        self.z = z
        self.timestamp = timestamp

    def __str__(self):
        return '{},{},{},{}'.format(self.id_window, self.x, self.y, self.z, self.timestamp)
