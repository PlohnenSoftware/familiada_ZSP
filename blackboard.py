import pygame
from math import floor
from threading import Timer as Delay


class Blackboard:
    def __init__(self):
        # Initialize the blackboard containing object
        self.rows, self.cols = 10, 30
        self.letter_matrix = [["" for _ in range(self.cols)] for _ in range(self.rows)]
        self.offset = 20
        self.max_ans_len = 17
        self.answers = []
        self.spacing = 2
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
        self.program_icon = pygame.image.load("familiada.ico")
        pygame.display.set_icon(self.program_icon)
        self.refresh()

    def refresh(self):
        # Set the background color
        self.surface.fill((0, 0, 255))  # Blue background

        # Calculate dimensions for the gray rectangle
        rect_width = self.surface.get_width() - 2 * self.offset
        rect_height = self.surface.get_height() - 2 * self.offset
        pygame.draw.rect(self.surface, (81, 81, 81), (self.offset, self.offset, rect_width, rect_height))

        # Calculate dimensions and positions for the grid
        aspect_ratio_rect = 3 / 2
        aspect_ratio_grid = 16 / 9

        # Calculate the maximum possible size of the grid within the gray rectangle
        grid_width = rect_width - 2 * self.spacing
        grid_height = rect_height - 2 * self.spacing

        if grid_width / grid_height > aspect_ratio_grid:
            grid_width = grid_height * aspect_ratio_grid
        else:
            grid_height = grid_width / aspect_ratio_grid

        block_width = (grid_width - (self.cols - 1) * self.spacing) / self.cols
        block_height = block_width * aspect_ratio_rect

        # print grid and block aspect ratio, declared and calculated from final dimentions:
        print(
            f"Grid aspect ratio: {grid_width / grid_height}, Grid aspect ratio target:{aspect_ratio_grid}, Block aspect ratio: {block_height/block_width}, Block aspect ratio target:{aspect_ratio_rect}"
        )

        # Recalculate block sizes based on height constraints
        if block_height > (grid_height - (self.rows - 1) * self.spacing) / self.rows:
            block_height = (grid_height - (self.rows - 1) * self.spacing) / self.rows
            block_width = block_height / aspect_ratio_rect

        # Calculate the starting position of the grid
        start_x = self.offset + (rect_width - grid_width) / 2
        start_y = self.offset + (rect_height - grid_height) / 2

        # Initialize the font module and set the font size
        pygame.font.init()  # Initialize the font module
        font_size = max(round(block_height * 0.75), 2)  # Font size based on block height
        myfont = myfont = pygame.font.Font("familiada.ttf", font_size)  # Use default font

        # Drawing grid and text within each block
        for i in range(self.rows):
            for j in range(self.cols):
                rect_x = start_x + j * (block_width + self.spacing)
                rect_y = start_y + i * (block_height + self.spacing)
                pygame.draw.rect(self.surface, (0, 0, 0), (rect_x, rect_y, block_width, block_height))
                label = myfont.render(self.letter_matrix[i][j], True, (255, 255, 0))  # Render the text in yellow
                # Calculate text position to center it in the rectangle
                label_rect = label.get_rect(center=(rect_x + 0.5 * block_width, rect_y + 0.5 * block_height))
                self.surface.blit(label, label_rect)  # Draw text at the calculated position

        pygame.display.update()  # Update the display

    # CHECK IF TEAM INPUT IS CORRECT
    @staticmethod
    def check_team_input(team):
        if team not in ("L", "R"):
            raise ValueError("A team must be either 'L' or 'R'")

    def playsound(self, sound_id):
        self.sounds[sound_id].play()

    def stop_playing(self):
        pygame.mixer.fadeout(500)

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
        self.letter_matrix = [[char for _ in range(self.cols)] for _ in range(self.rows)]
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
            self.write_hor("_________________ --", row_coords + i, 6)

        # Write the sum
        self.write_hor("suma   0", row_coords + no_answers + 1, 18)

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
        self.write_hor(answer_text.ljust(self.max_ans_len), row_coords + answer_number, 6)
        self.write_hor(answer_points.rjust(2), row_coords + answer_number, 6 + (self.max_ans_len + 1))
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
