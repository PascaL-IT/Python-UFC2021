# Project "MR BEAT" - version 2 - AUDIO ENGINE
from array import array
from audiostream import get_output
from audio_source_generator import AudioSourceGenerator
from audio_source_mixer import AudioSourceMixer
from audio_source_track import AudioSourceTrack


class AudioEngine:

    NBR_CHANNELS = 1    # mono is 1, stereo is 2
    FRAME_RATE = 22050  # 22050 or 44100
    BUFFER_SIZE = 1024  # bytes
    MAX_BUFFER = array('h', bytes(2) * (10 ** 6)) # alloc tracks & mixer silence buffer at a max.

    def __init__(self):
        # Connect to output speaker
        self.output_stream = get_output(channels=self.NBR_CHANNELS, rate=self.FRAME_RATE, buffersize=self.BUFFER_SIZE, encoding=16)
        # Assign the stream to an audio source generator to consume a wav file
        self.ASG = AudioSourceGenerator(self.output_stream)
        self.ASG.start()  # thread started once !

    def get_frame_rate(self):
        return self.FRAME_RATE

    def play_sound(self, wav_file):
        self.ASG.set_wav_file(wav_file)
        print(f"play_sound: {wav_file.get_sound_details()}")

    def create_track(self, sound, bpm, nbr_steps):
        steps = [0 for s in range(0, nbr_steps)]  # initialised to 0 (normal)
        ast = AudioSourceTrack(self.output_stream, sound, steps, self.MAX_BUFFER)
        # ast.start() - obsoleted by mixer for starting all tracks in synch
        print(f"AudioEngine - create_track for sound='{sound.get_displayname()}'")
        return ast

    def create_mixer(self, wav_files, fct_compute_snf, fct_callback):
        asmx = AudioSourceMixer(self.output_stream, wav_files, fct_compute_snf, fct_callback, self.MAX_BUFFER)
        asmx.start()
        print(f"\nAudioEngine - create_mixer: mixer is started with fct_callback")
        return asmx

