# Project "GALAXY" - version 3 - Main MENU
from kivy.uix.relativelayout import RelativeLayout


class MainMenu(RelativeLayout):
    pass
    """
    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super(RelativeLayout, self).on_touch_down(self)

    Rem. fuixed this error with workaround : disable button on start
    Ref. https://stackoverflow.com/questions/49896086/kivy-python3-detect-mousewheel
    """