import matplotlib.pyplot as plt
from scipy.io import wavfile

sample_rate, samples = wavfile.read('wav/Taiwanese/1.wav')
spectrogram, fs, t, im = plt.specgram(samples, Fs=sample_rate, NFFT=1024, noverlap=256 , scale='dB')

print(spectrogram.shape)
plt.show()
