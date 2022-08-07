import pygame
import sys
import tkinter
from math import floor
from tkinter import messagebox, ttk

# The program provides a graphical interface for the game familiada.

# Game data showuld be stored in a csv file called "familiada.csv" in the same directory as the program.
# The file should contain lines of answers of every round with
# tuples of the form (word, score) all separated by commas.

# Currently all gui texts are written in Polish.

# Blackboard class containing the matrix object used to draw characters on the screen
class Blackboard:
    def __init__(self, stroke):
        self.letter_matrix = [["" for _ in range(29)] for _ in range(10)]
        self.stroke = stroke
        self.answers = []
        self.tabs = []
        self.sum = 0

    # Write a word horizontally to the matrix
    def write_hor(self, word, start_row, start_col):
        letters = list(str(word))
        for i, letter in enumerate(letters):
            self.letter_matrix[start_row][start_col + i] = letter

    # Write a word vertically to the matrix
    def write_ver(self, word, start_row, start_col):
        # niewiedzeć czemu nie działa word = str(word)
        letters = list(word)
        for i, letter in enumerate(letters):
            self.letter_matrix[start_row + i][start_col] = letter

    # Fill whole board with one character
    def fill(self, char=""):
        self.letter_matrix = [[char for _ in range(29)] for _ in range(10)]

    def draw_small_x(self, start_row, start_col):
        for i in range(3):
            self.letter_matrix[start_row + i][start_col + i] = "#"
            self.letter_matrix[start_row - i + 2][start_col + i] = "#"

    def draw_gross_x(self, start_row, start_col):
        self.draw_small_x(start_row + 1, start_col)
        for j in range(2):
            for i in range(2):
                self.write_hor("#", start_row + j * 4, start_col + i * 2)

    def show_big_x(self, team):
        if team not in ("L", "R"):
            exception = ValueError("Team must be either 'L' or 'R'")
            raise exception
        if team == "L":
            self.draw_gross_x(3, 0)
        else:
            self.draw_gross_x(3, 26)
        pygame.mixer.Sound.play(wrong_sound)

    def show_small_x(self, team):
        if team not in ("L", "R"):
            exception = ValueError("Team must be either 'L' or 'R'")
            raise exception
        if team == "L":
            self.draw_small_x(2, 0)
        else:
            self.draw_small_x(2, 26)
        pygame.mixer.Sound.play(wrong_sound)

    def calculate_coords(self, round_number):
        # Get and set some parameters of the round
        no_answers = len(self.answers[round_number])

        # Center the answers on the blackboard
        row_coords = 1 + min(floor((6 - no_answers) / 2), 0)
        return no_answers, row_coords

    def round_init(self, round_number):
        self.sum = 0
        no_answers, row_coords = self.calculate_coords(round_number)

        # Write the indices of the answers to the blackboard
        self.write_ver([str(i) for i in range(1, no_answers + 1)], row_coords, 4)

        # Write blank spaces to the blackboard
        for i in range(no_answers):
            self.write_hor("________________ --", row_coords + i, 6)

        # Write the sum
        self.write_hor("suma   0", row_coords + no_answers + 1, 17)

    # Print selected answer for selected round
    def print_answer(self, round_number, answer_number):
        self.sum = int(self.answers[round_number][answer_number][1]) + self.sum
        no_answers, row_coords = self.calculate_coords(round_number)
        self.write_hor(str(self.answers[round_number][answer_number][0]).ljust(16), row_coords + answer_number, 6)
        self.write_hor(str(self.answers[round_number][answer_number][1]).rjust(2), row_coords + answer_number, 23)
        self.write_hor(str(self.sum).rjust(3), row_coords + no_answers + 1, 22)


def exit_app(tkwindow):
    tkwindow.destroy()
    pygame.display.quit()
    pygame.quit()
    sys.exit()


# Initialize the main game object
game1 = Blackboard(20)

# Create a list containing tuples of answers and points for every round
try:
    with open("dane.csv", "r+") as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1].split(",")
            round_data = []
            for i in range(0, len(line), 2):
                round_answers = line[i]
                points = line[i + 1]
                round_data.append((round_answers, points))
            game1.answers.append(round_data)

        # Sort answers by points
        for i, round_answers in enumerate(game1.answers):
            game1.answers[i] = sorted(round_answers, key=lambda x: int(x[1]), reverse=True)
except FileNotFoundError:
    if messagebox.showerror("ERROR", "There is no file named 'dane.csv' in the current directory"):
        sys.exit()


# Create the window, saving it to a variable.
pygame.init()
surface = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Familiada")
programIcon = pygame.image.load("familiada.ico")
pygame.display.set_icon(programIcon)

# Create the second window
window1 = tkinter.Tk()
window1.title("Familiada - reżyserka")
window1.iconbitmap("familiada.ico")
window1.geometry("400x200")
window1.configure(background="#f0f0f0")
window1.protocol("WM_DELETE_WINDOW", lambda: exit_app(window1))

tabControl = ttk.Notebook(window1)
tab1 = ttk.Frame(tabControl)


label = tkinter.Label(tab1, text="usernane")
label.pack()

inputUser = tkinter.Entry(tab1)
inputUser.pack()

labelPassword = tkinter.Label(tab1, text="Password")
labelPassword.pack()

inputPassword = tkinter.Entry(tab1)
inputPassword.pack()

button = tkinter.Button(tab1, text="Go", command=lambda: pygame.mixer.Sound.play(ending_music))
button2 = tkinter.Button(tab1, text="Go", command=lambda: game1.round_init(2))
button.pack()
button2.pack()

# Show round tabs and their content on the second window
for i, round_answers in enumerate(game1.answers):
    game1.tabs.append(ttk.Frame(tabControl))
    for j, answer_tuple in enumerate(round_answers):
        answer = answer_tuple[0]
        points = answer_tuple[1]
        answer_text = f"odpowiedz:{answer} {points}"
        round_button = tkinter.Button(game1.tabs[i], text=answer_text, command=lambda round=i, answer=j: game1.print_answer(round, answer))
        round_button.pack()
    tabControl.add(game1.tabs[i], text="Round" + str(i + 1))

tabControl.add(tab1, text="SFX")
tabControl.pack(expand=1, fill="both")

# Import pygame SFX
pygame.mixer.init()
correct_sound = pygame.mixer.Sound("sfx/correct.wav")
wrong_sound = pygame.mixer.Sound("sfx/incorrect.wav")
dubel_sound = pygame.mixer.Sound("sfx/dubel.wav")
bravo_sound = pygame.mixer.Sound("sfx/bravo.wav")
ending_music = pygame.mixer.Sound("sfx/final_ending.flac")
intro_music = pygame.mixer.Sound("sfx/show_music.flac")

while True:
    surface.fill((0, 0, 255))

    # Determine responsive width and height of the rectangles
    if surface.get_width() < surface.get_height() * (192 / 108):
        block_width = (surface.get_width() - 125 - (28 * 2)) / 29
        block_height = block_width * 3 / 2

        # Move blocks to the center of the screen
        block_x = 0
        block_y = (surface.get_height() - (block_height * 10) - (9 * 2) - 100) / 2
    else:
        block_height = (surface.get_height() - 100 - (9 * 2)) / 10
        block_width = block_height * 2 / 3

        # Move blocks to the center of the screen
        block_x = (surface.get_width() - (block_width * 29) - (28 * 2) - 125) / 2
        block_y = 0

    # Draw a grey rectangle around the game board
    rectangle_rgb = (81, 81, 81)
    rectangle_width = surface.get_width() - game1.stroke * 2
    rectangle_height = surface.get_height() - game1.stroke * 2
    rectangle_dimensions = (game1.stroke, game1.stroke, rectangle_width, rectangle_height)
    pygame.draw.rect(surface, rectangle_rgb, rectangle_dimensions)

    # Anti-bug max
    letter_height = max(round(block_height * 0.75), 2)

    # Set the font
    myfont = pygame.font.Font("familiada.ttf", letter_height)

    # Draw black rectangles & letters on the surface.
    for i in range(10):
        for j in range(29):
            pos_x = block_x + 50 + (block_width + 3) * j
            pos_y = block_y + 50 + (block_height + 3) * i
            label = myfont.render(game1.letter_matrix[i][j], 1, (255, 255, 0))
            rectangle_rgb = (0, 0, 0)
            rectangle_dimensions = (pos_x, pos_y, block_width, block_height)
            pygame.draw.rect(surface, rectangle_rgb, rectangle_dimensions)
            surface.blit(label, (pos_x + block_width * 0.146, pos_y + block_height / 2 - letter_height / 2))

    # Refresh both windows
    pygame.display.update()
    window1.update()
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exit_app(window1)

            if event.type == pygame.VIDEORESIZE:
                # There's some code to add back window content here.
                surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    # Quit the game if the window is closed
    except pygame.error:
        sys.exit()
