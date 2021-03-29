from random import randint
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock


class MyLabel(Label):

    def on_text(self, *_):

        if self.color == [1, 1, 1, 1]:
            self.color = [1, 0, 1, 1]
        else:
            self.color = [1, 1, 1, 1]


class MainWindow(BoxLayout):

    def update_text(self, num):

        for wid in self.ids.lay.data:
            wid['text'] = num
        self.ids.lay.refresh_from_data()


class TestApp(App):

    def build(self):

        Builder.load_string(
'''
<MainWindow>:
    orientation: 'vertical'
    RecycleView:
        id: lay
        RecycleGridLayout:
            name: 'gdl'
            viewclass: 'MyLabel'
            size_hint: None, None
            height: self.minimum_height
            width: self.minimum_width
            cols: 50
            rows: 100
''')

        self.root = MainWindow()

        self.root.ids.lay.data = [ {} for num in range(5000) ]

    def on_start(self):
        Clock.schedule_interval(self.random_numbers, .2)

    def random_numbers(self, _):
        self.root.update_text(str(randint(100, 200000)))


if __name__ == '__main__':
    app = TestApp()
    app.run()

