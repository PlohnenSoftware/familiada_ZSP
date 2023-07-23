import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLCDNumber
from PyQt6.QtCore import QTimer


class CounterWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.counter = 0
        self.is_running = False

        self.setWindowTitle("Counter Window")
        self.setGeometry(100, 100, 300, 150)

        self.layout = QVBoxLayout()

        self.display = QLCDNumber(self)
        self.display.setDigitCount(7)
        self.display.display(self.counter)

        self.layout.addWidget(self.display)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_timer)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_timer)
        self.layout.addWidget(self.stop_button)

        self.reset_button = QPushButton("Reset", self)
        self.reset_button.clicked.connect(self.reset_timer)
        self.layout.addWidget(self.reset_button)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_counter)

        central_widget = QWidget(self)
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.timer.start(500)  # 500 milliseconds (0.5 seconds)

    def stop_timer(self):
        if self.is_running:
            self.is_running = False
            self.timer.stop()

    def reset_timer(self):
        self.counter = 0
        self.display.display(self.counter)

    def update_counter(self):
        self.counter += 1
        self.display.display(self.counter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CounterWindow()
    window.show()
    sys.exit(app.exec())