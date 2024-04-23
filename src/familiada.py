import pygame
import sys
import tkinter
import os
from tkinter import messagebox, ttk, filedialog
from blackboard import Blackboard as Bb
from blackboard import dubel_sound, bravo_sound, round_sound, intro_music, ending_music

# The program provides a graphical interface for the game Familiada.

# Game data is a csv selected by the user upon startup.
# The file should contain lines of answers for round with points
# in the form of dicts {word,score} all separated by commas.

# Currently all gui texts are written in Polish.

# Blackboard class containing the matrix object used to draw characters on the screen

# Safely exit the program
def exit_app(tkwindow):
    tkwindow.destroy()
    pygame.display.quit()
    pygame.quit()
    sys.exit()


def terminate_error(error_description):
    if messagebox.showerror("FAMILIADA ERROR", error_description):
        sys.exit()


# Initialize the main game object
game1 = Bb(20)

# Read data from the disk
current_dir = os.path.dirname(os.path.abspath(__file__))
# lepiej zrobić pulpit na start, do finalnej wersji bo jak sie d exe spakuje to wywala do jakiegoś folderu temp,
# gdzie jest interpreter pythona przenosny z Pyinstallera 
# current_dir=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

filename = filedialog.askopenfilename(initialdir=current_dir, title="Wybierz plik z danymi", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

if filename == "":
    terminate_error("Nie wybrano pliku")

if filename[-4:] != ".csv":
    terminate_error("Zly format pliku, musi to byc .csv")

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
window1.geometry("650x400")
style = ttk.Style(window1)
window1.protocol("WM_DELETE_WINDOW", lambda: exit_app(window1))

# Create tab controler in the window1
tabControl = ttk.Notebook(window1)

# Create a tab for every round
for i, round_answers in enumerate(game1.answers):
    round_tab = ttk.Frame(tabControl)
    round_tab.grid_columnconfigure((0, 4), weight=1)

    round_button = tkinter.Button(round_tab, text="Zacznij runde", command=lambda round=i: game1.round_init(round))
    round_button.grid(row=0, column=2, sticky="ew")

    l_start_button = tkinter.Button(round_tab, text="Lewa pierwsza", command=lambda: game1.set_starting_team("L"))
    l_start_button.grid(row=1, column=1, sticky="ew")

    r_start_button = tkinter.Button(round_tab, text="Prawa pierwsza", command=lambda: game1.set_starting_team("R"))
    r_start_button.grid(row=1, column=3, sticky="ew")

    l_strike_button = tkinter.Button(round_tab, text="Błąd Lewa", command=lambda: game1.incorrect_answer("L"))
    l_strike_button.grid(row=2, column=1, sticky="ew")

    r_strike_button = tkinter.Button(round_tab, text="Błąd Prawa", command=lambda: game1.incorrect_answer("R"))
    r_strike_button.grid(row=2, column=3, sticky="ew")

    # Add buttons for every answer
    for j, answer_dict in enumerate(round_answers):
        answer = answer_dict[0].ljust(16)
        points = answer_dict[1].rjust(2)
        answer_text = f"{answer} {points}"
        answer_button = tkinter.Button(round_tab, text=answer_text, command=lambda round=i, answer=j: game1.show_answer(round, answer))
        answer_button.grid(row=j + 2, column=2, sticky="ew")
    tabControl.add(round_tab, text=f"Round {i + 1}")

# Create a tab for showing team scores
score_tab = ttk.Frame(tabControl)
score_button = tkinter.Button(score_tab, text="Pokaż wyniki", command=game1.show_scores)
score_button.pack()
tabControl.add(score_tab, text="Punktacja")

# Create a tab for final round
final_tab = ttk.Frame(tabControl)
for w in range(5):
    for t in range(2):
        input_answer = tkinter.Entry(final_tab)
        input_points = tkinter.Entry(final_tab)
        final_button = tkinter.Button(final_tab, text="Wyświetl", command=lambda r=w, c=t, answer_txt=input_answer, point_txt=input_points: game1.show_final_answer(answer_txt, point_txt, r, c))
        input_answer.grid(row=w + 1, column=t * 3)
        input_points.grid(row=w + 1, column=t * 3 + 1)
        final_button.grid(row=w + 1, column=t * 3 + 2)

startfinal_button = tkinter.Button(final_tab, text="Zacznij finał", command=game1.init_final_round)
startfinal_button.grid(row=0, column=2)

doubled_answer = tkinter.Button(final_tab, text="Dubel", command=lambda: pygame.mixer.Sound.play(dubel_sound))
doubled_answer.grid(row=7, column=2)

labeltxt = "Odpowiedź:"
label_answer = tkinter.Label(final_tab, text=labeltxt)
label_answer.grid(row=0, column=0)
label_answer1 = tkinter.Label(final_tab, text=labeltxt)
label_answer1.grid(row=0, column=3)

labeltxt1 = "Punkty:"
label_points = tkinter.Label(final_tab, text=labeltxt1)
label_points.grid(row=0, column=1)
label_points1 = tkinter.Label(final_tab, text=labeltxt1)
label_points1.grid(row=0, column=4)

tabControl.add(final_tab, text="Finał")

# Create SFX tab
sfx_tab = ttk.Frame(tabControl)

button1 = tkinter.Button(sfx_tab, text="Brawa", command=lambda: pygame.mixer.Sound.play(bravo_sound))
button1.pack()

button2 = tkinter.Button(sfx_tab, text="INTRO", command=lambda: pygame.mixer.Sound.play(intro_music))
button2.pack()

button3 = tkinter.Button(sfx_tab, text="ENDING", command=lambda: pygame.mixer.Sound.play(ending_music))
button3.pack()

button4 = tkinter.Button(sfx_tab, text="ROUND", command=lambda: pygame.mixer.Sound.play(round_sound))
button4.pack()

button4 = tkinter.Button(sfx_tab, text="STOP", command=lambda: pygame.mixer.fadeout(500))
button4.pack()

tabControl.add(sfx_tab, text="SFX")
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

    # Anti-bug SUPERmaxxx
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
