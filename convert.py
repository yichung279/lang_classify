from pydub import AudioSegment
from glob import glob

def convert2wav(filename):
    sound = AudioSegment.from_mp3(filename)
    sound =sound.set_frame_rate(8192)
    sound = sound.set_channels(1)

    wavfilename = filename.replace('mp3', 'wav')
    sound.export(wavfilename, format="wav")

if "__main__" == __name__:
    filenames = glob(r'./mp3/**/*.mp3', recursive=True)
    for filename in filenames:
        convert2wav(filename)
