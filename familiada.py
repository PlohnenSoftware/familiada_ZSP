from sys import exit, argv
from os import getcwd
from blackboard import Blackboard
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QWidget,
    QLineEdit,
    QTabWidget,
    QTextEdit,
    QComboBox,
    QSlider,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QCursor, QIcon
from PyQt6.QtCore import Qt, QTimer

gameWindow = Blackboard()

# current_dir = os.path.dirname(os.path.abspath(__file__))
# current_dir=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')


class ControlRoom(QMainWindow):
    def __init__(self):
        super().__init__()
        self.open_file()
        self.setWindowTitle("Familiada - reżyserka")
        self.setGeometry(300, 150, 1000, 600)
        self.setWindowIcon(QIcon("familiada.ico"))

        central_widget = QWidget()
        tab_widget = QTabWidget()
        sfx_widget = QWidget()

        pagelayout = QVBoxLayout(central_widget)
        sfxlayout = QGridLayout(sfx_widget)

        self.setCentralWidget(central_widget)

        tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        tab_widget.setMovable(True)

        for i, round_answers in enumerate(gameWindow.answers):
            newtab = QWidget()
            newtablayout = QGridLayout(newtab)
            start_button = self.create_buttons("ZACZNIJ")
            start_button.clicked.connect(lambda state, round=i: gameWindow.round_init(round))
            newtablayout.addWidget(start_button, 0, 0)

            for j, answer_dict in enumerate(round_answers):
                answer = answer_dict[0].ljust(16)
                points = answer_dict[1].rjust(2)
                answer_text = f"{answer} {points}"
                answer_button = self.create_buttons(answer_text)
                answer_button.clicked.connect(lambda state, round=i, answer=j: gameWindow.show_answer(round, answer))
                newtablayout.addWidget(answer_button, j + 1, 0)

            tab_widget.addTab(newtab, f"Runda {i+1}")

        # Create widgets - buttons
        button_brawo = self.create_buttons("Brawa")
        button_stop = self.create_buttons("Stop")
        verticalspacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_intro = self.create_buttons("Intro")
        button_outro = self.create_buttons("Outro")

        # Connect buttons to functions
        button_intro.clicked.connect(lambda: gameWindow.playsound("intro"))
        button_outro.clicked.connect(lambda: gameWindow.playsound("ending"))
        button_brawo.clicked.connect(lambda: gameWindow.playsound("bravo"))
        button_stop.clicked.connect(gameWindow.stop_playing)

        # Create widgets - slider and label
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 1000)
        self.slider.setValue(1000)
        self.slider.setMinimumWidth(400)
        self.slider.valueChanged.connect(self.slider_moved)
        self.label_glosnosc = QLabel("Głośność: " + str(self.slider.value() / 10) + "%")
        self.label_glosnosc.setStyleSheet("font-size: 16px;")

        # Add widgets to layouts
        sfxlayout.addWidget(button_brawo, 0, 0)
        sfxlayout.addWidget(button_stop, 2, 0)
        sfxlayout.addItem(verticalspacer, 1, 0, 2, 1)
        sfxlayout.addWidget(button_intro, 0, 1)
        sfxlayout.addWidget(button_outro, 2, 1)
        sfxlayout.addWidget(self.label_glosnosc, 0, 2, 1, 4, alignment=Qt.AlignmentFlag.AlignHCenter)
        sfxlayout.addWidget(self.slider, 2, 2, 2, 4)

        punktacja = QWidget()
        tab_widget.addTab(punktacja, "Punktacja")
        final = QWidget()
        tab_widget.addTab(final, "Finał")
        pagelayout.addWidget(tab_widget)
        pagelayout.addWidget(sfx_widget)
        refresher = QTimer(self)
        refresher.timeout.connect(gameWindow.refresh)
        refresher.start(250)

    def slider_moved(self):
        value_of_slider = self.slider.value()
        self.label_glosnosc.setText("Głośność: " + str(value_of_slider / 10) + "%")
        gameWindow.set_global_volume(value_of_slider / 1000)

    def create_buttons(self, name):
        button = QPushButton(name)
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button.setMinimumWidth(200)
        button.setStyleSheet("padding: 15px 10px;font-size: 14px;")
        return button

    def terminate_error(self, error_description):
        dlg = QMessageBox(self)
        dlg.setIcon(QMessageBox.Icon.Critical)
        dlg.setWindowTitle("Błąd")
        dlg.setText(error_description)
        button = dlg.exec()
        if button == QMessageBox.StandardButton.Ok:
            exit()

    def open_file(self):
        file_filter = "CSV File (*.csv)"
        filename = QFileDialog.getOpenFileName(parent=self, caption="Wybierz plik", directory=getcwd(), filter=file_filter, initialFilter="CSV File (*.csv)")
        filename = str(filename[0])
        if filename == "":
            self.terminate_error("Nie wybrano pliku")

        file_str = self.read_file(filename)
        if file_str is None:
            return

        lines = file_str.split("\n")
        gameWindow.answers = self.parse_lines(lines)
        self.write_sorted_answers(filename)

    def read_file(self, filename):
        try:
            with open(filename, "r") as f:
                file_str = f.read()
            return file_str
        except FileNotFoundError:
            self.terminate_error(f"Plik '{filename}' nie został znaleziony")
            return None

    def parse_lines(self, lines):
        parsed_answers = []
        for j, line in enumerate(lines):
            if line == "":
                continue
            line = line.split(",")
            if len(line) > 14:
                self.terminate_error(f"Każda runda musi mieć maksymalnie 7 odpowiedzi, runda {j+1} ma ich aż {len(line) // 2}")
            round_data = self.parse_round(line, j)
            parsed_answers.append(round_data)
        return parsed_answers

    def parse_round(self, line, j):
        round_data = []
        for i in range(0, len(line), 2):
            round_answer = line[i]
            if len(round_answer) > 16:
                self.terminate_error(f'Odpowiedź "{round_answer}" w linii {j+1} pliku CSV jest za długa')
            points = line[i + 1]
            if not points.isdigit() or int(points) not in range(100):
                self.terminate_error(f'Punkty "{points}" w linii {j+1} pliku CSV są nieprawidłowe')
            round_data.append([round_answer.lower(), points, True])

        # Sortowanie odpowiedzi po punktach, a następnie alfabetycznie
        round_data.sort(key=lambda x: (-int(x[1]), x[0]))
        return round_data

    def write_sorted_answers(self, filename):
        with open(filename, "w") as f:
            for round_answers in gameWindow.answers:
                answer_numbers = [f"{answer[0]},{answer[1]}" for answer in round_answers]
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

# Create a tab for every round
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

# button5 = tkinter.Button(sfx_tab, text="STOP", command=lambda: pygame.mixer.fadeout(500))
# button5.pack()

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
