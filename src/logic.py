from blackboard import Blackboard
from threading import Timer
from prec.helpers import calculate_coords


# @njit
def check_team_input(team):
    if team not in ("L", "R"):
        raise ValueError("A team must be either 'L' or 'R'")

class Game(Blackboard):  # Extending the Blackboard class
    def __init__(self):
        super().__init__()
        self.fgm = True  # full game mode, turns on game logic
        self.round_winner = ""  # Track the winner of the round
        self.round_score = 0  # Track the round score           
        self.answers = []# Initialize the round variables
        self.answers_shown_final = [[False for _ in range(5)] for _ in range(2)]  # Track final answers
        
    # Change the team that is winner of the round
    def change_winner(self):
        check_team_input(self.round_winner)
        if self.round_winner == "L":
            self.round_winner = "R"
        else:
            self.round_winner = "L"

            
#TODO functions to be redesigned and functionality slpit into smaller functions here & Blackboard class
############################################################################################################
    # Initialize the round printing a blank blackboard
    def round_init(self, round_number):
        self.fill()
        self.current_round = round_number
        no_answers, row_coords = calculate_coords(len(self.answers[round_number]))

        # Write the indices of the answers to the blackboard
        self.write_ver("".join([str(i) for i in range(1, no_answers + 1)]), row_coords, 4)

        # Write blank spaces to the blackboard
        for i in range(no_answers):
            self.write_hor("_" * self.max_ans_len + " --", row_coords + i, 6)

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
        no_answers, row_coords = calculate_coords(len(self.answers[round_number]))
        answer_text = str(self.answers[round_number][answer_number][0])
        answer_points = str(self.answers[round_number][answer_number][1])
        self.write_hor(answer_text.ljust(self.max_ans_len), row_coords + answer_number, 6)

        point_coor = 6 + self.max_ans_len
        self.write_hor(answer_points.rjust(2), row_coords + answer_number, point_coor + 1)
        self.write_hor(str(self.round_score).rjust(3), row_coords + no_answers + 1, point_coor)

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

        Timer(2, show_score_for_answer).start()
        ############################################################################################################
