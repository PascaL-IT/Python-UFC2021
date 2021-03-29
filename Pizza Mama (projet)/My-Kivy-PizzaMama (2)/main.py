# Python application - "Pizza V2"
from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Ellipse, Rectangle
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.text import Label as CoreLabel
from kivy.uix.progressbar import ProgressBar
from kivy.uix.recycleview import RecycleView
from kivy.uix.widget import Widget
from http_client import HttpClient
from models import Pizza
from storage_manager import StorageManager


class MainWidget(FloatLayout):

    recycleView = ObjectProperty(None)
    progressLabel = StringProperty("Please wait...")
    error_or_failure_message = StringProperty("")
    STORAGE_FILENAME = "pizzas.json"

    def __init__(self, **kvargs):
        super(MainWidget, self).__init__(**kvargs)

    def on_parent(self, widget, parent):
        print("on_parent event -> full layout available")
        pizzas_json = StorageManager().get_data(self.STORAGE_FILENAME)     # get pizzas from file
        self.recycleView.data = Pizza.build_list_data_for_rw(pizzas_json)
        HttpClient().get_pizzas(self.on_server_data, self.on_error_data, self.on_failure_data, self.on_progress_data)
        print("HttpClient().get_pizzas is called to get pizzas from web service")

    def on_server_data(self, data):
        print("on_server_data...")
        self.recycleView.data = Pizza.build_list_data_for_rw(data)
        StorageManager().store_data(self.STORAGE_FILENAME, data)

    def on_error_data(self, error_message):
        self.error_or_failure_message = error_message
        print("on_error_data : " + str(self.error_or_failure_message))

    def on_failure_data(self, failure_message):
        self.error_or_failure_message = failure_message
        print("on_failure_data : " + str(self.error_or_failure_message))

    def on_progress_data(self, ratio):
        print("ratio=" + str(round(ratio, 2)))
        if ratio == 1.0:
            self.progressLabel = ""
        else:
            self.progressLabel = str(round(ratio, 2))


class PizzaWidget(BoxLayout):
    name = StringProperty("name")
    ingredients = StringProperty("ingredients")
    price = NumericProperty("0.0")
    vegetarian = BooleanProperty("False")


class RV(RecycleView):
    pass


with open("pizza_v2.kv", encoding='utf8') as my_kvfile:
    Builder.load_string(my_kvfile.read())


# MAIN
class PizzaApp(App):

    def build(self):
        print("Pizza V2")
        return MainWidget()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    PizzaApp().run()
