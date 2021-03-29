# Project "MR BEAT" - version 2 - SOUND KIT SERVICE
import wave
from array import array


# Sound class
class Sound:

    # Sound variables
    nbr_audio_frames = 0
    __audio_frames_16bits = None
    wav_readfile = None

    def __init__(self, filename, displayname):
        self.filename = filename
        self.displayname = displayname
        self.load_wav_sound()

    def load_wav_sound(self):
        self.wav_readfile = wave.open(self.filename, mode='rb')
        self.nbr_audio_frames = self.wav_readfile.getnframes()  # see doc : https://docs.python.org/3/library/wave.html
        audio_frames_8bits = self.wav_readfile.readframes(self.nbr_audio_frames)  # output is an array of byte/8-bits
        self.__audio_frames_16bits = array('h', audio_frames_8bits)  # convert to an array of 2 bytes/16-bits
        print(f"Sound loaded : {self.get_sound_details()}")

    def get_audio_frames(self):
        if self.__audio_frames_16bits is None:
            raise EOFError("No frame available !?")
        return self.__audio_frames_16bits

    def get_filename(self):
        return self.filename

    def get_displayname(self):
        return self.displayname

    def get_sound_details(self):
        """
        print(f"name={self.get_displayname()} - number of audio channels={self.wav_readfile.getnchannels()}")   # Returns number of audio channels (1 for mono, 2 for stereo).
        print(f"name={self.get_displayname()} - sample width in bytes={self.wav_readfile.getsampwidth()}")   # Returns sample width in bytes.
        print(f"name={self.get_displayname()} - sampling frequency={self.wav_readfile.getframerate()}")   # Returns sampling frequency.
        print(f"name={self.get_displayname()} - number of audio frames={self.wav_readfile.getnframes()}")     # Returns number of audio frames.
        print(f"name={self.get_displayname()} - params={self.wav_readfile.getparams()}")      # Returns those various params
        """
        return f"name={self.get_displayname()}, file={self.get_filename()}, params={self.wav_readfile.getparams()}"


# Sound Kit generic class
class SoundKit:

    sounds = ()

    def get_nbr_of_tracks(self):
        return len(self.sounds)

    def get_wav_sounds(self):
        return self.sounds  # list, tuple

    def get_named_sounds(self):
        return { s.displayname : s for s in self.sounds } # dico of < names : sounds >

    def get_params_of_sound(self, index):
        if not (0 <= index <= self.get_nbr_of_tracks() - 1):
            raise IndexError(f"Invalid index - index must be between [0,{self.get_nbr_of_tracks() - 1}]")
        return self.sounds[index].get_params()


# Sound Kit1 class is a SoundKit by inherit
class SoundKit1(SoundKit):

    def __init__(self):
        self.sounds = (   Sound("sounds/kit1/kick.wav", "KICK")
               , Sound("sounds/kit1/clap.wav", "CLAP")
               , Sound("sounds/kit1/shaker.wav", "SHAKER")
               , Sound("sounds/kit1/snare.wav", "SNARE")
               , Sound("sounds/kit1/pluck.wav", "PLUCK")
               , Sound("sounds/kit1/bass.wav", "BASS")
               , Sound("sounds/kit1/effects.wav", "EFFECTS")
               , Sound("sounds/kit1/vocal_chop.wav", "V-CHOP")
               )


# Sound Kit2 class (Handpan Integral D notes)
class SoundKit2(SoundKit):

    def __init__(self):
        self.sounds = (   Sound("sounds/kit2/0_Ding_O.wav", "O - RE (DING)")
                        , Sound("sounds/kit2/1_La_A.wav", "1-LA (D)")
                        , Sound("sounds/kit2/2_Sib_Bb.wav", "2-Sib (Bb)")
                        , Sound("sounds/kit2/3_Do_C.wav", "3-Do (C)")
                        , Sound("sounds/kit2/4_Re_D.wav", "4-Re (D)")
                        , Sound("sounds/kit2/5_Mi_E.wav", "5-Mi (E)")
                        , Sound("sounds/kit2/6_Fa_F.wav", "6-Fa (F)")
                        , Sound("sounds/kit2/7_La_A.wav", "7-La (A)")
                    )



# Sound Kit service interface for UI calls (API)
class SoundKitService():

    source_tracks = {}  # dico
    source_tracks_mixer = None  # mixer for all tracks

    def __init__(self, audio_engine, bpm, nbr_steps):
        self.sound_kit = SoundKit1() # kit1 - default
        #self.sound_kit = SoundKit2() # kit2 - handpan
        self.audio_engine = audio_engine
        self.bpm = bpm
        self.nbr_steps = nbr_steps

    # Get number of tracks
    def get_nbr_tracks(self):
        return self.sound_kit.get_nbr_of_tracks()

    # Get number of steps per track
    def get_nbr_steps(self):
        return self.nbr_steps

    # Get list of sounds available
    def get_sounds(self):
        return self.sound_kit.get_wav_sounds()

    # Get a sound by his index in the list
    def get_sound(self, index):
        if not (0 <= index <= self.get_nbr_tracks() - 1):
            raise IndexError(f"Invalid index - index must be between [0,{self.get_nbr_tracks() - 1}]")
        return self.get_sounds()[index]

    # Get all params of a sound by his index in the list
    def get_sound_params(self, index):
        return self.sound_kit.get_params_of_sound(index)

    # Check sound name and return it if existing
    def __get_sound_exist(self, wav_name):
        sounds_dico = self.sound_kit.get_named_sounds()
        if wav_name not in sounds_dico.keys():
            raise TypeError(f"Invalid sound name '{wav_name}' - must be part of {sounds_dico.keys()}")
        return sounds_dico[wav_name]

    # Play sound by sound name
    def play_wav(self, wav_name):
        a_sound = self.__get_sound_exist(wav_name)
        self.audio_engine.play_sound(a_sound)

    # Create track for a sound name
    def create_track(self, wav_name):
        a_sound = self.__get_sound_exist(wav_name)
        ast = self.audio_engine.create_track(a_sound, self.get_bpm(), self.get_nbr_steps())
        self.source_tracks.update( { wav_name : ast } )

    # Get number of beats per minutes
    def get_bpm(self):
        return self.bpm

    # Get number of frame rate
    def get_frame_rate(self):
        return self.audio_engine.get_frame_rate()

    #Set number of beats per minutes
    def set_bpm(self, new_bpm):
        self.bpm = new_bpm

    # Update steps for each sound with new bpm
    def update_step(self, wav_name, step_index, value):
        self.__get_sound_exist(wav_name)
        ast = self.source_tracks.get(wav_name)
        ast.update_step(step_index, value)
        print(f"update_step on {wav_name} : set to {value} at index={step_index}")

    # Create mixer for all sound names
    def create_mixer(self, fct_callback):
        dico_sound = self.sound_kit.get_named_sounds()
        for key in dico_sound.keys():
            self.create_track(key)
        stmx = self.audio_engine.create_mixer(list(self.source_tracks.values()), self.compute_step_nbr_frames, fct_callback)
        self.source_tracks_mixer = stmx

    # Get mixer
    def get_mixer(self):
        return self.source_tracks_mixer

    # Compute step_nbr_frames for tracks and mixer
    def compute_step_nbr_frames(self):
        new_step_nbr_frames = int( (self.get_frame_rate() * 60) / (4 * self.get_bpm()))  # formula 1
        #  new_step_nbr_frames = int((self.frame_rate * 60 * 4) / (self.nbr_steps * self.bpm))  # formula 2
        return new_step_nbr_frames
