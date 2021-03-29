# Kivy Le Lab2 App (Python application built with Kivy) - Niveau de intermédiaire #2
from kivy.app import App
#from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty


class MainWidget(GridLayout):

    counter = 0
    # flag = False
    flag = BooleanProperty(False)
    text_label = StringProperty("Compteur = " + str(counter))
    # slider_text = StringProperty("")
    text_input = StringProperty("")

    def on_button_click(self):
        # print("Button click")
        if self.flag:
            self.counter += 1
            self.text_label = "" + str(self.counter)

    def on_togglebutton_state(self, widget):
        # print("Button toggle state: " + widget.state)
        if (widget.state == "normal"):
            widget.text = "OFF"
            self.flag = False
        else:
            widget.text = "ON"
            self.flag = True

    def on_switch_active(self, widget):
        print("Switch state: "+ str(widget.active))

    # def on_slider_value(self, widget):
    #    #print("Slider value: " + str(int(widget.value) ))
    #    self.slider_text = str(int(widget.value))

    def on_txt_validated(self, widget):
        self.text_input = widget.text



class LeLab2App(App):
    pass

# MAIN2 - RUN APP
LeLab2App().run()
