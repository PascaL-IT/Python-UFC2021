# Project "MR BEAT" - version 2 - AUDIO SOURCE MIXER
from array import array
from audiostream.sources.thread import ThreadSource


# Audio Source Mixer - https://audiostream.readthedocs.io/en/latest/
class AudioSourceMixer(ThreadSource):

    def __init__(self, stream_out, audio_source_tracks, fct_compute_step_nbr_frames, fct_on_step_index_changed, max_buffer, *args, **kwargs):
        ThreadSource.__init__(self, stream_out, *args, **kwargs)
        self.asts = audio_source_tracks # list with all the audio source track (i.e. ast)
        self.current_step_index = 0
        self.fct_on_step_index_changed = fct_on_step_index_changed # callback function (optional)
        self.fct_compute_step_nbr_frames = fct_compute_step_nbr_frames
        self.is_playing = False
        self.SILENCE_BUFFER = max_buffer # init to silence at a max.

    def mix_tracks_bytes(self):
        mixer_step_nbr_frames = self.fct_compute_step_nbr_frames()
        mx_buffer = self.SILENCE_BUFFER # mixer audio source buffer
        # play silence on condition (i.e. stop)
        if not self.is_playing:
            return mx_buffer[0:mixer_step_nbr_frames]
        # retrieve all the current audio stream track buffers
        track_buffers = []  # to memorise track buffers of each step
        for i in range(0, len(self.asts)):
            track_buf = self.asts[i].stream_track_buffer(mixer_step_nbr_frames)
            track_buffers.append(track_buf)
        # mix by summing each frame of each buffer
        sum_buffers = map(sum_16, zip(*track_buffers))
        mx_buffer = array('h', sum_buffers)
        # update ui step index via callback function
        self.fct_on_step_index_changed(self.current_step_index)
        # increment step index
        self.current_step_index += 1
        if self.current_step_index >= self.asts[0].nbr_steps:
            self.current_step_index = 0  # reset for looping back to the first step

        return mx_buffer[0:mixer_step_nbr_frames]

    def get_bytes(self):
        return self.mix_tracks_bytes().tostring()

    def play_stop_toggle(self):
        self.is_playing = not self.is_playing
        return self.is_playing


# sum_a6 (static function to sum with saturation)
def sum_16( n):
    value = sum(n)
    if value > 32767:
        value = 32767  # Max. to avoid overflow on 16-bits
    elif value < -32768:
        value = -32768  # Min. to avoid overflow on 16-bits
    return value
    """        
    Rem. SHRT_MAX: https://stackoverflow.com/questions/2308247/find-maximum-signed-short-integer-in-python
    """
