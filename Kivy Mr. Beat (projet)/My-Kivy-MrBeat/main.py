# Project "MR BEAT" - version 3 - MAIN
from kivy.config import Config
#Config.set('graphics', 'width', '288')
#Config.set('graphics', 'height', '384')
from kivy.uix.widget import Widget

Config.set('graphics', 'minimum_width', '680')
Config.set('graphics', 'minimum_height', '400')


from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty, ColorProperty, NumericProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window

from audio_engine import AudioEngine
from soundkit_service import SoundKitService
from track import TrackWidget

Builder.load_file("track.kv")
Builder.load_file("play_indicator.kv")


# VERTICAL SPACING WIDGET
class VerticalSpacingWidget(Widget):
    pass

# MAIN WIDGET
class MainWidget(RelativeLayout):

    # MAIN UI PARAMETERS
    NBR_STEPS_PER_TRACK = 16  # number of steps on a track, e.g. 16
    NBR_STEPS_IN_GROUP = 4    # number of steps to make a group (big foot) on a track, e.g. 4
    BPM_VALUE = 115           # start number of beats per minutes, e.g. 120
    BPM_MIN_VALUE = 10         # min. beats per minutes, e.g. 0
    BPM_MAX_VALUE = 300       # max. beats per minutes, e.g. 500
    BPM_STEP_VALUE = 5        # increment value for beats per minutes, e.g. +/- 5
    DELTA_X_SIZE = 400        # parameter to increase or decrease the default app screen size
    DELTA_Y_SIZE = 0          # parameter to increase or decrease the default app screen size
    SOUND_KIT_ID = 1          # 1 (Mr beat) or 2 (Handpan Integral D notes)

    # KIVY UI PARAMETERS
    a_red_color = (1, 1, 1, 0.9)
    a_green_color = (1, 1, 1, 0.9)
    tracks_layout = ObjectProperty()
    play_indicator_widget = ObjectProperty()
    play_stop_label = StringProperty("PLAY")
    play_stop_color = ColorProperty(a_green_color)
    play_stop_bg_normal = StringProperty("images/play_button_normal.png")
    play_stop_bg_down = StringProperty("images/play_button_down.png")
    bpm_value_label = StringProperty()
    nbr_of_tracks = NumericProperty(0)

    # MAIN UI VARIABLES (fixed)
    nbr_groups = NBR_STEPS_PER_TRACK / NBR_STEPS_IN_GROUP  # nbr of groups on a track
    step_index = 0
    event_bpm_clock = None  # bpm event clock scheduler
    bpm_new_value = 0
    bpm_time_sleep = 0.2  # bpm selection reactivity
    button_width_lalign = dp(120)  # width of the left aligned buttons
    is_indicator_with_image = False # True or False

    # CONSTRUCTOR
    def __init__(self, **kwargs):
        super(RelativeLayout, self).__init__(**kwargs)
        self.init_check_params()
        self.init_window_size()
        self.AE = AudioEngine()
        self.SKS = SoundKitService(self.nbr_groups, self.AE, self.BPM_VALUE, self.NBR_STEPS_PER_TRACK, self.SOUND_KIT_ID)

    # KIVY ON EVENT FUNCTIONS
    def on_parent(self, widget, parent):
        print("on_parent - W: " + str(self.width) + " - H: " + str(self.height))
        nbr_tracks = self.SKS.get_nbr_tracks()
        self.nbr_of_tracks = nbr_tracks
        self.bpm_value_label = str(self.BPM_VALUE)
        for i in range(0, nbr_tracks):
            a_sound = self.SKS.get_sounds()[i]
            self.tracks_layout.add_widget(VerticalSpacingWidget())
            self.tracks_layout.add_widget(TrackWidget(a_sound, self.SKS, self.button_width_lalign, self.nbr_groups))
        self.tracks_layout.add_widget(VerticalSpacingWidget())
        print(f"on_parent - {nbr_tracks} tracks generated")
        self.play_indicator_widget.set_nbr_steps(self.SKS.get_nbr_steps(), self.button_width_lalign, self.is_indicator_with_image)
        print(f"\non_parent - mixer created for {self.SKS.get_nbr_tracks()} tracks with bpm={self.SKS.get_bpm()}, nbr_steps={self.SKS.get_nbr_steps()}")
        self.SKS.create_mixer(self.on_mixer_step_index_changed)

    def on_mixer_step_index_changed(self, step_index):
        self.step_index = step_index
        Clock.schedule_once(self.dt_play_indicator_widget, 0)

    def dt_play_indicator_widget(self, dt):
        self.play_indicator_widget.set_steps_index(self.step_index, self.is_indicator_with_image)

    def on_size(self, *args):
        print("\non_size -> W: " + str(self.width) + " - H: " + str(self.height))

    """ Initialize the window size on start-up """
    def init_window_size(self):
        Window.size = (Window.size[0] + self.DELTA_X_SIZE, Window.size[1] + self.DELTA_Y_SIZE)
        Window.left = Window.left - (self.DELTA_X_SIZE / 2)
        Window.top = Window.top - (self.DELTA_Y_SIZE / 2)

    def init_check_params(self):
        if not self.BPM_MIN_VALUE > 0:
            raise TypeError("BPM_MIN_VALUE must be > 0")
        if not self.BPM_STEP_VALUE > 0:
            raise TypeError(f"BPM_STEP_VALUE must be > 0 , and < { self.BPM_MAX_VALUE - self.BPM_MIN_VALUE } ")
        if not self.NBR_STEPS_PER_TRACK > 0:
            raise TypeError("NBR_STEPS_PER_TRACK must be > 0")
        if not self.BPM_MIN_VALUE < self.BPM_VALUE < self.BPM_MAX_VALUE:
            print(f"WARNING: BPM_VALUE must be between {self.BPM_MIN_VALUE} and {self.BPM_MAX_VALUE}")
            self.BPM_VALUE = self.BPM_MIN_VALUE
            print(f"         BPM_VALUE set to MIN={self.BPM_VALUE} ")

    def play_stop_audio(self):
        flag = self.SKS.get_mixer().play_stop_toggle()
        if flag:
            self.play_stop_label = "STOP"
            self.play_stop_color = self.a_red_color
            self.play_stop_bg_normal = "images/stop_button_normal.png"
            self.play_stop_bg_down = "images/stop_button_down.png"

        else:
            self.play_stop_label = "PLAY"
            self.play_stop_color = self.a_green_color
            self.play_stop_bg_normal = "images/play_button_normal.png"
            self.play_stop_bg_down = "images/play_button_down.png"

    def update_bpm(self, text_button):
        self.bpm_new_value = self.SKS.get_bpm()
        if text_button == '+':
            self.event_bpm_clock = Clock.schedule_interval(self.dt_increase_bpm, self.bpm_time_sleep)
        else:
            self.event_bpm_clock = Clock.schedule_interval(self.dt_decrease_bpm, self.bpm_time_sleep)

    def dt_increase_bpm(self, dt):
            self.bpm_new_value += self.BPM_STEP_VALUE
            if self.bpm_new_value > self.BPM_MAX_VALUE:
                self.bpm_new_value = self.BPM_MAX_VALUE
            self.bpm_value_label = str(self.bpm_new_value)

    def dt_decrease_bpm(self, dt):
            self.bpm_new_value -= self.BPM_STEP_VALUE
            if self.bpm_new_value < self.BPM_MIN_VALUE:
                self.bpm_new_value = self.BPM_MIN_VALUE
            self.bpm_value_label = str(self.bpm_new_value)

    def stop_and_change_bpm(self):
        import time
        time.sleep(self.bpm_time_sleep)  # 0.2 ... 0.4
        Clock.unschedule(self.event_bpm_clock)
        #print(f"* DEBUG - bpm_new_value={self.bpm_new_value} to set by SKS")
        self.bpm_value_label = str(self.bpm_new_value)
        self.SKS.set_bpm(self.bpm_new_value)



# MR BEAT APP
class MrBeatApp(App):
    pass


# RUN MR BEAT APP
MrBeatApp().run()
