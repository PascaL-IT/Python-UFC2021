# Project "MR BEAT" - version 2 - AUDIO SOURCE GENERATOR
from array import array
from audiostream.sources.thread import ThreadSource

# Ref. https://audiostream.readthedocs.io/en/latest/
#  audiostream.sources.thread.ThreadSource used to implement a generator that run in a thread
# Audio Source Generator is used to play the sound of one source (see Track Sound Button)


class AudioSourceGenerator(ThreadSource):

    CHUNK_NBR_SAMPLES = 32

    def __init__(self, stream_out, *args, **kwargs):
        ThreadSource.__init__(self, stream_out, *args, **kwargs)
        # Initialize the buffer with 0 (silence) - https://www.programiz.com/python-programming/methods/built-in/bytes
        self.small_buffer = array('h', bytes(2) * self.CHUNK_NBR_SAMPLES)  # e.g. 2-bytes * 32 of 0 - b"\x00\x00"
        self.input_frames = []
        self.nbr_input_frames = 0
        self.current_frame_index = 0

    def get_bytes(self):
        if self.nbr_input_frames > 0 :
            for i in range(0, self.CHUNK_NBR_SAMPLES):
                if self.current_frame_index < self.nbr_input_frames:
                    self.small_buffer[i] = self.input_frames[self.current_frame_index]
                    self.current_frame_index += 1 # increment
                else:
                    self.small_buffer[i] = 0  # reset with silence
                    # self.current_frame_index = 0  # if you want to loop on the wav file
        return self.small_buffer.tostring()


    def set_wav_file(self, wav_file):
        self.current_frame_index = 0
        self.input_frames = wav_file.get_audio_frames()
        self.nbr_input_frames = len(self.input_frames)



