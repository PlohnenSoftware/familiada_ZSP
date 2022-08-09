import pygame
import sys
import tkinter
import os
from math import floor
from tkinter import messagebox, ttk, filedialog
from blackboard import Blackboard as Bb

# The program provides a graphical interface for the game Familiada.

# Game data is a csv selected by the user upon startup.
# The file should contain lines of answers for round with points
# in the form of dicts {word,score} all separated by commas.

# Currently all gui texts are written in Polish.

# Blackboard class containing the matrix object used to draw characters on the screen

# Initialize the main game object
game1 = Bb(20)
game1.clear_x()

# Safely exit the program
def exit_app(tkwindow):
    tkwindow.destroy()
    pygame.display.quit()
    pygame.quit()
    sys.exit()


def terminate_error(error_description):
    if messagebox.showerror("FAMILIADA ERROR", error_description):
        sys.exit()

# Read data from the disk
current_dir = os.path.dirname(os.path.abspath(__file__))
# lepiej zrobić pulpit na start, do finalnej wersji bo jak sie d exe spakuje to wywala do jakiegoś folderu temp,
# gdzie jest interpreter pythona przenosny z Pyinstallera current_dir=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

filename = filedialog.askopenfilename(initialdir=current_dir, title="Select a file", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

if filename == "":
    terminate_error("No file selected")

if filename[-4:] != ".csv":
    terminate_error("Wrong file format, the file must be a .csv")

# Create a list containing tuples of answers and points for every round
with open(filename, "r+") as f:
    file_str = f.read()

    # Put an endline at the end of the file
    if file_str[-1] != "\n":
        f.write("\n")
    lines = file_str.split("\n")

    for j, line in enumerate(lines):

        # Skip empty lines
        if line == "":
            continue

        line = line.split(",")

        # Check if the line is valid
        if len(line) > 14:
            terminate_error(f"Every round must have at most 7 answers, {line} has {len(line)//2}")  

        round_data = []
        for i in range(0, len(line), 2):
            round_answer = line[i]

            # Check if the answer is valid
            if len(round_answer) > 16:
                terminate_error(f"Answer {round_answer} at line {i-1} is too long")

            # Check if the  is valid
            points = line[i + 1]
            if not points.isdigit() or int(points) not in range(100):
                print(line[i])
                terminate_error(f"Points {points} at line {j+1} are not valid")

            round_data.append([round_answer.lower(), points, True])
        game1.answers.append(round_data)

    # Sort answers by points
    for i, round_answers in enumerate(game1.answers):
        game1.answers[i] = sorted(round_answers, key=lambda x: int(x[1]), reverse=True)

    # Write sorted answers to the disk
    f.seek(0)
    for round_answers in game1.answers:
        answer_numbers = []
        for answer in round_answers:
            answer_numbers.append(answer[0])
            answer_numbers.append(answer[1])
        f.write(",".join(answer_numbers) + "\n")


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
window1.geometry("400x400")
style = ttk.Style(window1)
window1.protocol("WM_DELETE_WINDOW", lambda: exit_app(window1))

# Create SFX tab
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

button = tkinter.Button(tab1, text="Go", command=lambda: pygame.mixer.Sound.play())
button.pack()

# Create a tab for every round
for i, round_answers in enumerate(game1.answers):
    tab = ttk.Frame(tabControl)
    round_button = tkinter.Button(tab, text="Inicjalizuj runde", command=lambda round=i: game1.round_init(round))
    round_button.grid(row=0, column=1)
    l_won_button = tkinter.Button(tab, text="Lewa Wygrywa runde", command=lambda: game1.set_current_winner("L"))
    l_won_button.grid(row=1, column=0)
    r_won_button = tkinter.Button(tab, text="Prawa Wygrywa runde", command=lambda: game1.set_current_winner("P"))
    r_won_button.grid(row=1, column=2)
    l_strike_button = tkinter.Button(tab, text="Utrata Lewa", command=lambda: game1.big_strike("L"))
    r_strike_button = tkinter.Button(tab, text="Utrata Prawa", command=lambda: game1.big_strike("R"))
    l_strike_button.grid(row=2, column=0)
    r_strike_button.grid(row=2, column=2)

    # Add buttons for every answer
    for j, answer_dict in enumerate(round_answers):
        answer = answer_dict[0].ljust(16)
        points = answer_dict[1].rjust(2)
        answer_text = f"{answer} {points}"
        answer_button = tkinter.Button(tab, text=answer_text, command=lambda round=i, answer=j: game1.print_answer(round, answer))
        answer_button.grid(row=j + 2, column=1)
    tabControl.add(tab, text="Round" + str(i + 1))

# Create a tab for showing team scores
score_tab = ttk.Frame(tabControl)
score_button = tkinter.Button(score_tab, text = "Pokaż wyniki", command = game1.show_scores)
score_button.pack()

tabControl.add(score_tab, text="Punktacja")
tabControl.pack(expand=1, fill="both")

tabControl.add(tab1, text="SFX")
tabControl.pack(expand=1, fill="both")


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

    # Anti-bug maxx
    font_height = max(round(block_height * 0.75), 2)

    # Set the font
    myfont = pygame.font.Font("familiada.ttf", font_height)

    # Draw black rectangles & letters on the surface.
    for i in range(10):
        for j in range(29):
            pos_x = block_x + 50 + (block_width + 3) * j
            pos_y = block_y + 50 + (block_height + 3) * i
            label = myfont.render(game1.letter_matrix[i][j], 1, (255, 255, 0))
            rectangle_rgb = (0, 0, 0)
            rectangle_dimensions = (pos_x, pos_y, block_width, block_height)
            pygame.draw.rect(surface, rectangle_rgb, rectangle_dimensions)
            surface.blit(label, (pos_x + block_width * 0.146, pos_y + block_height / 2 - font_height / 2))

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
