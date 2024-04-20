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
        self.secret_phrase = "::DISPLAY_MODE_ONLY::"
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
            # # add butto for incorect answer
            # answer_button = self.create_buttons("Nieznana odpowiedź")
            # answer_button.clicked.connect(lambda: gameWindow.incorrect_answer("R"))
            # newtablayout.addWidget(answer_button, j + 2, 0)
            # # buttons for strting teams
            # team1_button = self.create_buttons("Zaczyna drużyna L")
            # team1_button.clicked.connect(lambda: gameWindow.set_starting_team("L"))
            # newtablayout.addWidget(team1_button, j + 3, 0)
            # team2_button = self.create_buttons("Zaczyna drużyna P")
            # team2_button.clicked.connect(lambda: gameWindow.set_starting_team("P"))
            # newtablayout.addWidget(team2_button, j + 4, 0)

            tab_widget.addTab(newtab, f"Runda {i+1}")

        # Create widgets - buttons
        button_brawo = self.create_buttons("Brawa")
        button_stop = self.create_buttons("Stop")
        verticalspacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_intro = self.create_buttons("Intro")
        button_outro = self.create_buttons("Outro")
        button_name = self.create_buttons("Napis")

        # Connect buttons to functions
        button_intro.clicked.connect(lambda: gameWindow.playsound("intro"))
        button_outro.clicked.connect(lambda: gameWindow.playsound("ending"))
        button_brawo.clicked.connect(lambda: gameWindow.playsound("bravo"))
        button_stop.clicked.connect(gameWindow.stop_playing)
        button_name.clicked.connect(gameWindow.show_name)

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
        sfxlayout.addWidget(button_name, 0, 6)

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

    def check_odm(self, in_str: str):        
        if self.secret_phrase in in_str:
            return True, in_str.replace(self.secret_phrase, "")
        else:
            return False, in_str

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
        gameWindow.odm, file_str = self.check_odm(file_str)
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
            if len(round_answer) > 17:
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
            if gameWindow.odm:
                f.write(self.secret_phrase)


if __name__ == "__main__":
    app = QApplication(argv)
    window = ControlRoom()
    window.show()
    gameWindow.refresh()
    exit(app.exec())
