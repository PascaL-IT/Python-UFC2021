# Kivy Le Lab3 App (Python application built with Kivy) - Niveau de intermédiaire #3
# Screens and navigation
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager


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


#4 - ActionBar
#class MyStackedScreenManagerWithBLwAB(ScreenManagerPushPop):
#      pass

#5 - Menu
#class MyStackedScreenManagerWithMenu(ScreenManagerPushPop):
#      pass

#6 - Menu with Tabbed Panel for Layouts
class MyStackedScreenManagerWithMenuAndTabs(ScreenManagerPushPop):
      pass

class LeLab3App(App):

    manager = ObjectProperty(None)   # global var.

    def build(self):
        # self.manager = MyStackedScreenManagerWithBLwAB()      #4
        # self.manager = MyStackedScreenManagerWithMenu()       #5
        self.manager = MyStackedScreenManagerWithMenuAndTabs()  #6
        return self.manager


# MAIN3 - RUN APP
LeLab3App().run()
