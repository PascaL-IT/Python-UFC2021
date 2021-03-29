from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
#from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.metrics import dp
from kivy.uix.pagelayout import PageLayout


Builder.load_file("layouts.kv")


class MainPageLayout(PageLayout):
    pass

class MainStackLayout(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.orientation = "rl-bt"
        # self.padding = ( "10dp" , "50dp" , "50dp" , "10dp" )
        # self.spacing = ("30dp", "30dp")

        for i in range(0, 100):
            t = "SL" + str(i+1)
            # b = Button(text=t, size_hint=(0.2,0.2))
            b = Button(text=t, size_hint=(None, None), size=( dp(50) , dp(50) ))
            self.add_widget(b)

#class MainGridLayout(GridLayout):
#    pass

class MainAnchorLayout(AnchorLayout):
    pass

class MainBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        b1 = Button(text="A")
        b2 = Button(text="B")
        self.orientation = "vertical"
        """
        self.add_widget(b1)
        self.add_widget(b2)
        """

class MainWidget(Widget):
    pass