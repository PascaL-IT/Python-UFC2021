# Project "MR BEAT" - version 2 - PLAY INDICATOR
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton


class PlayIndicatorButton(ToggleButton):
    pass


class PlayIndicatorWidget(BoxLayout):

    nbr_steps = 0
    current_index = 0
    buttons = []

    def set_nbr_steps(self, nbr_steps, width):
        if nbr_steps != self.nbr_steps:
            self.nbr_steps = nbr_steps
            self.buttons.clear()
            self.clear_widgets()
            # add dummy button to be correctly aligned
            dummy_but = Button()
            dummy_but.size_hint_x = None
            dummy_but.width = width
            dummy_but.disabled = True
            self.add_widget(dummy_but)
            # rebuild layout by adding the PIBs
            for i in range(0, nbr_steps):
                tog_but = PlayIndicatorButton(text=str(i+1))
                tog_but.disabled = True
                tog_but.color=(1,1,1,0.4)
                tog_but.background_color=(0.1,0.1,0.6,.3)
                tog_but.background_disabled_down=''
                # tog_but.state = 'down' if i == 0 else 'normal'
                self.buttons.append(tog_but)
                self.add_widget(tog_but)

    def set_steps_index(self, index):
        if self.current_index != index and 0 <= index <= len(self.buttons):
            current_but = self.buttons[self.current_index]
            but = self.buttons[index]
            current_but.state = 'normal'
            but.state = 'down'
            self.current_index = index
