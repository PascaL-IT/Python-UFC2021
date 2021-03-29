from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.vertex_instructions import Ellipse
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, Clock, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
#import time
#import threading


Builder.load_file("canvas_sample.kv")


class CanvasExample1(Widget):
        pass

class CanvasExample2(Widget):
        pass

class CanvasExample3(Widget):
        pass

class CanvasExample4(Widget):

        forward_x = True
        forward_y = True
        label = StringProperty("")

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            with self.canvas:
                Line(points=(100,100,240,250))
                Color(0,1,1,0.5)
                self.square = Rectangle(pos=(0,100),size=(100,100))
                Color(1, 0, 1, 1)
                Line(circle=(100,100,250), width=3)

        def on_slider_value(self, widget):
                print(widget.value)

        def on_button_click(self):
                x, y = self.square.pos
                h, w = self.square.size
                step_x = dp(50)
                step_y = dp(50)

                if self.forward_x:
                        diff_x = super().width - (x + w)
                        if diff_x > step_x :
                                x += step_x
                        else:
                                x += diff_x
                                print("Touch RIGHT")
                                self.forward_x = False
                # backward_x
                else:
                        diff_x = x
                        if diff_x > step_x :
                                x -= step_x
                        else:
                                x -= diff_x
                                print("Touch LEFT")
                                self.forward_x = True
                print("diff_x=", diff_x, "x=", x, "step=", step_x)

                if self.forward_y:
                        diff_y = super().height - (y + h)
                        if diff_y <= step_y :
                                y += diff_y
                                print("Touch TOP")
                                self.forward_y = False
                        else:
                                y += step_y
                # backward_y
                else:
                        diff_y = y
                        if diff_y > step_y :
                                y -= step_y
                        else:
                                y -= diff_y
                                print("Touch BOTTOM")
                                self.forward_y = True

                print("diff_y=", diff_y, "y=", y, "step=", step_y)

                self.square.pos = (x , y)  # created tuple (non mutable)
                self.label = "Screen(h,w): " + str(int(super().height)) + "x" + str(int(super().width)) + " - Pos(x,y): " + str(int(x)) + "x" + str(int(y))



class CanvasExample5(Widget):

        forward_x = True
        forward_y = True
        label = StringProperty("")
        slider_value = 1              # set to 1 per default
        event = ObjectProperty(None)

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.ball_size=dp(50)
            with self.canvas:
                Color(0,1,1,0.5)
                self.circle = Ellipse(pos=(self.center_x,self.center_y),size=(self.ball_size,self.ball_size))
            self.start()

        def start(self):
            self. event = Clock.schedule_interval(self.run, 1/self.slider_value)

        def on_size(self, *args):
            print("on_size - screen size: " + str(self.size) + " - w:" + str(self.width) + " - h:" + str(self.height) + " - center:" + str(self.center))
            #print("on_size - circle size: " + str(self.circle.size))
            # Set circle position accurate at the center
            self.circle.pos = ( self.center_x - self.circle.size[0]/2, self.center_y - self.circle.size[1]/2 )

        def on_slider_value(self, widget):
            print("Slider value: " + str(widget.value))
            self.slider_value = int(widget.value)
            # stop scheduler
            Clock.unschedule(self.event)   # https://kivy.org/doc/stable/api-kivy.clock.html
            # restart scheduler at a new speed if cursor > 0
            if self.slider_value > 0 :
                self.start()

        def run(self, dt):
            #print("run with dt=" + str(round(dt, 2)) )
            # variables
            x, y = self.circle.pos
            h, w = self.circle.size
            step_x = self.ball_size
            step_y = self.ball_size
            # forward_x
            if self.forward_x:
                    diff_x = super().width - (x + w)
                    if diff_x > step_x :
                            x += step_x
                    else:
                            x += diff_x
                            print("Touch RIGHT")
                            self.forward_x = False
            # backward_x
            else:
                    diff_x = x
                    if diff_x > step_x :
                            x -= step_x
                    else:
                            x -= diff_x
                            print("Touch LEFT")
                            self.forward_x = True
            # print("X: diff=", diff_x, "x=", x, "step=", step_x)
            # forward_y
            if self.forward_y:
                    diff_y = super().height - (y + h)
                    if diff_y <= step_y :
                            y += diff_y
                            print("Touch TOP")
                            self.forward_y = False
                    else:
                            y += step_y
            # backward_y
            else:
                    diff_y = y
                    if diff_y > step_y :
                            y -= step_y
                    else:
                            y -= diff_y
                            print("Touch BOTTOM")
                            self.forward_y = True
            # print(Y: diff=", diff_y, "y=", y, "step=", step_y)
            self.circle.pos = x,y  # created new tuple (as non mutable)
            self.label = "Screen(h,w): " + str(int(super().height)) + "x" + str(int(super().width)) + "  -  Pos(x,y): " + str(int(x)).zfill(3) + "x" + str(int(y)).zfill(3)


class CanvasExample6(Widget):
    pass


class CanvasExample7(BoxLayout):
    pass