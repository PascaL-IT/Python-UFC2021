# Project "MR BEAT" - version 3 - PLAY INDICATOR
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget


class PlayIndicatorImage(Image):
    pass


class PlayIndicatorButton(ToggleButton):
    pass


class ImageSeparator(Image):
    pass


class PlayIndicatorWidget(BoxLayout):

    nbr_steps = 0
    current_index = 0
    indicators = []

    def set_nbr_steps(self, nbr_steps, width, is_indicator_with_image):
        if nbr_steps != self.nbr_steps:
            self.nbr_steps = nbr_steps
            self.indicators.clear()
            self.clear_widgets()
            # add dummy button to be correctly aligned
            dummy_but = Widget()  # instead of Button
            dummy_but.size_hint_x = None
            dummy_but.width = width
            dummy_but.disabled = True
            self.add_widget(dummy_but)
            self.add_widget(ImageSeparator())  # add a Track Sound Button with a width
            # rebuild layout by adding the PIBs or the PIIs
            if is_indicator_with_image:
                for i in range(0, nbr_steps):
                    pii = PlayIndicatorImage()  # (source="images/indicator_light_off.png")
                    self.indicators.append(pii)
                    self.add_widget(pii)
            else:
                for i in range(0, nbr_steps):
                    pib = PlayIndicatorButton(text=str(i+1))
                    pib.disabled = True
                    pib.color=(1,1,1,0.5)  # text color is (1,1,1,0.4)
                    pib.background_color=(0, 1, 1,.5)  # bgd color is (0.1,0.1,0.6,.3)
                    pib.background_normal=''
                    pib.background_disabled_down=''
                    # tog_but.state = 'down' if i == 0 else 'normal'
                    self.indicators.append(pib)
                    self.add_widget(pib)

    def set_steps_index(self, index, is_indicator_with_image):
        if self.current_index != index and 0 <= index <= len(self.indicators):
            current_indicator = self.indicators[self.current_index]
            next_indicator = self.indicators[index]
            if is_indicator_with_image:
                current_indicator.source = "images/indicator_light_off.png"
                next_indicator.source = "images/indicator_light_on.png"
            else:
                current_indicator.state = 'normal'
                next_indicator.state = 'down'
            self.current_index = index

