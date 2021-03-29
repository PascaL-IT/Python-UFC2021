# Project "MR BEAT" - version 2 - AUDIO SOURCE MIXER
from audiostream.sources.thread import ThreadSource


# Audio Source Mixer - https://audiostream.readthedocs.io/en/latest/
class AudioSourceMixer(ThreadSource):

    mx_buffer = [] # mixer audio source buffer

    def __init__(self, stream_out, audio_source_tracks, fct_compute_step_nbr_frames, fct_on_step_index_changed, max_buffer, *args, **kwargs):
        ThreadSource.__init__(self, stream_out, *args, **kwargs)
        self.asts = audio_source_tracks # list with all the audio source track (i.e. ast)
        self.current_step_index = 0
        self.fct_on_step_index_changed = fct_on_step_index_changed # callback function (optional)
        self.fct_compute_step_nbr_frames = fct_compute_step_nbr_frames
        self.is_playing = False
        self.mx_buffer = max_buffer

    def mix_tracks_bytes(self):
        mixer_step_nbr_frames = self.fct_compute_step_nbr_frames()
        # play silence on condition (i.e. stop)
        if not self.is_playing:
            for i in range(0, mixer_step_nbr_frames):
                self.mx_buffer[i] = 0
            return self.mx_buffer[0:mixer_step_nbr_frames]
        # retrieve all the current audio stream track buffers
        track_buffers = []  # to memorise track buffers of each step
        for i in range(0, len(self.asts)):
            track_buf = self.asts[i].stream_track_buffer(mixer_step_nbr_frames)
            track_buffers.append(track_buf)
        # mix by summing each frame of each buffer
        for i in range(0, mixer_step_nbr_frames):
            self.mx_buffer[i] = 0
            for j in range(0, len(track_buffers)):
                sum_result = track_buffers[j][i] + self.mx_buffer[i]
                if sum_result > 32767 :
                    self.mx_buffer[i] = 32767  # Max. to avoid overflow on 16-bits
                elif sum_result < -32768 :
                    self.mx_buffer[i] = -32768  # Min. to avoid overflow on 16-bits
                else:
                    self.mx_buffer[i] = sum_result  # sum of each frame
                """ 
                Rem. SHRT_MAX: https://stackoverflow.com/questions/2308247/find-maximum-signed-short-integer-in-python
                """
        # update ui step index via callback function
        self.fct_on_step_index_changed(self.current_step_index)
        # increment step index
        self.current_step_index += 1
        if self.current_step_index >= self.asts[0].nbr_steps:
            self.current_step_index = 0  # reset for looping back to the first step

        return self.mx_buffer[0:mixer_step_nbr_frames]

    def get_bytes(self):
        return self.mix_tracks_bytes().tostring()

    def play_stop_toggle(self):
        self.is_playing = not self.is_playing
        return self.is_playing


