# Project "GALAXY" - version 2 - UI GAME GRID
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Triangle
import math

""" UI GRID PARAMETERS """
IS_PERSPECTIVE = True  # Default is True (vs. False => 2D)
Y_POS_PERSPECTIVE = 0.75  # Y-position at a % of screen height, e.g 0.75
POW_FACTOR_PERSPECTIVE = 2  # Y-power factor of penetration, e.g. 2
NBR_FACTOR_PERSPECTIVE = 1  # start number for factor, e.g. 0.9 , 1 , 1.2

V_NBR_LINES = 16  # nbr. of lines drawn on the screen (must be an EVEN number to center the path)
V_SPC_LINES = 0.20  # spacing of vertical line in % (screen width)

H_NBR_LINES = 12  # nbr. of lines drawn on the screen
H_SPC_LINES = 0.25  # spacing of horizontal line in % (screen height)

SPEED_FPS = 75  # clock update speed, e.g. 60 FPS
SPEED_Y = 1.0  # Y-vertical speed increment, e.g. 1.0    (fct of height)
SPEED_X = 1.0  # X-horizontal speed increment, e.g. 2.0  (fct of width)

SHIP_WIDTH = 0.07  # ship width in % a % of screen width
SHIP_HEIGHT = 0.03  # ship height in % a % of screen height
SHIP_BASE_Y = 0.04  # distance of ship from the Y-bottom

""" UI GRID VARIABLES """
horizontal_lines = []  # list of horizontal lines
vertical_lines = []  # list of vertical lines
speed_touch = 0  # parameter to manage the motion on screen touch
current_offset_y = 0  # parameter to manage the grid scrolling down
current_offset_x = 0  # parameter to manage the grid moving left or right
ship = None  # ship object
ship_coordinates = []

""" Initialisation of lines (called by constructor) """


def init_vertical_lines(self):
    with self.canvas:
        Color(1, 1, 1)
        for l in range(0, self.V_NBR_LINES):
            line = Line(points=[100, 0, 100, 100], width=1)  # or simply Line()
            self.vertical_lines.append(line)
        nbr_v_lines = len(self.vertical_lines)
        if nbr_v_lines % 2 != 0:
            raise TypeError("Number of vertical lines must be an EVEN number")
        else:
            print("init_vertical_lines -> nbr. of v_lines=" + str(nbr_v_lines))


""" Initialisation of lines (called by constructor) """


def init_horizontal_lines(self):
    with self.canvas:
        Color(1, 1, 1)
        for l in range(0, self.H_NBR_LINES):
            line = Line(width=1)
            self.horizontal_lines.append(line)
        print("init_horizontal_lines -> nbr. of h_lines=" + str(len(self.horizontal_lines)))


""" Update of lines (called by on_size) """


def update_lines(self, spacing_x, spacing_y):
    # Vertical lines in 2D
    offset_x = int(self.V_NBR_LINES * 0.5) * -1  # from left and go to the right
    for l in range(0, self.V_NBR_LINES):  # update line coordinates (points)
        x1 = (self.width * 0.5) + (offset_x + 0.5) * spacing_x
        x1 += self.current_offset_x  # with X-animation (grid moving to the LEFT if positif)
        y1 = 0
        x2 = x1  # vertical line
        y2 = self.height
        self.vertical_lines[l].points = [x1, y1, x2, y2]
        offset_x += 1  # e.g (-3, -2, -1, 0, 1, 2, 3, 4) if V_NBR_LINES=8

    # Horizontal lines in 2D
    for l in range(0, self.H_NBR_LINES):  # update line coordinates (points)
        x1 = 0
        y1 = int(l * spacing_y)
        y1 += self.current_offset_y  # with Y-animation (grid moving DOWN stream)
        x2 = self.width
        y2 = y1  # horizontal line
        self.horizontal_lines[l].points = [x1, y1, x2, y2]

    # Switch between 2D and perspective view
    if self.IS_PERSPECTIVE:
        self.compute_perspective_vlines()  # Apply perspective on vertical lines
        self.compute_perspective_hlines()  # Compute perspective on horizontal lines


""" Compute vertical lines in perspective (transform from vertical to converging lines) """


def compute_perspective_vlines(self):
    for i, l in enumerate(self.vertical_lines):
        self.vertical_lines[i].points = [l.points[0], l.points[1], self.perspective_point_x,
                                         self.perspective_point_y]


""" Compute horizontal lines when in perspective (reducing the width and contracting lines near the center) """


def compute_perspective_hlines(self):
    # compute a1.x+b1 of the leftmost line
    d1x1, d1y1, d1x2, d1y2 = self.vertical_lines[0].points
    delta_x1 = d1x2 - d1x1
    a1 = (d1y2 - d1y1) / delta_x1 if delta_x1 != 0 else 0
    b1 = d1y1 - a1 * d1x1
    # compute a2.x+b2 of the far right line
    d2x1, d2y1, d2x2, d2y2 = self.vertical_lines[-1].points
    delta_x2 = d2x2 - d2x1
    a2 = (d2y2 - d2y1) / delta_x2 if delta_x2 != 0 else 0
    b2 = d2y1 - a2 * d2x1
    # for each horizontal line, compute the intersection of lines
    for i, l in enumerate(self.horizontal_lines):
        is_visible = True
        y1, y2 = l.points[1], l.points[3]
        factor_y = math.pow(self.NBR_FACTOR_PERSPECTIVE - (y1 / self.perspective_point_y),
                            self.POW_FACTOR_PERSPECTIVE)
        if factor_y < 0:
            factor_y = 0  # i.e. can happen on ODD value of POW_FACTOR_PERSPECTIVE

        y1 = y1 * (1 + factor_y)
        if y1 > self.perspective_point_y:
            y1 = self.perspective_point_y  # hidden line
            is_visible = False
        x1 = (y1 - b1) / a1 if a1 != 0 else d1x1
        y2 = y1  # as horizontal line
        x2 = (y2 - b2) / a2 if a2 != 0 else d2x1

        self.horizontal_lines[i].points = [int(x1), int(y1), int(x2), int(y2)]
        # self.horizontal_lines[i].width = 1

        if self.IS_DEBUG_ENABLE:
            self.debug_factors_y.append(factor_y)
            alpha_deg = round(math.atan(a1) * (180 / math.pi), 1)
            print(f"DEBUG - [{i}] compute_perspective_hlines: alpha={alpha_deg}°")
            print(f"DEBUG - [{i}] compute_perspective_hlines: factor_y={factor_y} is_visible={is_visible}")
            print(f"DEBUG - [{i}] compute_perspective_hlines: ({int(x1)},{int(y1)}) , ({int(x2)},{int(y2)})")


""" Update of offset x & y for animations (called by update) """


def update_offsets(self, speed_factor, spacing_y):
    # Update the current offset_x for X-grid-animation (left <-> right)
    self.current_offset_x -= self.speed_touch * speed_factor
    # Update the current offset_y to allow Y-grid-animation (up <-> down)
    self.current_offset_y -= self.SPEED_Y / 100 * self.height * speed_factor
    # Check current offset_y to allow Y-grid infinie looping
    if abs(self.current_offset_y) >= spacing_y:
        self.current_offset_y += spacing_y  # jump back to the upper line (!!! TIP !!!)
        # Update the score
        self.score_game += 1
        print(f"score_game={self.score_game}")
        # Increase list of tiles_coordinates on condition
        self.generate_new_tiles_game_path(self.score_game)


""" Build and initialise the black ship """


def init_ship(self):
    print(f"init_ship")
    with self.canvas:
        Color(0, 1, 0)
        self.ship = Triangle()


""" Update the black ship """


def update_ship(self):
    print(f"update_ship")
    x1 = self.width * 0.5 * (1 - self.SHIP_WIDTH)
    y1 = self.SHIP_BASE_Y * self.height
    x2 = self.width * 0.5
    y2 = (self.SHIP_BASE_Y + self.SHIP_HEIGHT) * self.height
    x3 = self.width * 0.5 * (1 + self.SHIP_WIDTH)
    y3 = y1
    self.ship.points = [int(x1), int(y1), int(x2), int(y2), int(x3), int(y3)]
    print(f"DEBUG - update_ship: points={self.ship.points}")


""" Check how many points of a ship are within a tile boundaries """


def check_ship_points_in_tile(self, tq, is_totally_in):
    # Retrieve tile/quad coordinates (rem. tx3 = tx4 , ty2 = ty3 , ty1 = ty4)
    tx1, ty1, tx2, ty2, tx3, ty3, tx4, ty4 = tq.points
    # Check each ship point (x,y) is in the tile area (rem. sy1 = sy3)
    result = 0
    for i in range(0, len(self.ship.points), 2):
        if is_totally_in:
            delta_xl = 10 + 3 * self.SPEED_X  # compensation add a few %errors on the righy
            delta_xr = delta_xl + 8 # compensation add a few %errors on the left (asymmetric)
        else:
            delta_xl = delta_xr = 0
        sx = self.ship.points[i]
        sy = self.ship.points[i + 1]
        if tx1 - delta_xl <= sx <= tx3 + delta_xr and ty1 <= sy <= ty3:
            result += 1  # true (+1) if point present in the tile/quad
    if self.IS_DEBUG_ENABLE:
        print(
            f"DEBUG: check_ship_points_in_tile[{i}]: {tx1 - delta_xl }<={sx}<={tx3 + delta_xr} ({tx1 - delta_xl <= sx <= tx3 + delta_xr}) {ty1}<={sy}<={ty3} ({ty1 <= sy <= ty3})")
        print(f"DEBUG: check_ship_points_in_tile - result={result} with tq={tq.points} and ship={self.ship.points}")
    return result


""" Check if ship is on path of tiles """


def check_ship_on_path_tiles(self, spacing_y, is_low_tolerance=True):
    results = []  # store booleans
    # Loop on the two bottom lines of quads
    for i, tq in enumerate(self.tiles_quad):
        # Exit loop when tile is not part of the two bottom lines
        if tq.points[3] > spacing_y * 2 + 1 :
            break
        # Check if the ship has at least one coordinates in a quad
        # print(f"DEBUG: check_ship_collision_with_tiles[{i}]")
        results.append(self.check_ship_points_in_tile(tq, is_low_tolerance))
    # Check results
    result = False
    if is_low_tolerance and sum(results) >= len(self.ship.points) / 2:
        result = True
    elif not is_low_tolerance and sum(results) >= 1:
        result = True

    if self.IS_DEBUG_ENABLE:
        print(f"DEBUG: check_ship_collision_with_tiles: low_tolerance={is_low_tolerance} , result={result} with {results}")

    return result
