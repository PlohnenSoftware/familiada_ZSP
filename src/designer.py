from PyQt6.QtWidgets import  QMainWindow, QLabel,QPushButton, QVBoxLayout, QWidget, QSpinBox, QTextEdit, QMessageBox, QCheckBox
class FamiliadaDesigner(QMainWindow):
    def __init__(self, filechooser):
        super().__init__()
        self.choose_file_dialog = filechooser
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Familiada Game Designer')
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Round input
        self.rounds_label = QLabel('Number of Rounds:', self)
        layout.addWidget(self.rounds_label)

        self.rounds_spinbox = QSpinBox(self)
        self.rounds_spinbox.setRange(1, 20)
        layout.addWidget(self.rounds_spinbox)

        # Answers input
        self.answers_text = QTextEdit(self)
        self.answers_text.setPlaceholderText('Enter answers and points as: answer1, points1, answer2, points2, etc. Each answer must be up to 17 chars, max 7 answers per round, max 99 points per answer.')
        layout.addWidget(self.answers_text)

        # Display mode checkbox
        self.display_mode_checkbox = QCheckBox('Enable Display Mode Only (::DISPLAY_MODE_ONLY::)', self)
        layout.addWidget(self.display_mode_checkbox)

        # Generate button
        self.generate_button = QPushButton('Generate Data File', self)
        self.generate_button.clicked.connect(self.generate_file)
        layout.addWidget(self.generate_button)

        # Open file button
        self.open_file_button = QPushButton('Otwórz plik CSV', self)
        self.open_file_button.clicked.connect(self.open_file)
        layout.addWidget(self.open_file_button)

    def validate_round(self, line, round_number):
        # Parsing and validation similar to provided code
        line = line.split(",")
        if len(line) > 14:
            self.show_error(f"Round {round_number + 1} has too many answers. Maximum allowed is 7.")
            return None

        round_data = []
        for i in range(0, len(line), 2):
            answer = line[i].strip()
            if len(answer) > 17:
                self.show_error(f'Answer "{answer}" in round {round_number + 1} is too long. Maximum length is 17 characters.')
                return None

            if i + 1 >= len(line):
                self.show_error(f'Missing points for answer "{answer}" in round {round_number + 1}.')
                return None

            points = line[i + 1].strip()
            if not points.isdigit() or int(points) not in range(100):
                self.show_error(f'Invalid points "{points}" for answer "{answer}" in round {round_number + 1}. Points must be between 0 and 99.')
                return None

            round_data.append([answer.lower(), points, True])

        # Sort answers by points, then alphabetically
        round_data.sort(key=lambda x: (-int(x[1]), x[0]))
        return round_data

    def generate_file(self):
        num_rounds = self.rounds_spinbox.value()
        all_rounds_text = self.answers_text.toPlainText().strip()
        lines = all_rounds_text.split('\n')

        if len(lines) != num_rounds:
            self.show_error(f'The number of rounds entered ({len(lines)}) does not match the selected number of rounds ({num_rounds}).')
            return

        parsed_answers = []
        for round_number, line in enumerate(lines):
            if line.strip() == "":
                continue
            round_data = self.validate_round(line, round_number)
            if round_data is None:
                return  # Error already shown in validate_round method
            parsed_answers.append(round_data)

        # Write to file
        filename = 'familiada_game_data.csv'
        try:
            with open(filename, "w") as f:
                for round_answers in parsed_answers:
                    answer_numbers = [f"{answer[0]},{answer[1]}" for answer in round_answers]
                    f.write(",".join(answer_numbers) + "\n")
                if self.display_mode_checkbox.isChecked():
                    f.write("::DISPLAY_MODE_ONLY::\n")
            QMessageBox.information(self, "Success", f"Data file '{filename}' generated successfully.")
        except Exception as e:
            self.show_error(f"Failed to write file: {str(e)}")

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def open_file(self):
        filename = self.choose_file_dialog(False)        
        if filename:
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                    self.answers_text.setText(content)
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się otworzyć pliku: {str(e)}")
