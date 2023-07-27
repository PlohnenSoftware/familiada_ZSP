import pygame
from math import floor
from threading import Timer as Delay


class Blackboard:
    def __init__(self):
        # Initialize the blackboard containing object
        self.letter_matrix = [["" for _ in range(29)] for _ in range(10)]
        self.stroke = 20
        self.answers = []
        self.round_score = 0
        self.current_round = -1
        self.answers_shown_final = [[True for _ in range(5)] for _ in range(2)]
        self.correct_answer = False
        self.round_winner = ""
        self.faster_team = ""

        # Initialize team scores
        self.score = {"L": 0, "R": 0}
        self.strike = {"L": 5, "R": 5}
        self.round_score = 0
        self.row_for_strike = {0: 7, 1: 4, 2: 1}

        # Initialize the music
        pygame.mixer.init()
        self.sounds = {
            "correct": pygame.mixer.Sound("sfx/correct.wav"),
            "wrong": pygame.mixer.Sound("sfx/incorrect.wav"),
            "dubel": pygame.mixer.Sound("sfx/dubel.wav"),
            "bravo": pygame.mixer.Sound("sfx/bravo.wav"),
            "write": pygame.mixer.Sound("sfx/write.wav"),
            "round": pygame.mixer.Sound("sfx/round_sound.wav"),
            "ending": pygame.mixer.Sound("sfx/final_ending.flac"),
            "intro": pygame.mixer.Sound("sfx/show_music.flac"),
        }

        # Initialize the blackboard window
        pygame.init()
        self.surface = pygame.display.set_mode((900, 700), pygame.RESIZABLE)
        pygame.display.set_caption("Familiada")
        self.programIcon = pygame.image.load("familiada.ico")
        pygame.display.set_icon(self.programIcon)
        self.refresh()

    def refresh(self):
        self.surface.fill((0, 0, 255))
        # Determine responsive width and height of the rectangles
        if self.surface.get_width() < self.surface.get_height() * (192 / 108):
            block_width = (self.surface.get_width() - 125 - (28 * 2)) / 29
            block_height = block_width * 3 / 2

            # Move blocks to the center of the screen
            block_x = 0
            block_y = (self.surface.get_height() - (block_height * 10) - (9 * 2) - 100) / 2
        else:
            block_height = (self.surface.get_height() - 100 - (9 * 2)) / 10
            block_width = block_height * 2 / 3

            # Move blocks to the center of the screen
            block_x = (self.surface.get_width() - (block_width * 29) - (28 * 2) - 125) / 2
            block_y = 0

        # Draw a grey rectangle around the game board
        rectangle_rgb = (81, 81, 81)
        rectangle_width = self.surface.get_width() - self.stroke * 2
        rectangle_height = self.surface.get_height() - self.stroke * 2
        rectangle_dimensions = (self.stroke, self.stroke, rectangle_width, rectangle_height)
        pygame.draw.rect(self.surface, rectangle_rgb, rectangle_dimensions)

        # Anti-bug SUPERmaxxx
        font_height = max(round(block_height * 0.75), 2)

        # Set the font
        myfont = pygame.font.Font("familiada.ttf", font_height)

        # Draw black rectangles & letters on the self.surface.
        for i in range(10):
            for j in range(29):
                pos_x = block_x + 50 + (block_width + 3) * j
                pos_y = block_y + 50 + (block_height + 3) * i
                label = myfont.render(self.letter_matrix[i][j], 1, (255, 255, 0))
                rectangle_rgb = (0, 0, 0)
                rectangle_dimensions = (pos_x, pos_y, block_width, block_height)
                pygame.draw.rect(self.surface, rectangle_rgb, rectangle_dimensions)
                self.surface.blit(label, (pos_x + block_width * 0.146, pos_y + block_height / 2 - font_height / 2))

        # Refresh both windows
        pygame.display.update()

    # CHECK IF TEAM INPUT IS CORRECT
    @staticmethod
    def check_team_input(team):
        if team not in ("L", "R"):
            raise ValueError("A team must be either 'L' or 'R'")

    def playsound(self, sound_ID):
        self.sounds[sound_ID].play()

    def set_global_volume(self, volume):
        for sound in self.sounds.values():
            sound.set_volume(volume)

    def set_volume(self, volume, *keys):
        for key in keys:
            if key in self.sounds:
                sound = self.sounds[key]
                sound.set_volume(volume)

    # change the team thaht is winner of the roud
    def change_winner(self):
        self.check_team_input(self.round_winner)
        if self.round_winner == "L":
            self.round_winner = "R"
        else:
            self.round_winner = "L"

    def add_score(self):
        if self.round_winner != "":
            self.score[self.round_winner] += self.round_score
            self.round_score = 0

    # Write a word horizontally
    def write_hor(self, word, start_row, start_col):
        letters = list(str(word))
        for i, letter in enumerate(letters):
            self.letter_matrix[start_row][start_col + i] = letter
        self.refresh()

    # Write a word vertically
    def write_ver(self, word, start_row, start_col):
        # niewiedzeć czemu nie działa word = str(word)
        letters = list(str(word))
        for i, letter in enumerate(letters):
            self.letter_matrix[start_row + i][start_col] = letter
        self.refresh()

    # Fill whole board with one character
    def fill(self, char=""):
        self.letter_matrix = [[char for _ in range(29)] for _ in range(10)]
        self.refresh()

    # Print a small x on selected row and column
    def draw_small_x(self, start_row, start_col):
        self.write_hor("Y", start_row, start_col + 1)
        self.write_hor("I", start_row + 1, start_col + 1)
        self.write_hor("X", start_row + 2, start_col + 1)
        for i in range(2):
            i = i << 1
            self.letter_matrix[start_row + i][start_col + i] = "G"
            self.letter_matrix[start_row - i + 2][start_col + i] = "H"
        self.refresh()

    # Print a big x on selected row and column
    def draw_gross_x(self, start_row, start_col):
        self.write_ver("DF CE", start_row, start_col)
        self.write_ver("CE DF", start_row, start_col + 2)
        self.write_hor("I", start_row + 2, start_col + 1)

    def calculate_coords(self, round_number) -> tuple:
        # Get and set some parameters of the round
        no_answers = len(self.answers[round_number])

        # Center the answers on the blackboard
        row_coords = 1 + max(floor((6 - no_answers) / 2), 0)
        return no_answers, row_coords

    # Initialize the round printing a blank blackboard
    def round_init(self, round_number):
        self.add_score()
        self.chance_reset_allowed = True
        self.round_winner = ""
        self.strike = {"L": 0, "R": 0}
        self.faster_team = ""
        self.correct_answer = False
        self.fill()
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
        # Play round SFX
        self.playsound("round")

    # Print selected answer for selected round
    def show_answer(self, round_number, answer_number):
        # Check if the answer is already printed
        if self.answers[round_number][answer_number][2]:
            return

        # Assure that the correct round is being shown
        if self.current_round != round_number:
            self.round_init(round_number)

        # Write the answer
        self.round_score = int(self.answers[round_number][answer_number][1]) + self.round_score
        no_answers, row_coords = self.calculate_coords(round_number)
        answer_text = str(self.answers[round_number][answer_number][0])
        answer_points = str(self.answers[round_number][answer_number][1])
        self.write_hor(answer_text.ljust(16), row_coords + answer_number, 6)
        self.write_hor(answer_points.rjust(2), row_coords + answer_number, 23)
        self.write_hor(str(self.round_score).rjust(3), row_coords + no_answers + 1, 22)

        self.playsound("correct")

        # Set the answer as printed
        self.answers[round_number][answer_number][2] = self.correct_answer = True

    def init_final_round(self):
        self.fill()
        self.round_winner = ""
        self.round_score = 0
        self.write_hor("suma   0", 8, 10)
        for k in range(1, 6):
            self.write_hor("----------- @@|@@ -----------", k, 0)
        self.answers_shown_final = [[False for _ in range(5)] for _ in range(2)]

    def show_scores(self):
        self.add_score()
        self.fill()
        self.write_hor("suma punktów:", 3, 8)

        # Write the scores
        l_score_str = str(self.score["L"])
        l_len = len(l_score_str)
        r_score_str = str(self.score["R"])
        r_len = len(r_score_str)
        self.write_hor(l_score_str, 5, 11 - l_len)
        self.write_hor(r_score_str, 5, 15 + r_len)

    # Function that clears all printed X from blackboard
    def clear_x(self):
        for i in range(10):
            for j in range(3):
                self.letter_matrix[i][j] = self.letter_matrix[i][j + 26] = ""

        self.strike = {"L": 0, "R": 0}
        self.refresh()

    # Draw a big x on the blackboard for a selected team and play a sound
    def big_strike(self, team):
        self.check_team_input(team)
        self.change_winner()
        if team == "L" and self.strike["L"] == 0:
            self.draw_gross_x(3, 0)
            self.strike["L"] = 4
            self.playsound("wrong")
        elif team == "R" and self.strike["R"] == 0:
            self.draw_gross_x(3, 26)
            self.strike["R"] = 4
            self.playsound("wrong")
        if self.strike["L"] == 4 and self.strike["R"] == 4:
            Delay(5, self.clear_x).start()
            self.chance_reset_allowed = False

    # Draw a small x on the blackboard for a selected team and play a sound
    def small_strike(self, team):
        self.check_team_input(team)
        current_strikes = self.strike[team]

        # Determine the row of the small x to be drawn
        if current_strikes not in (0, 1, 2):
            return
        y = self.row_for_strike[current_strikes]

        if team == "L":
            self.draw_small_x(y, 0)
        else:
            self.draw_small_x(y, 26)

        self.strike[team] = current_strikes + 1

        if current_strikes == 2:
            self.change_winner()

        self.playsound("wrong")

    def show_final_answer(self, answer_input, point_input, row, col):
        answer = str(answer_input.get())
        points = str(point_input.get())
        answer = answer.lower()

        # Check if inputs are valid
        if len(answer) > 11 or len(points) > 2 or points.isdigit() is False:
            return

        # Check if the answer is already printed
        if self.answers_shown_final[col][row]:
            return

        # Set answer as printed
        self.answers_shown_final[col][row] = True

        if col:
            answer_str = f"@@ {answer.rjust(11)}"
            output_str = f"{points.rjust(2)} {answer.rjust(11)}"
        else:
            answer_str = f"{answer.ljust(11)}"
            output_str = f"{answer.ljust(11)} {points.rjust(2)}"
        self.playsound("write")

        self.write_hor(answer_str, row + 1, col * 15)

        def show_score_for_answer():
            self.write_hor(output_str, row + 1, col * 15)
            if int(points) > 0:
                self.round_score += int(points)
                self.playsound("correct")
                self.write_hor(str(self.round_score).rjust(3), 8, 15)

            else:
                self.playsound("wrong")

        Delay(2, show_score_for_answer).start()

    def set_starting_team(self, team_signature):
        self.check_team_input(team_signature)
        if self.round_winner != "":
            return
        self.round_winner = self.faster_team = team_signature

    def incorrect_answer(self, team_signature):
        self.check_team_input(team_signature)
        if self.correct_answer and self.faster_team == team_signature:
            self.small_strike(team_signature)
        else:
            self.big_strike(team_signature)


# corrections, adding the final card and buttons to handle, start working on the function of displaying the answers from the final,
#  correct the symbol of the small loss to a more acurate one, but by doing so, the large loss should be corrected; the function from the answers
#  in the final should be finished writing; the font should be coded from large numbers and the large title caption should be coded
