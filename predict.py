#!/usr/bin/env python3
# from scipy.io import wavfile
from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model

SAMPLE_RATE = 8192

def load_data(filename):
    return AudioSegment.from_wav(filename)

def gen_spectrogram(sound):
    sound =sound.set_frame_rate(SAMPLE_RATE)
    sound = sound.set_channels(1)
    sound = sound.get_array_of_samples()

    # sample_rate, samples = wavfile.read(filename)
    spectrogram, fs, t, im = plt.specgram(sound, Fs=SAMPLE_RATE, NFFT=1024, noverlap=256 , scale='dB')
    spectrogram , _ = np.split(spectrogram, [512], axis=0)

    spectrogram_resize = np.zeros((1, 256, 256, 1))
    length = spectrogram.shape[1]
    print(length)
    for i in range(256):
        for j in range(length):
            if 255 < j: continue
            spectrogram_resize[0][i][j][0] = (spectrogram[2*i][j]+spectrogram[2*i+1][j])/2

    return np.log1p(spectrogram_resize)

if __name__ == '__main__':
    filename = 'test.wav'

    model_path = 'models/lang_classify.h5'
    model = load_model(model_path)

    sound = load_data(filename)
    spectrogram = gen_spectrogram(sound)
    lang = np.argmax(model.predict(spectrogram), axis=1)
    print(lang[0])

