# Project "MR BEAT" - version 2 - AUDIO SOURCE TRACK
from audiostream.sources.thread import ThreadSource


# Audio Source Track - https://audiostream.readthedocs.io/en/latest/
class AudioSourceTrack(ThreadSource):

    def __init__(self, stream_out, wav_file, steps, max_buffer, *args, **kwargs):
        ThreadSource.__init__(self, stream_out, *args, **kwargs)
        self.current_step_index = 0
        self.current_frame_index = 0
        self.wav_file = wav_file
        self.input_frames = wav_file.get_audio_frames()
        self.nbr_input_frames = len(self.input_frames)
        self.steps = steps # list of 0|1 (i.e. normal/inactive|down/active toggle button)
        self.nbr_steps = len(steps)
        self.last_pos = - self.nbr_input_frames  # fix bug - avoid play a wav at start (solution 1)
        self.track_buffer = max_buffer

    def stream_track_buffer(self, step_nbr_frames):
        for i in range(0, step_nbr_frames):
            if len(self.steps) > 0 and not self._is_no_step_activated():
                # play the sound if step is enabled (1 = active) and not at the end of the wav
                if self.steps[self.current_step_index] == 1 and i < self.nbr_input_frames:
                    self.track_buffer[i] = self.input_frames[i]
                    if i == 0:
                        self.last_pos = self.current_frame_index
                # play with silence or continue with remaining frames
                else:
                    wav_index = self.current_frame_index - self.last_pos
                    if wav_index < self.nbr_input_frames:
                        self.track_buffer[i] = self.input_frames[wav_index]
                    else:
                        self.track_buffer[i] = 0
            # play with silence if no step
            else:
                self.track_buffer[i] = 0
            # increment frame index to keep track of where we are
            self.current_frame_index += 1
        # increment step index
        self.current_step_index += 1
        if self.current_step_index >= len(self.steps):
            self.current_step_index = 0  # reset for looping

        return self.track_buffer[0:step_nbr_frames]

    def _is_no_step_activated(self):
        for i, s in enumerate(self.steps):
            if s == 1:
                return False
        return True

    def get_bytes(self):
        return self.stream_track_buffer().tostring()  # buffer as a string (see audiostream spec)

    def update_step(self, step_index, new_value):
        previous_value = self.steps[step_index]
        if previous_value != new_value:
            self.steps[step_index] = new_value
        # print(f"AudioSourceTrack: update_step -> steps={self.steps}")
