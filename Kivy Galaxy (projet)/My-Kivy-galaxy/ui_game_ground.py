# Project "GALAXY" - version 2 - UI GAME GROUND
from random import randint

from kivy.core.text import Label
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Quad

""" UI TILE VARIABLES """
NBR_INIT_TILES = 9
tiles_quad = []
tiles_coordinates = []

""" Initialisation of tiles (called by constructor) """


def init_tiles(self):
    with self.canvas:
        for t in range(0, NBR_INIT_TILES):
            Color(1 - t / 5, 1 - t / 10, 1 - t / 20)
            self.tiles_quad.append(Quad())  # TODO ... ajouter une texture ou label avec n° ... ?! How to !?
        print(f"init_tiles -> nbr. of tiles={len(self.tiles_quad)}")
    self.generate_1rst_tiles_coordinates()


""" Generate Tiles Coordinates """


def generate_1rst_tiles_coordinates(self):
    for i in range(0, NBR_INIT_TILES):
        self.tiles_coordinates.append((0, i))
    print(f"generate_1rst_tiles_coordinates -> len={len(self.tiles_coordinates)} -> {self.tiles_coordinates}")


""" Generate Tiles Game Path """


def generate_new_tiles_game_path(self, y_path_step):
    # delete obsolete tiles_coordinates (i.e. having an y-value below the current y_path_step)
    for i, tc in reversed(list(enumerate(self.tiles_coordinates))):
        if tc[1] < y_path_step:
            self.tiles_coordinates.pop(i)
    # check if enough tiles already generated (condition - rule)
    last_x, last_y = self.tiles_coordinates[-1]
    if last_y - y_path_step >= self.H_NBR_LINES:
        return  # no need to create new tiles
    # generate new random tiles on conditions
    r = randint(1, 3)  # right, forward or left
    # going forward at least always up+1
    self.tiles_coordinates.append((last_x, last_y + 1))
    # if path on the left border
    if last_x < 0 and last_x == - (self.V_NBR_LINES * 0.5) + 1:
        r = 1  # go to the right (1)
    # if path on the right border
    elif last_x > 0 and last_x == self.V_NBR_LINES * 0.5 - 1:
        r = 3  # go to left (3)
    # add new tiles_coordinates depending on r value
    if r == 3:  # then go to the left and then up+1
        self.tiles_coordinates.append((last_x - 1, last_y + 1))
        self.tiles_coordinates.append((last_x - 1, last_y + 2))
    elif r == 1:  # then could go to the right and then up+1
        self.tiles_coordinates.append((last_x + 1, last_y + 1))
        self.tiles_coordinates.append((last_x + 1, last_y + 2))

    if self.IS_DEBUG_ENABLE:
        print(
            f"DEBUG: generate_tiles_game_path -> nbr. of tiles coordinates={len(self.tiles_coordinates)} -> {self.tiles_coordinates}")
        print(f"DEBUG: generate_tiles_game_path -> nbr. of quads={len(self.tiles_quad)} with r={r}")


""" Compute tile point when in 2D or perspective """


def compute_tile_point_corner(self, linev_id, lineh_id):
    # simply get y of the horizontal line
    y = self.horizontal_lines[lineh_id].points[1]
    # if y < 0: y = 0
    # then compute a2.x+b2 of the vertical line (oblique line in perspective)
    x1, y1, x2, y2 = self.vertical_lines[linev_id].points
    c2 = x2 - x1
    a2 = (y2 - y1) / c2 if c2 != 0 else 0
    b2 = y1 - a2 * x1
    # compute the intersection of the two lines
    x = (y - b2) / a2 if a2 != 0 else x1
    if self.IS_DEBUG_ENABLE:
        print(f"DEBUG - compute_tile_point: lines({linev_id},{lineh_id})=({int(x)},{int(y)})")
    return int(x), int(y)


""" Update of tiles coordinates (called by update function) """


def update_tiles(self, y_path_step):
    # quads and tiles_coordinates numbers must be the same
    diff_nbr = len(self.tiles_coordinates) - len(self.tiles_quad)
    if diff_nbr >= 0:
        for i in range(0, diff_nbr):
            self.tiles_quad.append(Quad())  # add quad
    """
    else:
        for i in range(0, abs(diff_nbr)):
            self.tiles_quad.pop(0)  # delete last quad
    diff_nbr = len(self.tiles_coordinates) - len(self.tiles_quad)
    if diff_nbr != 0:
        print(f"DEBUG - update_tiles: diff_nbr = tc - tq ={diff_nbr}")
        raise ("Technical error... (quit game - bug?)")
    """
    for i, tq in enumerate(self.tiles_quad, start=0):
        tc = self.tiles_coordinates[i]
        # Retrieve indexes of vertical and horizontal lines
        line_v_min = int(self.V_NBR_LINES * 0.5 - 1) + tc[0]
        line_h_min = tc[1] - y_path_step  # i.e. score = y_path_step
        line_v_max = line_v_min + 1
        line_h_max = line_h_min + 1
        # Check and limit computation within grid boundaries
        if line_h_max < self.H_NBR_LINES and line_v_max < self.V_NBR_LINES and line_h_min >= 0 and line_v_min >= 0:
            # Compute the four corners for the quad graphic
            x1, y1 = self.compute_tile_point_corner(line_v_min, line_h_min)
            x2, y2 = self.compute_tile_point_corner(line_v_min, line_h_max)
            x3, y3 = self.compute_tile_point_corner(line_v_max, line_h_max)
            x4, y4 = self.compute_tile_point_corner(line_v_max, line_h_min)
            # Assign tile points to (re)build the quad graphic
            tq.points = [x1, y1, x2, y2, x3, y3, x4, y4]
        else:
            tq.points = [0, 0, 0, 0, 0, 0, 0, 0]
            if self.IS_DEBUG_ENABLE:
                print(
                    f"DEBUG -  update_tiles[{i}]: TOUCH BOUNDARIES - MIN(h={line_h_min},v={line_v_min}) - MAX(h={line_h_max},v={line_v_max})")
            return  # quit loop

        if self.IS_DEBUG_ENABLE:
            print(f"DEBUG - update_tiles[{i}]: all tiles coordinates={self.tiles_coordinates}")
            print(f"DEBUG - update_tiles[{i}]: tile coordinates={tc}")
            print(f"DEBUG - update_tiles[{i}]: lines(vmin,hmin)=({line_v_min},{line_h_min})")
            print(f"DEBUG - update_tiles[{i}]: lines(vmax,hmax)=({line_v_max},{line_h_max})")
            print(f"DEBUG - update_tiles[{i}]: tile.points={tq.points}\n")
