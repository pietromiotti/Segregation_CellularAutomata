import numpy as np


class Map:
    EMPTY = -1

    def initMap(self, rows, columns):
        self.map = np.ndarray(shape=(rows,columns), dtype=int)
        self.map.fill(self.EMPTY)
        self.size = rows*columns
        self.rows = rows
        self.columns = columns
