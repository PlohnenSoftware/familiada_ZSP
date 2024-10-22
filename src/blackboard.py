import pygame
from os import path, getcwd
import sys
from prec.helpers import calc_grid_size, grid_creator_calc

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
        #Window size multiplier
        self.wsm = 70

        # Set the dimensions of the blackboard and the maximum length of an answer for those dimensions
        self.rows, self.cols = 10, 30
        self.max_ans_len = 17

        # Set the offset and spacing for the blackboard
        self.offset = 20
        self.spacing = 2

        # Initialize the blackboard containing object
        self.letter_matrix = [["" for _ in range(self.cols)] for _ in range(self.rows)]
        self.secondary_letter_matrix = self.letter_matrix.copy()

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
        self.surface = pygame.display.set_mode((self.wsm * 16, self.wsm * 9), pygame.RESIZABLE)
        pygame.display.set_caption("Familiada")
        self.program_icon = pygame.image.load(ICON_PATH)
        pygame.display.set_icon(self.program_icon)
        self.refresh()

    def refresh(self):
        pygame.event.pump()
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

    def write_hor(self, word, start_row, start_col, use_secondary=False):
        target_matrix = self.secondary_letter_matrix if use_secondary else self.letter_matrix
        letters = list(str(word))
        for i, letter in enumerate(letters):
            target_matrix[start_row][start_col + i] = letter
        self.refresh()

    def write_ver(self, word, start_row, start_col, use_secondary=False):
        target_matrix = self.secondary_letter_matrix if use_secondary else self.letter_matrix
        letters = list(str(word))
        for i, letter in enumerate(letters):
            target_matrix[start_row + i][start_col] = letter
        self.refresh()

    def write_matrix(self, content, start_row, start_col, matrix_height, matrix_width, use_secondary=False):
        # Determine which matrix to write to
        target_matrix = self.secondary_letter_matrix if use_secondary else self.letter_matrix

        # Convert content to a list of characters
        content_list = list(str(content))

        # Check if the dimensions match the content length
        if len(content_list) != matrix_width * matrix_height:
            raise ValueError("Content length must match the dimensions of the matrix width * height")

        # Check if the dimensions and starting points are within bounds
        if start_row < 0 or start_col < 0 or start_row + matrix_height > self.rows or start_col + matrix_width > self.cols:
            raise ValueError("Specified matrix dimensions and starting points are out of bounds")

        # Fill the target matrix with the content
        index = 0
        for row in range(start_row, start_row + matrix_height):
            for col in range(start_col, start_col + matrix_width):
                target_matrix[row][col] = content_list[index]
                index += 1

        # Refresh the board
        self.refresh()

    # Fill whole board with one character
    def fill(self, char="", use_secondary=False):
        target_matrix = self.secondary_letter_matrix if use_secondary else self.letter_matrix
        for row in range(self.rows):
            target_matrix[row] = [char] * self.cols
        self.refresh()

    def big_digit(self, digit, start_row, start_col, use_secondary=False):
        digit_to_pattern_map = {
            0: "CAAADA   AA   AA   AA   AA   AFAAAE",
            1: "  A   AA    A    A    A    A    A  ",
            2: "CAAADA   A    A   A   A   A   AAAAA",
            3: "AAAAA    A   A   AA     AA   AFAAAE",
            4: "   A   AA  A A A  A AAAAA   A    A ",
            5: "AAAAAA    AAAAD    A    AA   AFAAAE",
            6: "  AA  A   A    AAAADA   AA   AFAAAE",
            7: "",
            8: "",
            9: "CAAADA   AA   AFAAAA    A   A  AA  ",
        }

        if digit not in digit_to_pattern_map:
            raise ValueError("This function only supports digits thus from 0 to 9")
        content = digit_to_pattern_map[digit]
        self.write_matrix(content, start_row, start_col, 7, 5, use_secondary)

    def show_name(self):
        self.fill()
        self.write_hor("AAACAD A  A A A  A CAD AAD CAD", 2, 0)
        self.write_hor("A  A A AGHA A A  A A A A A A A", 3, 0)
        self.write_hor("AA AAA A  A A A  A AAA A A AAA", 4, 0)
        self.write_hor("A  A A A  A A A  A A A A A A A", 5, 0)
        self.write_hor("A  A A A  A A AA A A A AAE A A", 6, 0)

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

    # Print a big x on selected row and column
    def draw_big_x(self, start_row, start_col):
        self.write_ver("DF CE", start_row, start_col)
        self.write_ver("CE DF", start_row, start_col + 2)
        self.write_hor("I", start_row + 2, start_col + 1)
