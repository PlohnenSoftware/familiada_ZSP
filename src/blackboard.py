import pygame
from numba import njit
from math import floor
from threading import Timer as Delay
from os import path, getcwd
import sys

# helping static functions
@njit
def check_team_input(team):
    if team not in ("L", "R"):
        raise ValueError("A team must be either 'L' or 'R'")


@njit
def calc_grid_size(surf_h, surf_w, offset, spacing, cols, rows):
    # Calculate dimensions for the gray rectangle
    rect_width = surf_w - 2 * offset
    rect_height = surf_h - 2 * offset

    # Aspect ratios
    aspect_ratio_rect = 3 / 2
    aspect_ratio_grid = 16 / 9

    # Calculate the maximum possible size of the grid within the gray rectangle
    if rect_width / rect_height > aspect_ratio_grid:
        grid_width = (rect_height - 2 * spacing) * aspect_ratio_grid
    else:
        grid_width = rect_width - 2 * spacing
    block_width = (grid_width - (cols - 1) * spacing) / cols
    block_height = block_width * aspect_ratio_rect
    grid_height_recalc = (block_height + spacing) * rows - spacing

    # Calculate the starting position of the grid
    start_x = offset + (rect_width - grid_width) / 2
    start_y = offset + (rect_height - grid_height_recalc) / 2
    font_size = max(round(block_height * 0.8), 2)  # Font size based on block height
    return (start_x, start_y, font_size, block_width, block_height, rect_width, rect_height)


@njit
def grid_creator_calc(spa, start_x, start_y, block_width, block_height, i, j):
    rect_x = start_x + j * (block_width + spa)
    rect_y = start_y + i * (block_height + spa)
    coord_cent = (rect_x + 0.55 * block_width, rect_y + 0.5 * block_height)
    return rect_x, rect_y, coord_cent


@njit
def calculate_coords(no_answers) -> tuple:
    row_coords = 1 + max(floor((6 - no_answers) / 2), 0)
    return no_answers, row_coords

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
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
        self.fgm = True  # full game mode, turns on game logic

        # Initialize the round variables
        self.answers = []
        self.round_score = 0
        self.current_round = -1

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

    def refresh(self):
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

    # change the team thaht is winner of the roud
    def change_winner(self):
        check_team_input(self.round_winner)
        if self.round_winner == "L":
            self.round_winner = "R"
        else:
            self.round_winner = "L"

    # Write a word horizontally
    def write_hor(self, word, start_row, start_col):
        letters = list(str(word))
        for i, letter in enumerate(letters):
            self.letter_matrix[start_row][start_col + i] = letter
        self.refresh()

    # Write a word vertically
    def write_ver(self, word, start_row, start_col):
        # niewiedzeć czemu nie działa word = str(word)
        letters = list(str(word))
        for i, letter in enumerate(letters):
            self.letter_matrix[start_row + i][start_col] = letter
        self.refresh()

    # Fill whole board with one character
    def fill(self, char=""):
        self.letter_matrix = [[char for _ in range(self.cols)] for _ in range(self.rows)]
        self.refresh()

    def zero(self, start_row, start_col):
        self.write_hor("CAAAD", start_row, start_col)
        self.write_ver("AAAAA", start_row+1, start_col)
        self.write_ver("AAAAA", start_row+1, start_col+4)
        self.write_hor("FAAAE", start_row+6, start_col)

    def two(self, start_row, start_col):
        self.write_hor("CAAAD", start_row, start_col)
        self.write_hor("A   A", start_row+1, start_col)
        self.write_hor("A", start_row+2, start_col+4)
        self.write_hor("A", start_row+3, start_col+3)
        self.write_hor("A", start_row+4, start_col+2)
        self.write_hor("A", start_row+5, start_col+1)
        self.write_hor("AAAAA", start_row+6, start_col)

    def five(self, start_row, start_col):
        self.write_hor("AAAAA", start_row, start_col)
        self.write_hor("A", start_row+1, start_col)
        self.write_hor("AAAAD", start_row+2, start_col)
        self.write_ver("AAA", start_row+3, start_col+4)
        self.write_ver("A", start_row+5, start_col)
        self.write_hor("FAAAE", start_row+6, start_col)

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
    def show_name(self):
        self.fill()
        n = 2
        self.write_hor("AAACAD A  A A A  A CAD AAD CAD", n, 0)
        self.write_hor("A  A A AGHA A A  A A A A A A A", n + 1, 0)
        self.write_hor("AA AAA A  A A A  A AAA A A AAA", n + 2, 0)
        self.write_hor("A  A A A  A A A  A A A A A A A", n + 3, 0)
        self.write_hor("A  A A A  A A AA A A A AAE A A", n + 4, 0)
        Delay(2, self.fill).start()
        Delay(3, lambda: self.five(0,5)).start()

    # Print a big x on selected row and column
    def draw_gross_x(self, start_row, start_col):
        self.write_ver("DF CE", start_row, start_col)
        self.write_ver("CE DF", start_row, start_col + 2)
        self.write_hor("I", start_row + 2, start_col + 1)

    # Initialize the round printing a blank blackboard
    def round_init(self, round_number):
        self.fill()
        self.current_round = round_number
        no_answers, row_coords = calculate_coords(len(self.answers[round_number]))

        # Write the indices of the answers to the blackboard
        self.write_ver("".join([str(i) for i in range(1, no_answers + 1)]), row_coords, 4)

        # Write blank spaces to the blackboard
        for i in range(no_answers):
            self.write_hor("_" * self.max_ans_len + " --", row_coords + i, 6)

        # Write the sum
        self.write_hor("suma   0", row_coords + no_answers + 1, 18)

        for round_answers in self.answers:
            for answer in round_answers:
                answer[2] = True

        # Set the answers as not printed
        for answer_dict in self.answers[round_number]:
            answer_dict[2] = False
        # Play round SFX
        self.playsound("round")

    # Print selected answer for selected round
    def show_answer(self, round_number, answer_number):
        # Check if the answer is already printed
        if self.answers[round_number][answer_number][2]:
            return

        # Assure that the correct round is being shown
        if self.current_round != round_number:
            self.round_init(round_number)

        # Write the answer
        self.round_score = int(self.answers[round_number][answer_number][1]) + self.round_score
        no_answers, row_coords = calculate_coords(len(self.answers[round_number]))
        answer_text = str(self.answers[round_number][answer_number][0])
        answer_points = str(self.answers[round_number][answer_number][1])
        self.write_hor(answer_text.ljust(self.max_ans_len), row_coords + answer_number, 6)

        point_coor = 6 + self.max_ans_len
        self.write_hor(answer_points.rjust(2), row_coords + answer_number, point_coor + 1)
        self.write_hor(str(self.round_score).rjust(3), row_coords + no_answers + 1, point_coor)

        self.playsound("correct")

        # Set the answer as printed
        self.answers[round_number][answer_number][2] = self.correct_answer = True

    def init_final_round(self):
        self.fill()
        self.round_winner = ""
        self.round_score = 0
        self.write_hor("suma   0", 8, 10)
        for k in range(1, 6):
            self.write_hor("----------- @@|@@ -----------", k, 0)
        self.answers_shown_final = [[False for _ in range(5)] for _ in range(2)]


    def show_final_answer(self, answer_input, point_input, row, col):
        answer = str(answer_input.get())
        points = str(point_input.get())
        answer = answer.lower()

        # Check if inputs are valid
        if len(answer) > 11 or len(points) > 2 or points.isdigit() is False:
            return

        # Check if the answer is already printed
        if self.answers_shown_final[col][row]:
            return

        # Set answer as printed
        self.answers_shown_final[col][row] = True

        if col:
            answer_str = f"@@ {answer.rjust(11)}"
            output_str = f"{points.rjust(2)} {answer.rjust(11)}"
        else:
            answer_str = f"{answer.ljust(11)}"
            output_str = f"{answer.ljust(11)} {points.rjust(2)}"
        self.playsound("write")

        self.write_hor(answer_str, row + 1, col * 15)

        def show_score_for_answer():
            self.write_hor(output_str, row + 1, col * 15)
            if int(points) > 0:
                self.round_score += int(points)
                self.playsound("correct")
                self.write_hor(str(self.round_score).rjust(3), 8, 15)

            else:
                self.playsound("wrong")

        Delay(2, show_score_for_answer).start()


# corrections, adding the final card and buttons to handle, start working on the function of displaying the answers from the final,
#  correct the symbol of the small loss to a more acurate one, but by doing so, the large loss should be corrected; the function from the answers
#  in the final should be finished writing; the font should be coded from large numbers and the large title caption should be coded
