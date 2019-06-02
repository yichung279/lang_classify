#!/usr/bin/env python3
import numpy as np
# from keras.models import Sequential
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, GlobalAveragePooling2D, Flatten, Dropout
from keras.layers.merge import concatenate
from keras.models import Model
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, TensorBoard

# import tensorflow as tf
# from keras.backend.tensorflow_backend import set_session
# config = tf.ConfigProto()
# config.gpu_options.per_process_gpu_memory_fraction = 0.45
# set_session(tf.Session(config = config))

from utils import DataLoader

def branch1(input, n_1x1):
    return  Conv2D(n_1x1, kernel_size=(1, 1), padding='same', activation='selu')(input)

def branch2(input, n_3x3r, n_3x3):
    net = Conv2D(n_3x3r, kernel_size=(1, 1), padding='same', activation='selu')(input)
    return  Conv2D(n_3x3, kernel_size=(3, 3), padding='same', activation='selu')(net)

def branch3(input, n_5x5r, n_5x5):
    net = Conv2D(n_5x5r, kernel_size=(1, 1), padding='same', activation='selu')(input)
    return  Conv2D(n_5x5, kernel_size=(5, 5), padding='same', activation='selu')(net)

def branch4(input, n_pool):
    net = MaxPooling2D(pool_size=(3, 3), strides=(1, 1), padding='same')(input)
    return  Conv2D(n_pool, kernel_size=(1, 1), padding='same', activation='selu')(net)


def inception_block(input, n_1x1, n_3x3r, n_3x3, n_5x5r, n_5x5, n_pool):
    br1 = branch1(input, n_1x1)
    br2 = branch2(input, n_3x3r, n_3x3)
    br3 = branch3(input, n_5x5r, n_5x5)
    br4 = branch4(input, n_pool)

    # channel last
    # return concatenate([br1, br2, br3, br4], axis=-1)
    return concatenate([input, br1, br2, br3, br4], axis=-1)

def build_model():
    inputs = Input(shape=(256, 256, 1))
    model = Conv2D(64, kernel_size=(5, 5), padding='same', activation='selu')(inputs)
    model = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(model)
    model = Conv2D(64, kernel_size=(1, 1), padding='same', activation='selu')(model)
    model = Conv2D(192, kernel_size=(3, 3), padding='same', activation='selu')(model)
    model = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(model)

    model = inception_block(model, 64, 96, 128, 16, 32, 32)
    model = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(model)

    model = inception_block(model, 196, 96, 208, 16, 48, 64)
    model = inception_block(model, 160, 112, 224, 24, 64, 64)
    model = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(model)

    model = inception_block(model, 128, 128, 256, 24, 64, 64)
    model = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(model)

    model = inception_block(model, 112, 144, 288, 32, 64, 64)
    model = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(model)

    model = inception_block(model, 256, 160, 320, 32, 96, 96)
    model = GlobalAveragePooling2D()(model)

    # model = Dropout(0.4)(model)
    model = Dense(2, activation='softmax')(model)

    model = Model(inputs, model)
    model.summary()

    return model

if __name__ == '__main__':
    train_size, valid_size = 4800, 3200
    batch_size = 24
    epochs = 100

    train_loader = DataLoader(file_glob_pattern = 'feature/train_*.npy', batch_size = batch_size)
    valid_loader = DataLoader(file_glob_pattern = 'feature/valid_*.npy', batch_size = batch_size)
    model_ckpt = ModelCheckpoint('./models/lang_classify.h5', verbose = 1, save_best_only = True)
    tensorboard = TensorBoard(log_dir='./logs/lang_classify', histogram_freq=0, write_graph=True, write_images=False)

    model = build_model()
    model.compile(loss = 'binary_crossentropy', optimizer = Adam(lr = 1e-4), metrics = ['accuracy'])
    model.fit_generator(train_loader, steps_per_epoch = train_size // batch_size,\
            validation_data = valid_loader, validation_steps = valid_size // batch_size,\
            epochs = epochs, callbacks = [model_ckpt, tensorboard])
