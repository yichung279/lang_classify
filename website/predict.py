#!/usr/bin/env python3

from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


SAMPLE_RATE = 16000

def load_data(filename):
    return AudioSegment.from_wav(filename)

def gen_feature(sound):
    sound =sound.set_frame_rate(SAMPLE_RATE)
    sound = sound.set_channels(1)
    sound = sound.get_array_of_samples()

    spectrogram, fs, t, im = plt.specgram(sound, Fs=SAMPLE_RATE, NFFT=512, noverlap=128 , scale='dB')
    spectrogram , _ = np.split(spectrogram, [256], axis=0)
    spectrogram , _ = np.split(spectrogram, [256], axis=1)
    print(spectrogram.shape)

    x = np.zeros((1, 256, 256, 1))
    x[0, :256, :256,0] = spectrogram

    return np.log1p(x)

if __name__ == '__main__':
    # filename = 'website/test.wav'
    filename = 'test.wav'

    model_path = '../models/lang_classify.h5'
    model = load_model(model_path)

    sound = load_data(filename)
    x = gen_feature(sound)
    lang = np.argmax(model.predict(x), axis=1)
    print(lang[0])
