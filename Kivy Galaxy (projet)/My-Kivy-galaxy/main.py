# Project "GALAXY" - version 2 - MAIN
from kivy.graphics.context_instructions import Color
from kivy.utils import platform
from kivy.app import App
from kivy.properties import NumericProperty, Clock
from kivy.uix.widget import Widget
from kivy.core.window import Window

""" MAIN WIDGET """


class MainWidget(Widget):
    ## Imports variables and functions from local files (c'est le prix à payer... pas top!)
    from ui_on_events import on_request_close, on_keyboard_closed, on_keyboard_down, on_keyboard_up, on_parent, on_size, \
        on_touch_up, on_touch_down
    from ui_game_grid import init_vertical_lines, init_horizontal_lines, update_lines, compute_perspective_vlines, \
        compute_perspective_hlines, update_offsets, V_NBR_LINES, vertical_lines, H_NBR_LINES, horizontal_lines, \
        SPEED_FPS, Y_POS_PERSPECTIVE, \
        V_SPC_LINES, H_SPC_LINES, init_ship, update_ship, ship, SHIP_WIDTH, SHIP_HEIGHT, SHIP_BASE_Y, \
        check_ship_on_path_tiles, check_ship_points_in_tile
    from ui_game_grid import current_offset_x, current_offset_y, IS_PERSPECTIVE, NBR_FACTOR_PERSPECTIVE, \
        POW_FACTOR_PERSPECTIVE, SPEED_Y, SPEED_X
    from ui_game_grid import speed_touch
    from debug import IS_DEBUG_ENABLE, debug_factors_y, debug_dt, debug_speed_factor, debug_offset_y, debug_and_tune
    from ui_game_ground import init_tiles, update_tiles, NBR_INIT_TILES, tiles_quad, tiles_coordinates, \
        compute_tile_point_corner, \
        generate_1rst_tiles_coordinates, generate_new_tiles_game_path

    ## Variables
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)
    score_game = 0  # parameter to keep the score

    """ Kivy GUI Constructor """

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        Window.size = (1200, 600)
        Window.bind(on_request_close=self.on_request_close)
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.init_ship()  # after init_tiles to be visible !
        if self.is_desktop_platform():
            self._keyboard = Window.request_keyboard(self.on_keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)
        Clock.schedule_interval(self.update, 1 / self.SPEED_FPS)

    """ 
        Identifying the current operating system 
        Kivy can detect various OS : ‘win’, ‘linux’, ‘android’, ‘macosx’, ‘ios’ or ‘unknown’
    """

    def is_desktop_platform(self):
        print(f"is_desktop_platform - running on {platform}")
        if platform in ('win', 'linux', 'macosx'):
            return True
        return False

    """ UPDATE LINES & OFFSET_X & OFFSET_Y & TILES """

    def update(self, dt):
        spacing_x = self.V_SPC_LINES * self.width  # spacing_x is a % of the width (not of V_NBR_LINES)
        spacing_y = self.H_SPC_LINES * self.height  # spacing_y is a % of the height (not of H_NBR_LINES)
        speed_factor = dt * self.SPEED_FPS  # clock speed_factor value has a value around ~1.0

        # Update the lines of the grid
        self.update_lines(spacing_x, spacing_y)

        # Update the tiles for the ground
        self.update_tiles(self.score_game)

        # Update the offsets for X and Y animations of the grid
        self.update_offsets(speed_factor, spacing_y)

        # Check ship position on the path
        if not self.check_ship_on_path_tiles(spacing_y):
            message_go = "GAME OVER"
            print(message_go + " - score: " + str(self.score_game))
            raise TypeError(message_go)  # TODO ...

        if self.IS_DEBUG_ENABLE:
            print(
                f"DEBUG - update: speed_factor={round(speed_factor, 2)} - dt={round(dt, 2)} - 1/SPEED_FPS={round(1 / self.SPEED_FPS, 2)}")
            self.debug_dt.append(dt)
            self.debug_speed_factor.append(speed_factor)


# GALAXY APP
class GalaxyApp(App):
    pass


# MAIN
if __name__ == '__main__':
    GalaxyApp().run()
