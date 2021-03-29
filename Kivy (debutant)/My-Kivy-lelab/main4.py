# Kivy Le Lab4 App (Python application built with Kivy) - Niveau de intermédiaire #4
# Canvas
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager
#from canvas_sample import CanvasExample1
#from canvas_sample import CanvasExample2
#from canvas_sample import CanvasExample3
from canvas_sample import *
from layouts import MainPageLayout


class ScreenManagerPushPop(ScreenManager):

    screen_stack = []

    def push(self, screen_name):
        if self.current not in self.screen_stack: # CONTROL
            self.screen_stack.append(self.current)  # add current
            self.transition.direction = "left"
            self.current = screen_name              # assign new

    def pop(self):
        if len(self.screen_stack) > 0 :                  # CONTROL
            last_screen_name = self.screen_stack[-1]     # retrieve new (last of the stack)
            # del self.screen_stack[-1]                   # delete last one
            self.screen_stack.pop()                      # delete last one
            self.transition.direction = "right"
            self.current = last_screen_name              # assign new


#Menu with Tabbed Panel for Layouts
class MyStackedScreenManagerWithMenuAndTabs(ScreenManagerPushPop):
      pass


class LeLab4App(App):

    manager = ObjectProperty(None)   # global var.

    def build(self):
        # return CanvasExample1()
        # return CanvasExample2()
        # return CanvasExample3()
        # return CanvasExample4()
        # return CanvasExample5()
        # return CanvasExample6()
        # return CanvasExample7()
        # return MainPageLayout()
        self.manager = MyStackedScreenManagerWithMenuAndTabs()  # add menu canvas - 270
        return self.manager

# MAIN3 - RUN APP
LeLab4App().run()
