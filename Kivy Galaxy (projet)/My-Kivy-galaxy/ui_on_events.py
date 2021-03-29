# Project "GALAXY" - version 2 - UI ON EVENTS

""" On parent widget available """

def on_parent(self, widget, parent):
    print("on_parent - W: " + str(self.width) + " - H: " + str(self.height))


""" On re-size """

def on_size(self, *args):
    print("on_size -> W: " + str(self.width) + " - H: " + str(self.height) + " - R=" + str(
        round(self.height / self.width, 2)))
    self.update_ship()
    # self.perspective_point_x = self.width * 0.5                            # move in kv : X position at 50% screen width (always)
    # self.perspective_point_y = self.height * self.Y_POS_PERSPECTIVE        # move in kv : Y position at a % of screen height


""" On perspective_point_x """

def on_perspective_point_x(self, widget, parent):
    print("on_perspective_point_x -> PX: " + str(self.perspective_point_x))


""" On perspective_point_y """


def on_perspective_point_y(self, widget, parent):
    print("on_perspective_point_y -> PY: " + str(self.perspective_point_y))


""" On request close """


def on_request_close(self, *args):
    if self.IS_DEBUG_ENABLE:
        self.debug_and_tune()
    print("on_request_close -> Bye... ")
    return False


""" On touch down (click on screen) """


def on_touch_down(self, touch):
    print(f"on_touch_down -> ...")
    speed_x = self.SPEED_X / 100 * self.width
    if touch.x < self.width / 2:
        print(f"on_touch_down -> LEFT (<=) ")
        self.speed_touch -= speed_x
    else:
        print(f"on_touch_down -> RIGHT (=>) ")
        self.speed_touch += speed_x


""" On touch up (click on screen) """


def on_touch_up(self, touch):
    print(f"on_touch_up -> UP (=)")
    self.speed_touch = 0


""" On keyboard closed """


def on_keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self.on_keyboard_down)
    self._keyboard.unbind(on_key_up=self.on_keyboard_up)
    self._keyboard = None


""" On keyboard down """


def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    speed_x = self.SPEED_X / 100 * self.width
    if keycode[1] == 'left':
        print(f"on_keyboard_down -> LEFT (<=) ")
        self.speed_touch -= speed_x
    elif keycode[1] == 'right':
        print(f"on_keyboard_down -> RIGHT (=>) ")
        self.speed_touch += speed_x
    else:
        print("on_keyboard_down -> keycode=" + keycode[1])
    return True


""" On keyboard up """


def on_keyboard_up(self, keyboard, keycode):
    print(f"on_keyboard_up -> UP (=) - keycode=" + keycode[1])
    self.speed_touch = 0
    return True
