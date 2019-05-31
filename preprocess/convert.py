from scipy.io import wavfile
from pydub import AudioSegment
from glob import glob

def convert2wav(filename):
    sound = AudioSegment.from_wav(filename)
    # sound = AudioSegment.from_mp3(filename)
    sound =sound.set_frame_rate(8192)
    sound = sound.set_channels(1)

    wavfilename = filename.replace('Chinesee', 'Chinese')
    sound.export(wavfilename, format="wav")

if "__main__" == __name__:
    filenames = glob(r'wav/Chinesee/*.wav', recursive=True)
    for filename in filenames:
        convert2wav(filename)
