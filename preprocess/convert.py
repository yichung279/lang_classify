from pydub import AudioSegment
from glob import glob

def convert2wav(filename, type='wav'):
    if 'wav' == type:
        sound = AudioSegment.from_wav(filename)
    elif 'mp3' == type:
        sound = AudioSegment.from_mp3(filename)
    sound = sound.set_frame_rate(16000)
    sound = sound.set_channels(1)

    # wavfilename = filename.replace('download', 'normalized_sound')
    # wavfilename = wavfilename.replace('A2/A2_', '')
    # wavfilename = wavfilename.replace('mp3', 'wav')
    # print(filename, wavfilename , sound.frame_rate)
    # sound.export(wavfilename, format="wav")
    sound.export('16kHzmono.wav', format="wav")

if "__main__" == __name__:
    # filenames = glob(r'download/**/*.mp3', recursive=True)
    # for filename in filenames:
    #     convert2wav(filename, 'mp3')
    #
    # filenames = glob(r'download/**/*.wav', recursive=True)
    # for filename in filenames:
    #     convert2wav(filename, 'wav')
    convert2wav('website/test.wav', 'wav')
