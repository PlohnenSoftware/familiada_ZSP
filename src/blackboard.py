import pygame
# from numba import njit
from math import floor
from os import path, getcwd
import sys


# helping static functions
# @njit
def calc_grid_size(surf_h, surf_w, offset, spacing, cols, rows):
    """
    Calculate the size and position of a grid within a gray rectangle.

    Args:
        surf_h (int): Height of the surface.
        surf_w (int): Width of the surface.
        offset (int): Offset from the edges of the surface to the gray rectangle.
        spacing (int): Spacing between blocks in the grid.
        cols (int): Number of columns in the grid.
        rows (int): Number of rows in the grid.

    Returns:
        tuple: A tuple containing the following values:
            - start_x (float): The x-coordinate of the starting position of the grid.
            - start_y (float): The y-coordinate of the starting position of the grid.
            - font_size (int): The font size based on the block height.
            - block_width (float): The width of each block in the grid.
            - block_height (float): The height of each block in the grid.
            - rect_width (int): The width of the gray rectangle.
            - rect_height (int): The height of the gray rectangle.
    """
    # Calculate dimensions for the gray rectangle
    rect_width = surf_w - 2 * offset
    rect_height = surf_h - 2 * offset

    # Aspect ratios
    aspect_ratio_rect = 1.5  # 3 / 2
    aspect_ratio_grid = 2  # 16 / 8

    # Calculate the maximum possible size of the grid within the gray rectangle
    if rect_width / rect_height > aspect_ratio_grid:
        grid_width = (rect_height - 2 * offset) * aspect_ratio_grid
    else:
        grid_width = rect_width - 2 * offset
    block_width = (grid_width - (cols - 1) * spacing) / cols
    block_height = block_width * aspect_ratio_rect
    grid_height_recalc = (block_height + spacing) * rows - spacing

    # Calculate the starting position of the grid
    start_x = offset + (rect_width - grid_width) / 2
    start_y = offset + (rect_height - grid_height_recalc) / 2
    font_size = max(round(block_height * 0.8), 2)  # Font size based on block height
    return (start_x, start_y, font_size, block_width, block_height, rect_width, rect_height)


# @njit
def grid_creator_calc(spa, start_x, start_y, block_width, block_height, i, j):
    """
    Calculates the coordinates and center of a rectangle in a grid.

    Parameters:
    spa (float): The spacing between each rectangle.
    start_x (float): The starting x-coordinate of the grid.
    start_y (float): The starting y-coordinate of the grid.
    block_width (float): The width of each rectangle.
    block_height (float): The height of each rectangle.
    i (int): The row index of the rectangle in the grid.
    j (int): The column index of the rectangle in the grid.

    Returns:
    tuple: A tuple containing the x-coordinate, y-coordinate, and center coordinates of the rectangle.
    """
    rect_x = start_x + j * (block_width + spa)
    rect_y = start_y + i * (block_height + spa)
    coord_cent = (rect_x + 0.55 * block_width, rect_y + 0.5 * block_height)
    return rect_x, rect_y, coord_cent


# @njit
def calculate_coords(no_answers) -> tuple:
    """
    Calculate the coordinates based on the number of answers.

    Parameters:
    - no_answers (int): The number of answers.

    Returns:
    - tuple: A tuple containing the number of answers and the row coordinates.
    """
    row_coords = 1 + max(floor((6 - no_answers) / 2), 0)
    return no_answers, row_coords


if getattr(sys, "frozen", False):
    try:
        application_path = sys._MEIPASS
    except Exception:
        application_path = path.dirname(path.abspath(__file__))
    finally:
        CWD_PATH = getcwd()
elif __file__:
    application_path = path.abspath("./")
    CWD_PATH = application_path


def res_path(relative_path):
    return path.join(application_path, relative_path)


ICON_PATH = res_path("familiada.ico")
FONT_PATH = res_path("familiada.ttf")


class Blackboard:
    def __init__(self):
        # Initialize the blackboard containing object
        self.rows, self.cols = 10, 30
        self.letter_matrix = [["" for _ in range(self.cols)] for _ in range(self.rows)]
        self.offset = 20
        self.max_ans_len = 17
        self.spacing = 2
        self.answers_shown_final = [[True for _ in range(5)] for _ in range(2)]

        # Initialize the round variables
        self.answers = []

        # Initialize the music
        pygame.mixer.init()
        self.sounds = {
            "correct": pygame.mixer.Sound(res_path("sfx/correct.wav")),
            "wrong": pygame.mixer.Sound(res_path("sfx/incorrect.wav")),
            "dubel": pygame.mixer.Sound(res_path("sfx/dubel.wav")),
            "bravo": pygame.mixer.Sound(res_path("sfx/bravo.wav")),
            "write": pygame.mixer.Sound(res_path("sfx/write.wav")),
            "round": pygame.mixer.Sound(res_path("sfx/round_sound.wav")),
            "ending": pygame.mixer.Sound(res_path("sfx/final_ending.flac")),
            "intro": pygame.mixer.Sound(res_path("sfx/show_music.flac")),
        }

        # Initialize the blackboard window
        pygame.init()
        self.surface = pygame.display.set_mode((72 * 16, 72 * 9), pygame.RESIZABLE)
        pygame.display.set_caption("Familiada")
        self.program_icon = pygame.image.load(ICON_PATH)
        pygame.display.set_icon(self.program_icon)
        self.refresh()

    # temporary handler
    def calculate_coords(self, no_answers) -> tuple:
        return calculate_coords(no_answers)
    
    def refresh(self):
        pygame.event.get()
        # Set the background color
        self.surface.fill((0, 0, 255))  # Blue background
        # Calculate dimensions for objects
        (start_x, start_y, font_size, block_width, block_height, rect_width, rect_height) = calc_grid_size(
            self.surface.get_height(), self.surface.get_width(), self.offset, self.spacing, self.cols, self.rows
        )
        pygame.draw.rect(self.surface, (81, 81, 81), (self.offset, self.offset, rect_width, rect_height))
        # Initialize the font module and set the font size
        pygame.font.init()  # Initialize the font module
        myfont = pygame.font.Font(FONT_PATH, font_size)  # Use familiada font

        # Drawing grid and text within each block
        for i in range(self.rows):
            for j in range(self.cols):
                rect_x, rect_y, coord_cent = grid_creator_calc(self.spacing, start_x, start_y, block_width, block_height, i, j)
                pygame.draw.rect(self.surface, (0, 0, 0), (rect_x, rect_y, block_width, block_height))
                label = myfont.render(self.letter_matrix[i][j], True, (255, 255, 0))  # Render the text in yellow
                # Calculate text position to center it in the rectangle
                label_rect = label.get_rect(center=coord_cent)
                self.surface.blit(label, label_rect)  # Draw text at the calculated position

        pygame.display.update()

    def playsound(self, sound_id):
        self.sounds[sound_id].play()

    def stop_playing(self):
        pygame.mixer.fadeout(500)

    def set_global_volume(self, volume):
        for sound in self.sounds.values():
            sound.set_volume(volume)

    def set_volume(self, volume, *keys):
        for key in keys:
            if key in self.sounds:
                sound = self.sounds[key]
                sound.set_volume(volume)

    def write_hor(self, word, start_row, start_col):
        letters = list(str(word))
        for i, letter in enumerate(letters):
            self.letter_matrix[start_row][start_col + i] = letter
        self.refresh()

    def write_ver(self, word, start_row, start_col):
        letters = list(str(word))
        for i, letter in enumerate(letters):
            self.letter_matrix[start_row + i][start_col] = letter
        self.refresh()

    def write_diag(self, word, start_row, start_col, end_row, end_col):
        step_row = 1 if start_row < end_row else -1
        step_col = 1 if start_col < end_col else -1
        letters = list(str(word))
        for i, letter in enumerate(letters):
            self.letter_matrix[start_row + i * step_row][start_col + i * step_col] = letter
        self.refresh()

    def write_on_line(self, word, start_row, start_col, end_row, end_col):
        delta_x = abs(end_col - start_col)
        delta_y = abs(end_row - start_row)

        # Determine the length and verify if the word fits
        if start_row == end_row:
            length = delta_x + 1
            self.write_hor(word, start_row, start_col)
        elif start_col == end_col:
            length = delta_y + 1
            self.write_ver(word, start_row, start_col)
        elif delta_x == delta_y:
            length = delta_x + 1
            self.write_diag(word, start_row, start_col, end_row, end_col)
        else:
            raise ValueError("Line must be either horizontal, vertical, or diagonal (45 degrees)")

        if length != len(word):
            raise ValueError("Word length does not match the available space on the line")

    # Fill whole board with one character
    def fill(self, char=""):
        self.letter_matrix = [[char for _ in range(self.cols)] for _ in range(self.rows)]
        self.refresh()

    def zero(self, start_row, start_col):
        self.write_hor("CAAAD", start_row, start_col)
        self.write_ver("AAAAA", start_row + 1, start_col)
        self.write_ver("AAAAA", start_row + 1, start_col + 4)
        self.write_hor("FAAAE", start_row + 6, start_col)

    def two(self, start_row, start_col):
        self.write_hor("CAAAD", start_row, start_col)
        self.write_hor("A   A", start_row + 1, start_col)
        self.write_on_line("AAAAA", start_row + 2, start_col + 4, start_row + 6, start_col)
        self.write_hor("AAAA", start_row + 6, start_col + 1)

    def four(self, start_row, start_col):
        self.write_on_line("AAAA", start_row, start_col + 3, start_row + 3, start_col)
        self.write_ver("AAAAAA", start_row + 1, start_col + 3)
        self.write_hor("AAAAA", start_row + 4, start_col)

    def five(self, start_row, start_col):
        self.write_hor("AAAAA", start_row, start_col)
        self.write_hor("A", start_row + 1, start_col)
        self.write_hor("AAAAD", start_row + 2, start_col)
        self.write_ver("AAA", start_row + 3, start_col + 4)
        self.write_ver("A", start_row + 5, start_col)
        self.write_hor("FAAAE", start_row + 6, start_col)

    def six(self, start_row, start_col):
        self.write_hor("AA", start_row, start_col + 2)
        self.write_hor("A", start_row + 1, start_col + 1)
        self.write_hor("AAAD", start_row + 3, start_col + 1)
        self.write_ver("AAAA", start_row + 2, start_col)
        self.write_ver("AA", start_row + 4, start_col + 4)
        self.write_hor("FAAAE", start_row + 6, start_col)

    def nine(self, start_row, start_col):
        self.write_hor("CAAAD", start_row, start_col)
        self.write_ver("AA", start_row + 1, start_col)
        self.write_ver("AAAA", start_row + 1, start_col + 4)
        self.write_hor("FAAA", start_row + 3, start_col)
        self.write_hor("A", start_row + 5, start_col + 3)
        self.write_hor("AA", start_row + 6, start_col + 1)

    # Print a small x on selected row and column
    def draw_small_x(self, start_row, start_col):
        self.write_hor("Y", start_row, start_col + 1)
        self.write_hor("I", start_row + 1, start_col + 1)
        self.write_hor("X", start_row + 2, start_col + 1)
        for i in range(2):
            i = i << 1
            self.letter_matrix[start_row + i][start_col + i] = "G"
            self.letter_matrix[start_row - i + 2][start_col + i] = "H"
        self.refresh()

    # print show name
    def show_name(self, n=2):
        self.fill()
        self.write_hor("AAACAD A  A A A  A CAD AAD CAD", n, 0)
        self.write_hor("A  A A AGHA A A  A A A A A A A", n + 1, 0)
        self.write_hor("AA AAA A  A A A  A AAA A A AAA", n + 2, 0)
        self.write_hor("A  A A A  A A A  A A A A A A A", n + 3, 0)
        self.write_hor("A  A A A  A A AA A A A AAE A A", n + 4, 0)
        # Delay(2, self.fill).start()
        # Delay(3, lambda: self.two(0, 5)).start()

    # Print a big x on selected row and column
    def draw_gross_x(self, start_row, start_col):
        self.write_ver("DF CE", start_row, start_col)
        self.write_ver("CE DF", start_row, start_col + 2)
        self.write_hor("I", start_row + 2, start_col + 1)