from glob import glob
import matplotlib.pyplot as plt
import numpy as np
import random
import re
from scipy.io import wavfile

def gen_spectrogram(filename):
    sample_rate, samples = wavfile.read(filename)
    spectrogram, fs, t, im = plt.specgram(samples, Fs=sample_rate, NFFT=512, noverlap=256 , scale='dB')

    spectrogram , _ = np.split(spectrogram, [256], axis=0)
    return np.log1p(spectrogram_resize)

def get_lang(filename):
    m = re.match(r'\./normalized_sound/([a-zA-Z]+)/.*\.wav', filename)
    if 1 != len(m.groups()): return -1

    if 'Taiwanese' == m.group(1):
        return 0
    elif 'Chinese' == m.group(1):
        return 1
    elif 'English' == m.group(1):
        return 2

    return -1

if "__main__" == __name__:
    filenames = glob(r'./normalized_sound/**/*.wav', recursive=True)

    spectrogram_list = []
    # spectrogram = {
    #     'x': x, # spectrogram (512*256)
    #     'y': y, # 0 -> Taiwanese, 1 -> Chinese, 3->English
    # }
    for filename in filenames:
        y = get_lang(filename)
        if -1 == y: continue
        spectrogram = gen_spectrogram(filename)
        print(filename)
        n_spec = 0
        while 0 < spectrogram.shape[1] :
            x, spectrogram = np.split(spectrogram, [256], axis=1)
            n_spec += 1
            if 1 == y and n_spec == 1: continue
            spectrogram_list.append({"x":x, "y":y})

    t_count = 0
    c_count = 0

    for spectrogram in spectrogram_list:
        if 0 == spectrogram['y']:
            t_count += 1
        elif 1 == spectrogram['y']:
            c_count += 1

    print(t_count, c_count)
    random.shuffle(spectrogram_list)
    length = len(spectrogram_list)
    print(length)

    for i in range(12):
        train = spectrogram_list[int(i * length / 20):int((i+1) * length / 20)]
        np.save('feature/train_%s.npy'%i, train)
    for i in range(4):
        train = spectrogram_list[int((i+12) * length / 20):int((i+13) * length / 20)]
        np.save('feature/valid_%s.npy'%i, train)
    for i in range(4):
        train = spectrogram_list[int((i+16) * length / 20):int((i+17) * length / 20)]
        np.save('feature/test_%s.npy'%i, train)
