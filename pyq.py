import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QTabWidget


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple GUI")
        self.setGeometry(300, 300, 400, 200)

        # Create a central widget and set it as the main window's central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout
        layout = QVBoxLayout(central_widget)

        # Create a tab widget
        self.tab_widget = QTabWidget(self)

        # Create the first tab
        self.tab1 = QWidget()
        self.tab_widget.addTab(self.tab1, "Tab 1")

        # Create a vertical layout for the first tab
        tab1_layout = QVBoxLayout(self.tab1)

        # Create a label
        self.label = QLabel("Hello, PyQt6!", self)

        # Create a horizontal layout for buttons and text input fields
        button_layout = QHBoxLayout()

        # Create buttons
        self.button1 = QPushButton("Button 1", self)
        self.button2 = QPushButton("Button 2", self)

        # Create text input fields
        self.input1 = QLineEdit(self)
        self.input2 = QLineEdit(self)

        # Add the buttons and text input fields to the horizontal layout
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)
        button_layout.addWidget(self.input1)
        button_layout.addWidget(self.input2)

        # Add the label and the horizontal layout to the vertical layout of the first tab
        tab1_layout.addWidget(self.label)
        tab1_layout.addLayout(button_layout)

        # Create the second tab
        self.tab2 = QWidget()
        self.tab_widget.addTab(self.tab2, "Tab 2")

        # Create a vertical layout for the second tab
        tab2_layout = QVBoxLayout(self.tab2)

        # Create a button to generate a random number
        self.random_button = QPushButton("Generate Random Number", self)
        self.random_label = QLabel(self)

        # Add the button and label to the vertical layout of the second tab
        tab2_layout.addWidget(self.random_button)
        tab2_layout.addWidget(self.random_label)

        # Connect the button signals to their respective slots
        self.button1.clicked.connect(self.button1_clicked)
        self.button2.clicked.connect(self.button2_clicked)
        self.random_button.clicked.connect(self.generate_random_number)

        # Add the tab widget to the main layout
        layout.addWidget(self.tab_widget)

    def button1_clicked(self):
        input_text = self.input1.text()
        self.label.setText(f"Button 1 clicked!\nInput 1: {input_text}")

    def button2_clicked(self):
        input_text = self.input2.text()
        self.label.setText(f"Button 2 clicked!\nInput 2: {input_text}")

    def generate_random_number(self):
        random_number = random.randint(0, 100)
        self.random_label.setText(f"Random Number: {random_number}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
