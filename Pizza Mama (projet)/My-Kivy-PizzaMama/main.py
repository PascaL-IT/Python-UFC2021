# Python application - "Pizza V1"
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview import RecycleView
from models import *


class MainWidget(FloatLayout):

    recycleView = ObjectProperty(None)

    def __init__(self, **kvargs):
        super(MainWidget, self).__init__(**kvargs)
        # see https://www.forketers.com/italian-pizza-names-list/
        self.pizzas_list = [
            Pizza("Margherita", "tomato, mozzarella, oregano", 8.50, True) ,
            Pizza("Quattro Stagioni", "tomato, mozzarella, mushrooms, ham, artichokes, olives, oregano", 11.40) ,
            Pizza("Quattro Formaggi", "tomato, mozzarella, parmesan, gorgonzola, oregano", 10.60, True)
        ]

    # Parent event => full layout available
    def on_parent(self, widget, parent):
        self.recycleView.data = [ pizza.get_data_dictionary() for pizza in self.pizzas_list ]


class PizzaWidget(BoxLayout):
    name = StringProperty("name")
    ingredients = StringProperty("ingredients")
    price = NumericProperty("0.0")
    vegetarian = BooleanProperty("False")


class RV(RecycleView):
    pass

with open("pizza_v1.kv", encoding='utf8') as kvfile:
    Builder.load_string(kvfile.read())

class PizzaApp(App):

    def build(self):
        print("Pizza V1")
        return MainWidget()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    PizzaApp().run()
