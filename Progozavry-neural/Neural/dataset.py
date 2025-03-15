import os
import sys
import numpy as np
sys.path.insert(1, '../Progozavry/')
from Utils.functions import toASCII

class Dataset:
    def __init__(self) -> None:
        self.train = []

    def load(self, directory, channel):
        y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        data = []
        labels = []

        for s in os.listdir(directory):
            if s.count('Np ') == 0:
                continue

            # Process the first segment
            tr = toASCII(s, 1, channel)
            tr2 = []
            rate = len(tr) // (512 * 512)
            for i in range(0, len(tr), rate):
                p = 0.0
                if i + rate >= len(tr):
                    rate = len(tr) - i
                for j in range(rate):
                    p += tr[i + j]
                tr2.append(p / rate)
                if len(tr2) == 512 * 512:
                    break
            data.append(tr2)
            labels.append(y[int(s[3:]) - 1])

            # Process the second segment
            tr = toASCII(s, 2, channel)
            tr2 = []
            rate = len(tr) // (512 * 512)
            for i in range(0, len(tr), rate):
                p = 0.0
                if i + rate >= len(tr):
                    rate = len(tr) - i
                for j in range(rate):
                    p += tr[i + j]
                tr2.append(p / rate)
                if len(tr2) == 512 * 512:
                    break
            data.append(tr2)
            labels.append(y[int(s[3:]) - 1])

        # Convert lists to numpy arrays and reshape
        data = np.array(data).reshape((-1, 512, 512, 1))
        labels = np.array(labels)

        self.train = (data, labels)
