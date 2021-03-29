from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.gridlayout import GridLayout

Builder.load_file("widgets.kv")

class MainWidget2(GridLayout):

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