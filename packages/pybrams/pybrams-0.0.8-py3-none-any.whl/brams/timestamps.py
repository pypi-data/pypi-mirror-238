import numpy as np

class Timestamps:

    def __init__(self, data):

        self.data = data
        
    def get_s(self):

        return np.array([x / 1e6 for x in self.data])

    def get_ms(self):

        return np.array([x / 1e3 for x in self.data])

    def get_us(self):

        return self.data

    def set_s(self, data):

        self.data = np.array([x * 1e6 for x in data])

    def set_ms(self, data):

        self.data = np.array([x * 1e3 for x in data])

    def set_us(self, data):

        self.data = data