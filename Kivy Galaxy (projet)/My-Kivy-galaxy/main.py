# Project "GALAXY" - version 3 - MAIN
from kivy.core.audio import SoundLoader
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Quad, Triangle
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.utils import platform
from kivy.app import App
from kivy.properties import NumericProperty, Clock, ObjectProperty, StringProperty, BooleanProperty
from kivy.core.window import Window
import time

""" MAIN WIDGET """

Builder.load_file("menu.kv")


class MainWidget(RelativeLayout):
    ## Imports variables and functions from local files (c'est le prix à payer... pas top!)
    from ui_on_events import on_request_close, on_keyboard_closed, on_keyboard_down, on_keyboard_up, on_parent, on_size, \
        on_touch_up, on_touch_down
    from ui_game_grid import init_vertical_lines, init_horizontal_lines, update_lines, compute_perspective_vlines, \
        compute_perspective_hlines, update_offsets, V_NBR_LINES, vertical_lines, H_NBR_LINES, horizontal_lines, \
        SPEED_FPS, Y_POS_PERSPECTIVE, \
        V_SPC_LINES, H_SPC_LINES, init_ship, update_ship, SHIP_WIDTH, SHIP_HEIGHT, SHIP_BASE_Y, \
        check_ship_on_path_tiles, check_ship_points_in_tile
    from ui_game_grid import current_offset_x, current_offset_y, IS_PERSPECTIVE, NBR_FACTOR_PERSPECTIVE, \
        POW_FACTOR_PERSPECTIVE, SPEED_Y, SPEED_X, game_level
    from ui_game_grid import speed_touch
    from debug import IS_DEBUG_ENABLE, debug_factors_y, debug_dt, debug_speed_factor, debug_offset_y, debug_and_tune
    from ui_game_ground import init_tiles, update_tiles, NBR_INIT_TILES, tiles_quad, tiles_coordinates, \
        compute_tile_point_corner, generate_new_tiles_game_path


    """ Main variables """

    delta_x_size = 400  # parameter to increase or decrease the default app screen size
    delta_y_size = 0  # parameter to increase or decrease the default app screen size
    score_game = 0  # parameter to keep the score
    state_game_over = False  # state to know if the game is over
    state_game_start = False  # state to know if the game has started
    ship_color_rgb = (1, 0, 1)

    audio_begin = None # audio/begin.wav
    audio_galaxy = None # audio/galaxy.wav
    audio_impact = None # audio/gameover_impact.wav
    audio_gameover = None # audio/gameover_voice.wav
    audio_music_bg = None # audio/music1.wav
    audio_restart = None # audio/restart.wav

    """ Kivy GUI properties """

    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)
    ship = ObjectProperty()  # ship object
    menu_start = ObjectProperty()
    label_menu_message = StringProperty("G   A   L   A   X   Y")
    label_button_message = StringProperty("START")
    menu_button_state = BooleanProperty(False)
    label_score = StringProperty("")
    label_parameters = StringProperty("")

    """ Kivy GUI Constructor """

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_window_size()
        Window.bind(on_request_close=self.on_request_close)
        self.init_audio_files()
        self.init_vertical_lines()
        self.init_horizontal_lines()
        #self.init_tiles()
        self.init_ship()  # must be called after init_tiles to be visible !

        # add keyboard bindings
        if self.is_desktop_platform():
            self._keyboard = Window.request_keyboard(self.on_keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)
        # start the clock for update
        Clock.schedule_interval(self.update, 1 / self.SPEED_FPS)
        print(f"Clock started... \nStates: game_start={self.state_game_start} , game_over={self.state_game_start}")

    """ 
        Identifying the current operating system 
        Kivy can detect various OS : ‘win’, ‘linux’, ‘android’, ‘macosx’, ‘ios’ or ‘unknown’
    """

    def is_desktop_platform(self):
        print(f"is_desktop_platform - running on {platform}")
        if platform in ('win', 'linux', 'macosx'):
            return True
        return False


    """ Initialize the window size on start-up """
    def init_window_size(self):
        Window.size = (Window.size[0] + self.delta_x_size, Window.size[1] + self.delta_y_size)
        Window.left = Window.left - (self.delta_x_size / 2)
        Window.top = Window.top - (self.delta_y_size / 2)

    """ Initialize the audio files """
    def init_audio_files(self):
        # load audio files
        self.audio_begin = SoundLoader.load("audio/begin.wav")
        self.audio_galaxy = SoundLoader.load("audio/galaxy.wav")
        self.audio_impact= SoundLoader.load("audio/gameover_impact.wav")
        self.audio_gameover = SoundLoader.load("audio/gameover_voice.wav")
        self.audio_music_bg = SoundLoader.load("audio/music1.wav")
        self.audio_restart = SoundLoader.load("audio/restart.wav")
        # adjust audio volume
        self.audio_begin.volume = 0.25
        self.audio_galaxy.volume = 0.25
        self.audio_impact.volume = 0.70
        self.audio_gameover.volume = 0.40
        self.audio_music_bg.volume = 0.60
        self.audio_restart.volume = 0.25

    """ UPDATE LINES & OFFSET_X & OFFSET_Y & TILES & SHIP COLLISION """

    def update(self, dt):
        spacing_x = self.V_SPC_LINES * self.width  # spacing_x is a % of the width (not of V_NBR_LINES)
        spacing_y = self.H_SPC_LINES * self.height  # spacing_y is a % of the height (not of H_NBR_LINES)
        speed_factor = dt * self.SPEED_FPS  # clock speed_factor value has a value around ~1.0

        # Update the lines of the grid
        self.update_lines(spacing_x, spacing_y)

        # Update the tiles for the ground
        self.update_tiles(self.score_game)
        self.label_score = "SCORE: " + str(self.score_game)
        self.label_parameters = "LEVEL:" + str(self.game_level) + "\nSPEED: X=" + str(round(self.SPEED_X,1)) + "\n             Y=" + str(round(self.SPEED_Y,1))

        if not self.state_game_over and self.state_game_start:
            # Start music un background
            if self.audio_music_bg.state == "stop":
                self.audio_music_bg.play()

            # Update the offsets for X and Y animations of the grid
            self.update_offsets(speed_factor, spacing_y)

            if not self.check_ship_on_path_tiles(spacing_y):
                # Stop music un background
                self.audio_music_bg.stop()
                # Game over as the ship quit the path of tiles
                self.on_game_over()

        """
        if self.state_game_over:
            # Rotate the game => effect...
            time.sleep(0.25)
            self.parent.parent.rotation += 90
        """

        if self.IS_DEBUG_ENABLE:
            print(f"DEBUG - update: speed_factor={round(speed_factor, 2)} - dt={round(dt, 2)} ")
            print(f"DEBUG - update: game_over={self.state_game_over} - 1/SPEED_FPS={round(1 / self.SPEED_FPS, 2)}")
            self.debug_dt.append(dt)
            self.debug_speed_factor.append(speed_factor)


    """ ON GAME OVER """

    def on_game_over(self):
        self.audio_impact.play()
        time.sleep(1.0)
        self.audio_gameover.play()
        self.state_game_over = True
        message_game_over = "GAME   OVER"
        print(f"on_game_over: {message_game_over} - SCORE: {self.score_game}")
        self.label_menu_message = message_game_over
        self.label_button_message = "RESTART"
        print(f"on_game_over -> reset_board_game() called")
        self.reset_board_game()


    """ MENU - START BUTTON """

    def on_start_button(self):
        self.menu_start.opacity = 0  # menu invisible
        self.menu_button_state = True  # menu button disabled
        self.opacity = 1 # board game visible
        self.score_game = 0
        # rebuild the board game
        for e in self.canvas.children:
            if type(e) is Color:
                e.rgba = (1,1,1,1)
            if type(e) is Quad:
                e.points = [0, 0, 0, 0, 0, 0, 0, 0]
        self.init_tiles()
        self.init_ship()
        self.update_ship()
        # play voice begin or restart
        if self.state_game_over:
            self.audio_restart.play()
        else:
            self.audio_begin.play()
        time.sleep(0.5)
        # resume the states for starting
        self.state_game_over = False
        self.state_game_start = True


    """ RESET BOARD GAME """

    def reset_board_game(self):
        # menu setup
        self.menu_start.opacity = 1     # menu visible
        self.menu_button_state = False  # menu button enabled
        # reset variables
        self.speed_touch = 0
        self.current_offset_y = 0
        self.current_offset_x = 0
        # hide all remaining quads in memory
        self.ship.points = [0, 0, 0, 0, 0, 0]
        for e in self.canvas.children:
            if type(e) is Color:
                e.rgba = (1,1,1,0.2)
            if type(e) is Triangle:
                e.points = [0, 0, 0, 0, 0, 0]
            """    
            if type(e) is Quad:
                e.points = [0, 0, 0, 0, 0, 0, 0, 0]
            """

# GALAXY APP
class GalaxyApp(App):
    pass


# MAIN
if __name__ == '__main__':
    GalaxyApp().run()
