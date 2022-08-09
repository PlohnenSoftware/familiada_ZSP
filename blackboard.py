import pygame
import sys
import tkinter
import os
from math import floor
from tkinter import messagebox, ttk, filedialog

# Import pygame SFX
pygame.mixer.init()
correct_sound = pygame.mixer.Sound("sfx/correct.wav")
wrong_sound = pygame.mixer.Sound("sfx/incorrect.wav")
dubel_sound = pygame.mixer.Sound("sfx/dubel.wav")
bravo_sound = pygame.mixer.Sound("sfx/bravo.wav")
write_sound = pygame.mixer.Sound("sfx/write.wav")
ending_music = pygame.mixer.Sound("sfx/final_ending.flac")
intro_music = pygame.mixer.Sound("sfx/show_music.flac")

class Blackboard:
    def __init__(self, stroke):
        self.letter_matrix = [["" for _ in range(29)] for _ in range(10)]
        self.stroke = stroke
        self.answers = []
        self.round_score = 0
        self.current_round = -1

        # Initialize team scores
        self.l_score = 0
        self.r_score = 0
        self.l_strike = 0
        self.r_strike = 0
        self.round_score = 0
        self.winning_team = None

    # Write a word horizontally to the matrix
    def write_hor(self, word, start_row, start_col):
        letters = list(str(word))
        for i, letter in enumerate(letters):
            self.letter_matrix[start_row][start_col + i] = letter

    # Write a word vertically to the matrix
    def write_ver(self, word, start_row, start_col):
        # niewiedzeć czemu nie działa word = str(word)
        letters = list(str(word))
        for i, letter in enumerate(letters):
            self.letter_matrix[start_row + i][start_col] = letter

    # Fill whole board with one character
    def fill(self, char=""):
        self.letter_matrix = [[char for _ in range(29)] for _ in range(10)]

    # Print a small x on selected row and column
    def draw_small_x(self, start_row, start_col):
        for i in range(3):
            self.letter_matrix[start_row + i][start_col + i] = "#"
            self.letter_matrix[start_row - i + 2][start_col + i] = "#"

    # Print a big x on selected row and column
    def draw_gross_x(self, start_row, start_col):
        self.draw_small_x(start_row + 1, start_col)
        for j in range(2):
            for i in range(2):
                self.write_hor("#", start_row + j * 4, start_col + i * 2)

    # Draw a big x on the blackboard for a selected team and play a sound
    def show_big_x(self, team):
        if team not in ("L", "R"):
            exception = ValueError("Team must be either 'L' or 'R'")
            raise exception
        if team == "L":
            self.draw_gross_x(3, 0)
        else:
            self.draw_gross_x(3, 26)
        pygame.mixer.Sound.play(wrong_sound)

    # Draw a small x on the blackboard for a selected team and play a sound
    def show_small_x(self, team):
        if team not in ("L", "R"):
            exception = ValueError("Team must be either 'L' or 'R'")
            raise exception
        if team == "L":
            self.draw_small_x(2, 0)
        else:
            self.draw_small_x(2, 26)
        pygame.mixer.Sound.play(wrong_sound)

    def calculate_coords(self, round_number) -> tuple:
        # Get and set some parameters of the round
        no_answers = len(self.answers[round_number])

        # Center the answers on the blackboard
        row_coords = 1 + max(floor((6 - no_answers) / 2), 0)
        return no_answers, row_coords

    def add_score(self):
        if self.winning_team == "L":
            self.l_score += self.round_score
        else:
            self.r_score += self.round_score

    # Initialize the round printing a blank blackboard
    def round_init(self, round_number):
        self.add_score()
        self.round_score = 0
        self.fill()
        self.round_score = 0
        self.current_round = round_number
        no_answers, row_coords = self.calculate_coords(round_number)

        # Write the indices of the answers to the blackboard
        self.write_ver("".join([str(i) for i in range(1, no_answers + 1)]), row_coords, 4)

        # Write blank spaces to the blackboard
        for i in range(no_answers):
            self.write_hor("________________ --", row_coords + i, 6)

        # Write the sum
        self.write_hor("suma   0", row_coords + no_answers + 1, 17)

        for round_answers in self.answers:
            for answer in round_answers:
                answer[2] = True

        # Set the answers as not printed
        for answer_dict in self.answers[round_number]:
            answer_dict[2] = False

    # Print selected answer for selected round
    def print_answer(self, round_number, answer_number):

        # Check if the answer is already printed
        if self.answers[round_number][answer_number][2]:
            return

        # Assure that the correct round is being shown
        if self.current_round != round_number:
            self.round_init(round_number)

        self.round_score = int(self.answers[round_number][answer_number][1]) + self.round_score
        no_answers, row_coords = self.calculate_coords(round_number)
        answer_text = str(self.answers[round_number][answer_number][0])
        answer_points = str(self.answers[round_number][answer_number][1])
        self.write_hor(answer_text.ljust(16), row_coords + answer_number, 6)
        self.write_hor(answer_points.rjust(2), row_coords + answer_number, 23)
        self.write_hor(str(self.round_score).rjust(3), row_coords + no_answers + 1, 22)
        pygame.mixer.Sound.play(correct_sound)

        # Set the answer as printed
        self.answers[round_number][answer_number][2] = True

    def init_final_round(self):
        self.fill()
        self.write_hor("suma   0", 8, 10)
        for k in range(1, 6):
            self.write_hor("----------- @@|@@ -----------", k, 0)

    def show_scores(self):
        self.add_score()
        self.fill()
        self.write_hor("suma punktów:", 3, 8)

        # Write the scores
        l_score_str = str(self.l_score)
        l_len = len(l_score_str)
        r_score_str = str(self.r_score)
        r_len = len(r_score_str)
        self.write_hor(l_score_str, 5, 11 - l_len)
        self.write_hor(r_score_str, 5, 15 + r_len)

    def set_current_winner(self, winner):
        self.winning_team = winner

def pit():
    return 0