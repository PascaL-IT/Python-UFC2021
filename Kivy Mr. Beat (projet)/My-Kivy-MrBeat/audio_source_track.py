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
        self.last_pos = - self.nbr_input_frames  # avoid playing a wav at start (solution 1 - fix bug)
        self.silence = max_buffer  # big buffer of silence

    def stream_track_buffer(self, step_nbr_frames):
        result_buffer = None
        # case 1 : if no step activated on this track -> play silence
        if self._is_no_step_activated():
            result_buffer = self.silence[0:step_nbr_frames]
        # case 2 : step activated
        elif self.steps[self.current_step_index] == 1:
            # memorise the last position of the index in the sound wav
            self.last_pos = self.current_frame_index
            # case 2.1 : with a sound longer than one step -> play sound
            if self.nbr_input_frames >= step_nbr_frames:
                result_buffer = self.input_frames[0:step_nbr_frames]
            # case 2.2 : with a sound smaller than one step -> play sound with additional silence
            else:
                silence_nbr = step_nbr_frames - self.nbr_input_frames
                result_buffer = self.input_frames[0:self.nbr_input_frames]
                result_buffer.extend(self.silence[0:silence_nbr])
        # case 3 : step inactivated
        else:
            # compute position of the index in the sound wav
            wav_index = self.current_frame_index - self.last_pos
            # case 3.0 : no remaining sound -> just play silence
            if wav_index > self.nbr_input_frames:
                result_buffer = self.silence[0:step_nbr_frames]
            # case 3.1 : but we need to play his remaining sound
            #             that is longer than one step -> play sound
            elif self.nbr_input_frames - wav_index >= step_nbr_frames:
                result_buffer = self.input_frames[wav_index:step_nbr_frames+wav_index]
            # case 3.2 : but we need to play his remaining sound
            #             that is smaller than one step -> play sound with additional silence
            else:
                silence_nbr = step_nbr_frames - self.nbr_input_frames + wav_index
                result_buffer = self.input_frames[wav_index:self.nbr_input_frames] # TODO check
                result_buffer.extend(self.silence[0:silence_nbr])
        # increment frame index to keep track of where we are (per chunk of step_nbr_frames)
        self.current_frame_index += step_nbr_frames
        # increment step index
        self.current_step_index += 1
        if self.current_step_index >= len(self.steps):
            self.current_step_index = 0  # reset for looping
        # return the resulting track buffer
        if len(result_buffer) != step_nbr_frames:
            raise EOFError(f"ERROR - result_buffer has an invalid len={len(result_buffer)} != {step_nbr_frames}")
        return result_buffer

    def _is_no_step_activated(self):
        if len(self.steps) <= 0 :
            return True
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
        #print(f"AudioSourceTrack: update_step -> steps={self.steps}")
