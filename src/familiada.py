from sys import exit, argv
from blackboard import ICON_PATH, CWD_PATH
from logic import Game
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
    QCheckBox,
    QSlider,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QCursor, QIcon
from PyQt6.QtCore import Qt, QTimer

class ControlRoom(QMainWindow):
    def __init__(self):
        super().__init__()
        self.secret_phrase = "::DISPLAY_MODE_ONLY::"
        self.setWindowTitle("Familiada - reżyserka")
        self.setGeometry(300, 150, 1000, 600)
        self.fam_icon = QIcon(ICON_PATH)
        self.setWindowIcon(self.fam_icon)

    def setup_game_controls(self):
        self.open_file()  # Teraz otwórz plik po wyborze trybu gry
        central_widget = QWidget()
        pagelayout = QVBoxLayout(central_widget)
        
        # Create active team indicator
        active_team_widget = QWidget()
        active_team_layout = QHBoxLayout(active_team_widget)
        
        # Left indicator for team L
        self.team_L_indicator = QLabel("DRUŻYNA L")
        self.team_L_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.team_L_indicator.setStyleSheet("background-color: lightblue; color: black; font-weight: bold; padding: 10px; border-radius: 5px; font-size: 16px;")
        self.team_L_indicator.setMinimumHeight(40)
        
        # Right indicator for team R
        self.team_R_indicator = QLabel("DRUŻYNA P")
        self.team_R_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.team_R_indicator.setStyleSheet("background-color: lightgray; color: black; font-weight: bold; padding: 10px; border-radius: 5px; font-size: 16px;")
        self.team_R_indicator.setMinimumHeight(40)
        
        # Current player indicator
        self.current_player_indicator = QLabel("Gracz: -")
        self.current_player_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.current_player_indicator.setStyleSheet("font-weight: bold; font-size: 16px; padding: 10px;")
        
        # Game phase indicator
        self.game_phase_indicator = QLabel("Faza gry: -")
        self.game_phase_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.game_phase_indicator.setStyleSheet("font-style: italic; font-size: 14px;")
        
        # Add indicators to layout
        active_team_layout.addWidget(self.team_L_indicator)
        active_team_layout.addWidget(self.current_player_indicator)
        active_team_layout.addWidget(self.team_R_indicator)
        
        # Create a timer to update team indicators
        indicator_refresher = QTimer(self)
        indicator_refresher.timeout.connect(self.update_team_indicators)
        indicator_refresher.start(250)
        
        # Add the active team widget to main layout
        pagelayout.addWidget(active_team_widget)
        pagelayout.addWidget(self.game_phase_indicator)
        
        # Create tab widget and other elements
        tab_widget = QTabWidget()
        sfx_widget = QWidget()
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

            if gameWindow.fgm:
                # Jeden przycisk dla błędnej odpowiedzi aktywnej drużyny
                answer_button = self.create_buttons("Błędna odpowiedź")
                answer_button.clicked.connect(lambda: gameWindow.incorrect_answer(gameWindow.active_team))
                newtablayout.addWidget(answer_button, j + 2, 0)

                # buttons for starting teams
                team1_button = self.create_buttons("Zaczyna drużyna L")
                team1_button.clicked.connect(lambda: gameWindow.set_starting_team("L"))
                newtablayout.addWidget(team1_button, j + 3, 0)
                
                team2_button = self.create_buttons("Zaczyna drużyna P")
                team2_button.clicked.connect(lambda: gameWindow.set_starting_team("R"))
                newtablayout.addWidget(team2_button, j + 4, 0)

            tab_widget.addTab(newtab, f"Runda {i+1}")

        # Create widgets - buttons
        button_brawo = self.create_buttons("Brawa")
        button_stop = self.create_buttons("Stop")
        verticalspacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_intro = self.create_buttons("Intro")
        button_outro = self.create_buttons("Outro")
        button_name = self.create_buttons("Napis")
        checkbox_gradient = QCheckBox("Show gradient?")  # Add checkbox here

        # Connect buttons to functions
        button_intro.clicked.connect(lambda: gameWindow.playsound("intro"))
        button_outro.clicked.connect(lambda: gameWindow.playsound("ending"))
        button_brawo.clicked.connect(lambda: gameWindow.playsound("bravo"))
        button_stop.clicked.connect(gameWindow.stop_playing)
        button_name.clicked.connect(gameWindow.show_name)
        # button_name.clicked.connect(lambda: gameWindow.big_digit(1,1,0))

       # Use a lambda to update the show_gradient variable
        def update_gradient_state(state):
           gameWindow.grad_bkg = bool(state)
           gameWindow.refresh()
        checkbox_gradient.stateChanged.connect(update_gradient_state)

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
        sfxlayout.addWidget(checkbox_gradient, 1, 6)

        # Create points tab if full game logic is on
        if gameWindow.fgm:
            punktacja = QWidget()
            punktacjalayout = QGridLayout(punktacja)
            
            # Create score display
            score_label_L = QLabel(f"Drużyna L: 0")
            score_label_L.setStyleSheet("font-size: 20px; font-weight: bold;")
            punktacjalayout.addWidget(score_label_L, 0, 0)
            
            score_label_R = QLabel(f"Drużyna R: 0")
            score_label_R.setStyleSheet("font-size: 20px; font-weight: bold;")
            punktacjalayout.addWidget(score_label_R, 0, 1)
            
            # Create phase display
            phase_label = QLabel(f"Faza gry: {gameWindow.game_phase}")
            phase_label.setStyleSheet("font-size: 16px;")
            punktacjalayout.addWidget(phase_label, 1, 0, 1, 2)
            
            # Add prepare face-off button
            face_off_button = self.create_buttons("Przygotuj Face-Off")
            face_off_button.clicked.connect(gameWindow.prepare_face_off)
            punktacjalayout.addWidget(face_off_button, 2, 0, 1, 2)
            
            # Function to update score display
            def update_scores():
                score_label_L.setText(f"Drużyna L: {gameWindow.teams['L']['score']}")
                score_label_R.setText(f"Drużyna R: {gameWindow.teams['R']['score']}")
                phase_label.setText(f"Faza gry: {gameWindow.game_phase}")
            
            # Create a timer to refresh the scores
            score_refresher = QTimer(self)
            score_refresher.timeout.connect(update_scores)
            score_refresher.start(250)
            
            tab_widget.addTab(punktacja, "Punktacja")

        # Create finals tab
        final = QWidget()
        finallayout = QGridLayout(final)
        
        # Create a button to initialize the final round
        final_round_button = self.create_buttons("Rozpocznij Finał")
        final_round_button.clicked.connect(gameWindow.init_final_round)
        finallayout.addWidget(final_round_button, 0, 0, 1, 2)
        
        # Create input fields and buttons for final round answers
        for i in range(5):
            # Create input fields for answers and points
            answer_input_1 = QLineEdit()
            answer_input_1.setPlaceholderText(f"Odpowiedź {i+1} - gracz 1")
            finallayout.addWidget(answer_input_1, i+1, 0)
            
            points_input_1 = QLineEdit()
            points_input_1.setPlaceholderText("Punkty")
            points_input_1.setMaximumWidth(50)
            finallayout.addWidget(points_input_1, i+1, 1)
            
            show_button_1 = self.create_buttons("Pokaż")
            show_button_1.clicked.connect(lambda state, row=i, a=answer_input_1, p=points_input_1: 
                                         gameWindow.show_final_answer(a, p, row, 0))
            finallayout.addWidget(show_button_1, i+1, 2)
            
            answer_input_2 = QLineEdit()
            answer_input_2.setPlaceholderText(f"Odpowiedź {i+1} - gracz 2")
            finallayout.addWidget(answer_input_2, i+1, 3)
            
            points_input_2 = QLineEdit()
            points_input_2.setPlaceholderText("Punkty")
            points_input_2.setMaximumWidth(50)
            finallayout.addWidget(points_input_2, i+1, 4)
            
            show_button_2 = self.create_buttons("Pokaż")
            show_button_2.clicked.connect(lambda state, row=i, a=answer_input_2, p=points_input_2: 
                                         gameWindow.show_final_answer(a, p, row, 1))
            finallayout.addWidget(show_button_2, i+1, 5)
        
        tab_widget.addTab(final, "Finał")
        
        # Add layouts to window
        pagelayout.addWidget(tab_widget)
        pagelayout.addWidget(sfx_widget)

        # Create a timer to refresh the window
        refresher = QTimer(self)
        refresher.timeout.connect(gameWindow.refresh)
        refresher.start(250)
        self.show()  # Pokazanie obecnego okna gry
        gameWindow.refresh()

    def update_team_indicators(self):
        """Update the team indicators based on the active team"""
        active_team = gameWindow.active_team
        
        # Reset both indicators
        self.team_L_indicator.setStyleSheet("background-color: lightgray; color: black; font-weight: bold; padding: 10px; border-radius: 5px; font-size: 16px;")
        self.team_R_indicator.setStyleSheet("background-color: lightgray; color: black; font-weight: bold; padding: 10px; border-radius: 5px; font-size: 16px;")
        
        # Highlight active team
        if active_team == "L":
            self.team_L_indicator.setStyleSheet("background-color: #4287f5; color: white; font-weight: bold; padding: 10px; border-radius: 5px; font-size: 16px;")
            if gameWindow.game_phase == "main_play":
                player_num = gameWindow.current_player_index["L"] + 1
                self.current_player_indicator.setText(f"Gracz: {player_num}")
        elif active_team == "R":
            self.team_R_indicator.setStyleSheet("background-color: #f54242; color: white; font-weight: bold; padding: 10px; border-radius: 5px; font-size: 16px;")
            if gameWindow.game_phase == "main_play":
                player_num = gameWindow.current_player_index["R"] + 1
                self.current_player_indicator.setText(f"Gracz: {player_num}")
        else:
            self.current_player_indicator.setText("Gracz: -")
            
        # Update game phase
        self.game_phase_indicator.setText(f"Faza gry: {gameWindow.game_phase}")

    def slider_moved(self):
        value_of_slider = self.slider.value()
        self.label_glosnosc.setText("Głośność: " + str(value_of_slider / 10) + "%")
        gameWindow.set_global_volume(value_of_slider / 1000)

    def create_buttons(self, name: str) -> QPushButton:
        button = QPushButton(name)
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button.setMinimumWidth(200)
        button.setStyleSheet("padding: 15px 10px;font-size: 14px;")
        return button

    def check_odm(self, in_str: str):
        if self.secret_phrase in in_str:
            return False, in_str.replace(self.secret_phrase, "")
        else:
            return True, in_str

    def display_error_and_exit(self, error_description: str, term: bool = True) -> None:
        dlg = QMessageBox(self)
        dlg.setIcon(QMessageBox.Icon.Critical)
        dlg.setWindowTitle("Błąd")
        dlg.setText(error_description)
        button = dlg.exec()
        if button == QMessageBox.StandardButton.Ok and term:
            exit()

    def open_file(self):
        filename = self.choose_file_dialog(True)

        file_str = self.read_file(filename)
        if file_str is None:
            return

        gameWindow.fgm, file_str = self.check_odm(file_str)

        lines = file_str.split("\n")
        gameWindow.answers = self.parse_lines(lines)
        self.write_sorted_answers(filename)

    def choose_file_dialog(self, term) -> str:
        file_filter = "CSV File (*.csv)"
        filename = QFileDialog.getOpenFileName(parent=self, caption="Wybierz plik", directory=CWD_PATH, filter=file_filter, initialFilter=file_filter)
        filename = str(filename[0])
        if filename == "":
            self.display_error_and_exit("Nie wybrano pliku",term)
        return filename

    def read_file(self, filename) -> str | None:
        try:
            with open(filename, "r") as f:
                file_str = f.read()
            return file_str
        except FileNotFoundError:
            self.display_error_and_exit(f"Plik '{filename}' nie został znaleziony")
            return None

    def parse_lines(self, lines):
        parsed_answers = []
        for j, line in enumerate(lines):
            if line == "":
                continue
            line = line.split(",")
            if len(line) > 14:
                self.display_error_and_exit(f"Każda runda musi mieć maksymalnie 7 odpowiedzi, runda {j+1} ma ich aż {len(line) // 2}")
            round_data = self.parse_round(line, j)
            parsed_answers.append(round_data)
        return parsed_answers

    def parse_round(self, line, j: int):
        round_data = []
        for i in range(0, len(line), 2):
            round_answer = line[i]
            if len(round_answer) > 17:
                self.display_error_and_exit(f'Odpowiedź "{round_answer}" w linii {j+1} pliku CSV jest za długa')
            points = line[i + 1]
            if not points.isdigit() or int(points) not in range(100):
                self.display_error_and_exit(f'Punkty "{points}" w linii {j+1} pliku CSV są nieprawidłowe')
            round_data.append([round_answer.lower(), points, True])

        # Sortowanie odpowiedzi po punktach, a następnie alfabetycznie
        round_data.sort(key=lambda x: (-int(x[1]), x[0]))
        return round_data

    def write_sorted_answers(self, filename) -> None:
        with open(filename, "w") as f:
            for round_answers in gameWindow.answers:
                answer_numbers = [f"{answer[0]},{answer[1]}" for answer in round_answers]
                f.write(",".join(answer_numbers) + "\n")
            if not gameWindow.fgm:
                f.write(self.secret_phrase)
                f.write("\n")

    def ask_what_to_run(self):
        dlg = QMessageBox(self)
        dlg.setIcon(QMessageBox.Icon.Question)  # Ikona zapytania
        dlg.setWindowTitle("Wybór trybu")
        dlg.setText("Co chcesz uruchomić?")
        dlg.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowTitleHint)

        # Add custom buttons instead of using setButtonText
        button_designer = dlg.addButton("Designer", QMessageBox.ButtonRole.AcceptRole)
        button_game = dlg.addButton("Gra",QMessageBox.ButtonRole.ActionRole)

        dlg.exec()
        clicked_button = dlg.clickedButton()

        if clicked_button  == button_designer:
            self.run_designer()  # Funkcja do uruchomienia Designera
        elif clicked_button  == button_game:
            global gameWindow
            gameWindow = Game()
            gameWindow.refresh()
            self.setup_game_controls()  # Konfiguracja kontroli gry

    def run_designer(self):
        from designer import FamiliadaDesigner  # Importowanie Designera
        self.designer_window = FamiliadaDesigner(self.choose_file_dialog)
        self.designer_window.setWindowIcon(self.fam_icon)
        self.designer_window.show()

if __name__ == "__main__":
    app = QApplication(argv)
    control_room = ControlRoom()
    control_room.ask_what_to_run()  # Zapytanie użytkownika, co uruchomić
    exit(app.exec())
