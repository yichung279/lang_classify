#!/usr/bin/env python3
import numpy as np
from glob import glob
from random import shuffle
from queue import Queue
from keras.utils import to_categorical

class DataLoader():

    def __init__(self, file_glob_pattern, batch_size, num_classes = 2):
        self.files = glob(file_glob_pattern)
        self.num_classes = num_classes
        self.batch_size = batch_size
        self.ptr = 1

        shuffle(self.files)

        self.holder = np.load(self.files[0])
        np.random.shuffle(self.holder)

    def load(self):
        chunk = np.load(self.files[self.ptr])
        np.random.shuffle(chunk)

        self.holder = np.concatenate([self.holder, chunk], axis = 0)

        self.ptr += 1

    def __iter__(self):
        return self

    def __next__(self):

        if self.holder.shape[0] < self.batch_size:
            if self.ptr >= len(self.files):
                self.ptr = 0
                shuffle(self.files)

            self.load()


        batch, self.holder = np.split(self.holder, [self.batch_size], axis = 0)

        x = []
        y = []

        for data in batch:
            x.append(data.get('x'))
            y.append(data.get('y'))

        x = np.array(x).astype(float)
        y = np.array(y).astype(float)

        return x, to_categorical(y, num_classes = self.num_classes)

if __name__ == '__main__':

    data_loader = DataLoader(file_glob_pattern = 'feature/A.train.*.npy', batch_size = 72)
    data = data_loader.__next__()
    print(np.array(data[0]).shape)
    print(np.array(data[1]).shape)

