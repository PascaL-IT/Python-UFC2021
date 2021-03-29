from kivy.core.audio import SoundLoader
from audiostream import get_output

sound = SoundLoader.load('sounds/kit1/clap.wav')

if sound:
    print("Sound found at %s" % sound.source)
    print("Sound is %.3f seconds" % sound.length)
    sound.play()

#stream = get_output(channels=1, rate=44100, buffersize=1024)
stream = get_output(channels=1, rate=22050, buffersize=512)
print(type(stream))