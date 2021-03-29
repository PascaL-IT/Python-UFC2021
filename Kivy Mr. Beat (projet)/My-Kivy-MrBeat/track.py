# Project "MR BEAT" - version 2 - TRACK WIDGET
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton


# TRACK STEP BUTTON @ TOGGLEBUTTON
class TrackStepButton(ToggleButton):

    def __init__(self, wav_name, step_index, update_step, **kwargs):
        super(Button, self).__init__(**kwargs)
        self.text = "" # str(step_index)
        self.step_index = step_index
        self.name = wav_name
        self.fct_update_step = update_step
        self.state = 'normal'  # 'normal' (0=disabled) or 'down' (1=enabled)

    #def on_press(self):
    #    print(f"TrackStepButton - on_press[{self.index}]")

    #def on_release(self):
    #    print(f"TrackStepButton - on_release[{self.index}]")

    def on_state(self, widget, value):
        #print(f"DEBUG - TrackStepButton - on_state[{self.step_index}]: value={value}")
        new_value = 1 if value == 'down' else 0
        self.fct_update_step(self.name, self.step_index, new_value)


# TRACK SOUND BUTTON @ BUTTON
class TrackSoundButton(Button):

    def __init__(self, name, play_wav, width, **kwargs):
        super(Button, self).__init__(**kwargs)
        self.text = name
        self.width = width
        self.fct_play_wav = play_wav

    def on_press(self):
        self.fct_play_wav(self.text)  # i.e. sks.play_way(self.text)


# TRACK WIDGET
class TrackWidget(BoxLayout):

    def __init__(self, sound, sks, width, **kwargs):
        super(TrackWidget, self).__init__(**kwargs)
        self.add_widget(TrackSoundButton(sound.displayname, sks.play_wav, width))  # add a Track Sound Button with a width

        for i in range(0, sks.get_nbr_steps()):
            self.add_widget(TrackStepButton(sound.displayname, i, sks.update_step))  # add Track Step Buttons

        # Obsolete by mixer
        #  sks.create_track(sound.displayname, sks.get_bpm(), NBR_STEPS_PER_TRACK) - obsoleted by create_mixer