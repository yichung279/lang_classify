from pydub import AudioSegment
sound = AudioSegment.from_mp3("./mp3/Taiwanese/2.mp3")
sound =sound.set_frame_rate(8192)
sound = sound.set_channels(1)
sound.export("./wav/Taiwanese/2.wav", format="wav")
print(sound.frame_rate)
