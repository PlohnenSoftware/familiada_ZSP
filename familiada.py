from sys import exit, argv
import os
from blackboard import Blackboard as Bb
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QLineEdit, QTabWidget, QTextEdit, QComboBox
from PyQt6.QtCore import QTimer
from PyQt6 import QtGui
from PyQt6.QtGui import QCursor
from PyQt6 import QtCore

gameWindow = Bb()
# The program provides a graphical interface for the game Familiada.gameWindow

# Game data is a csv selected by the user upon startup.
# The file should contain lines of answers for round with points
# in the form of dicts {word,score} all separated by commas.

# Currently all gui texts are written in Polish.

# Blackboard class containing the matrix object used to draw characters on the screen


# Safely exit the program

###############TKINTER##################
# if messagebox.showerror("FAMILIADA ERROR", error_description):
#     exit()


# Initialize the main game object

# Read data from the disk

# lepiej zrobić pulpit na start, do finalnej wersji bo jak sie d exe spakuje to wywala do jakiegoś folderu temp,
# gdzie jest interpreter pythona przenosny z Pyinstallera
# current_dir=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')


###############TKINTER##################
# filename = filedialog.askopenfilename(initialdir=current_dir, title="Wybierz plik z danymi", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))


# Create a list containing tuples of answers and points for every round

#################################################################################################################


# current_dir = os.path.dirname(os.path.abspath(__file__))


class ControlRoom(QMainWindow):
    def __init__(self):
        super().__init__()
        self.getFileName()
        self.setWindowTitle("Familiada")
        self.setGeometry(300, 150, 1000, 600)
        self.setWindowIcon(QtGui.QIcon("familiada.ico"))

        central_widget = QWidget()
        tab_widget = QTabWidget()
        sfx_widget = QWidget()
        pagelayout = QVBoxLayout(central_widget)
        sfxlayout = QGridLayout(sfx_widget)
        self.setCentralWidget(central_widget)
        self.setLayout(pagelayout)
        tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        tab_widget.setMovable(True)

        for i, round_answers in enumerate(gameWindow.answers):
            newtab = QWidget()
            tab_widget.addTab(newtab, f"Runda {i+1}")

        button_brawo = self.create_buttons("Brawa")
        button_stop = self.create_buttons("Stop")
        button_intro = self.create_buttons("Intro")
        button_outro = self.create_buttons("Outro")

        sfxlayout.addWidget(button_brawo, 0, 0)
        sfxlayout.addWidget(button_stop, 1, 0)
        sfxlayout.addWidget(button_intro, 0, 1)
        sfxlayout.addWidget(button_outro, 1, 1)

        punktacja = QWidget()
        tab_widget.addTab(punktacja, "Punktacja")
        final = QWidget()
        tab_widget.addTab(final, "Finał")
        pagelayout.addWidget(tab_widget)
        pagelayout.addWidget(sfx_widget)

    def create_buttons(self, name):
        button = QPushButton(name)
        button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        button.setFixedWidth(300)
        return button

    def terminate_error(self, error_description):
        dlg = QMessageBox(self)
        dlg.setIcon(QMessageBox.Icon.Critical)
        dlg.setWindowTitle("Błąd")
        dlg.setText(error_description)
        button = dlg.exec()
        if button == QMessageBox.StandardButton.Ok:
            exit()

    def getFileName(self):
        file_filter = "CSV File (*.csv)"
        filename = QFileDialog.getOpenFileName(parent=self, caption="Wybierz plik", directory=os.getcwd(), filter=file_filter, initialFilter="CSV File (*.csv)")
        filename = str(filename[0])
        if filename == "":
            self.terminate_error("Nie wybrano pliku")

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
                    self.terminate_error(f"Every round must have at most 7 answers, {line} has {len(line)//2}")

                round_data = []
                for i in range(0, len(line), 2):
                    round_answer = line[i]

                    # Check if the answer is valid
                    if len(round_answer) > 16:
                        self.terminate_error(f"Answer {round_answer} at line {i-1} is too long")

                    # Check if the  is valid
                    points = line[i + 1]
                    if not points.isdigit() or int(points) not in range(100):
                        self.terminate_error(f"Points {points} at line {j+1} are not valid")

                    round_data.append([round_answer.lower(), points, True])
                gameWindow.answers.append(round_data)

            # Sort answers by points
            for i, round_answers in enumerate(gameWindow.answers):
                gameWindow.answers[i] = sorted(round_answers, key=lambda x: int(x[1]), reverse=True)

            # Write sorted answers to the disk
            f.seek(0)
            for round_answers in gameWindow.answers:
                answer_numbers = []
                for answer in round_answers:
                    answer_numbers.append(answer[0])
                    answer_numbers.append(answer[1])
                f.write(",".join(answer_numbers) + "\n")


if __name__ == "__main__":
    app = QApplication(argv)
    window = ControlRoom()
    window.show()
    gameWindow.refresh()
    exit(app.exec())


# Create the window, saving it to a variable.


# # Create the second window
# window1 = tkinter.Tk()
# window1.title("Familiada - reżyserka")
# window1.iconbitmap("familiada.ico")
# window1.geometry("650x400")
# style = ttk.Style(window1)
# window1.protocol("WM_DELETE_WINDOW", lambda: exit(window1))

# # Create tab controler in the window1
# tabControl = ttk.Notebook(window1)

# # Create a tab for every round
# for i, round_answers in enumerate(gameWindow.answers):
#     round_tab = ttk.Frame(tabControl)
#     round_tab.grid_columnconfigure((0, 4), weight=1)

#     round_button = tkinter.Button(round_tab, text="Zacznij runde", command=lambda round=i: gameWindow.round_init(round))
#     round_button.grid(row=0, column=2, sticky="ew")

#     l_start_button = tkinter.Button(round_tab, text="Lewa pierwsza", command=lambda: gameWindow.set_starting_team("L"))
#     l_start_button.grid(row=1, column=1, sticky="ew")

#     r_start_button = tkinter.Button(round_tab, text="Prawa pierwsza", command=lambda: gameWindow.set_starting_team("R"))
#     r_start_button.grid(row=1, column=3, sticky="ew")

#     l_strike_button = tkinter.Button(round_tab, text="Błąd Lewa", command=lambda: gameWindow.incorrect_answer("L"))
#     l_strike_button.grid(row=2, column=1, sticky="ew")

#     r_strike_button = tkinter.Button(round_tab, text="Błąd Prawa", command=lambda: gameWindow.incorrect_answer("R"))
#     r_strike_button.grid(row=2, column=3, sticky="ew")

#     # Add buttons for every answer
#     for j, answer_dict in enumerate(round_answers):
#         answer = answer_dict[0].ljust(16)
#         points = answer_dict[1].rjust(2)
#         answer_text = f"{answer} {points}"
#         answer_button = tkinter.Button(round_tab, text=answer_text, command=lambda round=i, answer=j: gameWindow.show_answer(round, answer))
#         answer_button.grid(row=j + 2, column=2, sticky="ew")
#     tabControl.add(round_tab, text=f"Round {i + 1}")

# # Create a tab for showing team scores
# score_tab = ttk.Frame(tabControl)
# score_button = tkinter.Button(score_tab, text="Pokaż wyniki", command=gameWindow.show_scores)
# score_button.pack()
# tabControl.add(score_tab, text="Punktacja")

# # Create a tab for final round
# final_tab = ttk.Frame(tabControl)
# for w in range(5):
#     for t in range(2):
#         input_answer = tkinter.Entry(final_tab)
#         input_points = tkinter.Entry(final_tab)
#         final_button = tkinter.Button(final_tab, text="Wyświetl", command=lambda r=w, c=t, answer_txt=input_answer, point_txt=input_points: gameWindow.show_final_answer(answer_txt, point_txt, r, c))
#         input_answer.grid(row=w + 1, column=t * 3)
#         input_points.grid(row=w + 1, column=t * 3 + 1)
#         final_button.grid(row=w + 1, column=t * 3 + 2)

# startfinal_button = tkinter.Button(final_tab, text="Zacznij finał", command=gameWindow.init_final_round)
# startfinal_button.grid(row=0, column=2)

# doubled_answer = tkinter.Button(final_tab, text="Dubel", command=lambda: pygame.mixer.Sound.play(dubel_sound))
# doubled_answer.grid(row=7, column=2)

# labeltxt = "Odpowiedź:"
# label_answer = tkinter.Label(final_tab, text=labeltxt)
# label_answer.grid(row=0, column=0)
# label_answer1 = tkinter.Label(final_tab, text=labeltxt)
# label_answer1.grid(row=0, column=3)

# labeltxt1 = "Punkty:"
# label_points = tkinter.Label(final_tab, text=labeltxt1)
# label_points.grid(row=0, column=1)
# label_points1 = tkinter.Label(final_tab, text=labeltxt1)
# label_points1.grid(row=0, column=4)

# tabControl.add(final_tab, text="Finał")

# # Create SFX tab
# sfx_tab = ttk.Frame(tabControl)

# button1 = tkinter.Button(sfx_tab, text="Brawa", command=lambda: pygame.mixer.Sound.play(bravo_sound))
# button1.pack()

# button2 = tkinter.Button(sfx_tab, text="INTRO", command=lambda: pygame.mixer.Sound.play(intro_music))
# button2.pack()

# button3 = tkinter.Button(sfx_tab, text="ENDING", command=lambda: pygame.mixer.Sound.play(ending_music))
# button3.pack()

# button4 = tkinter.Button(sfx_tab, text="ROUND", command=lambda: pygame.mixer.Sound.play(round_sound))
# button4.pack()

# button4 = tkinter.Button(sfx_tab, text="STOP", command=lambda: pygame.mixer.fadeout(500))
# button4.pack()

# tabControl.add(sfx_tab, text="SFX")
# tabControl.pack(expand=1, fill="both")


#   try:
#      for event in pygame.event.get():
#          if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
#              exit()

#          if event.type == pygame.VIDEORESIZE:
#              # There's some code to add back window content here.
#              surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

#  # Quit the game if the window is closed
#   except pygame.error:
#      exit()
