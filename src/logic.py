from blackboard import Blackboard
from threading import Timer
from prec.helpers import calculate_coords


# @njit
def check_team_input(team: str) -> None:
    if team not in ("L", "R"):
        raise ValueError("A team must be either 'L' or 'R'")

class Game(Blackboard):  # Extending the Blackboard class
    def __init__(self):
        super().__init__()
        self.fgm = True  # full game mode, turns on game logic
        self.round_winner = ""  # Track the winner of the round
        self.round_score = 0  # Track the round score           
        self.answers = []  # Initialize the round variables
        self.answers_shown_final = [[False for _ in range(5)] for _ in range(2)]  # Track final answers
        
        # Game state variables
        self.teams = {
            "L": {"score": 0, "strikes": 0, "display_name": "Drużyna Lewa"},
            "R": {"score": 0, "strikes": 0, "display_name": "Drużyna Prawa"}
        }
        self.current_round = 0
        self.total_rounds = 0
        self.active_team = ""  # Team currently playing (L or R)
        self.current_player_index = {"L": 0, "R": 0}  # Current player index for each team
        self.face_off_state = "initial"  # initial, first_player, second_player, control_decided
        self.face_off_first_answer = None
        self.game_phase = "setup"  # setup, face_off, main_play, opponent_steal, round_end, final_round
        self.correct_answer = False  # Was the last answer correct?
        
    # Change the team that is winner of the round
    def change_winner(self):
        check_team_input(self.round_winner)
        if self.round_winner == "L":
            self.round_winner = "R"
        else:
            self.round_winner = "L"
            
    def set_starting_team(self, team: str) -> None:
        """Set the team that starts the round after winning face-off"""
        check_team_input(team)
        self.active_team = team
        self.game_phase = "main_play"
        self.reset_strikes()
        self.round_winner = team  # Set the active team as the potential round winner right away
        
        # Display which team has control
        self.fill()
        self.write_hor(f"{self.teams[team]['display_name']} zaczyna grę!", 4, 5)
        Timer(2, lambda: self.round_init(self.current_round)).start()
    
    def reset_strikes(self):
        """Reset strikes for both teams"""
        self.teams["L"]["strikes"] = 0
        self.teams["R"]["strikes"] = 0
        
    def get_opponent_team(self, team: str) -> str:
        """Get the opposing team"""
        check_team_input(team)
        return "R" if team == "L" else "L"
    
    def incorrect_answer(self, team: str) -> None:
        """Handle an incorrect answer for the specified team"""
        # Jeśli nie podano drużyny (None) lub podana drużyna nie jest aktywna,
        # użyj aktualnie aktywnej drużyny
        if team is None or team not in ("L", "R") or team != self.active_team:
            team = self.active_team
            
        # Tylko w fazie głównej rozgrywki obsługuj błędne odpowiedzi
        if self.game_phase == "main_play" and team and team == self.active_team:
            self.teams[team]["strikes"] += 1
            self.playsound("wrong")
            
            # Draw the X on the board
            no_answers, row_coords = calculate_coords(len(self.answers[self.current_round]))
            strike_position = 2 + self.teams[team]["strikes"]
            
            # Draw small or big X depending on strike number
            if self.teams[team]["strikes"] < 3:
                self.draw_small_x(row_coords + no_answers + 1, strike_position)
                # Move to next player after an incorrect answer
                self.next_player_turn()
            else:
                self.draw_big_x(row_coords + no_answers + 1, strike_position)
                # After 3 strikes, switch to opponent steal phase
                Timer(1, lambda: self.start_opponent_steal()).start()
    
    def start_opponent_steal(self):
        """Switch to opponent steal phase after 3 strikes"""
        self.game_phase = "opponent_steal"
        opponent = self.get_opponent_team(self.active_team)
        self.fill()
        self.write_hor(f"{self.teams[opponent]['display_name']} ma szansę na kradzież!", 4, 3)
    
    def process_steal_attempt(self, answer_number: int):
        """Process the opponent team's steal attempt"""
        if self.game_phase != "opponent_steal":
            return
            
        # Get the opponent team (the one trying to steal)
        opponent = self.get_opponent_team(self.active_team)
            
        # Check if the answer exists and is not already shown
        if answer_number < len(self.answers[self.current_round]) and not self.answers[self.current_round][answer_number][2]:
            # Show the answer
            self.show_answer(self.current_round, answer_number)
            
            # Successful steal - transfer round points to opponent by changing round_winner
            self.round_winner = opponent
            
            # Announce the steal
            self.fill()
            self.write_hor(f"{self.teams[opponent]['display_name']} kradnie punkty!", 4, 5)
            
            # End the round after delay
            Timer(2, lambda: self.end_round()).start()
        else:
            # Failed steal - original team keeps points (round_winner remains unchanged)
            self.playsound("wrong")
            
            # Announce failed steal
            self.fill()
            self.write_hor(f"{self.teams[self.active_team]['display_name']} zachowuje punkty!", 4, 3)
            
            # End the round after delay
            Timer(2, lambda: self.end_round()).start()
    
    def end_round(self):
        """End the current round and update scores"""
        # Apply round multiplier based on round number
        multiplier = 1
        if self.current_round == 1:  # second round
            multiplier = 2
        elif self.current_round >= 2:  # third round and beyond
            multiplier = 3
            
        final_round_score = self.round_score * multiplier
        
        # Add points to the winning team (determined by round_winner)
        if self.round_winner:
            self.teams[self.round_winner]["score"] += final_round_score
            
            # Show the updated score
            self.fill()
            self.write_hor(f"Koniec rundy {self.current_round + 1}!", 2, 8)
            self.write_hor(f"{self.teams['L']['display_name']}: {self.teams['L']['score']} punktów", 4, 5)
            self.write_hor(f"{self.teams['R']['display_name']}: {self.teams['R']['score']} punktów", 6, 5)
            
            # Show which team won the round
            self.write_hor(f"Rundę wygrywa: {self.teams[self.round_winner]['display_name']}", 8, 5)
            
            # Check if game should end
            if max(self.teams["L"]["score"], self.teams["R"]["score"]) >= 300 or self.current_round >= 2:
                Timer(3, lambda: self.check_game_end()).start()
            else:
                # Move to next round
                self.current_round += 1
                self.game_phase = "face_off"
                self.round_score = 0
                self.round_winner = ""  # Reset round winner for next round
                self.active_team = ""  # Reset active team for next round's face-off
                Timer(3, lambda: self.prepare_face_off()).start()
    
    def check_game_end(self):
        """Check if the game should end or go to sudden death"""
        # If any team has 300+ points, they win
        if self.teams["L"]["score"] >= 300:
            self.handle_game_win("L")
        elif self.teams["R"]["score"] >= 300:
            self.handle_game_win("R")
        # If we've played at least 3 rounds and no winner, go to sudden death
        elif self.current_round >= 2:
            self.start_sudden_death()
        else:
            # Continue to next round
            self.current_round += 1
            self.game_phase = "face_off"
            self.round_score = 0
            self.round_winner = ""
            self.active_team = ""
            self.prepare_face_off()
    
    def start_sudden_death(self):
        """Start the sudden death round"""
        self.fill()
        self.write_hor("RUNDA NAGŁEJ ŚMIERCI!", 4, 6)
        self.game_phase = "sudden_death"
        
        # Reset for sudden death
        self.round_score = 0
        self.round_winner = ""
        self.active_team = ""
        
        # Initialize sudden death round
        Timer(2, lambda: self.round_init(self.current_round)).start()
    
    def handle_sudden_death_answer(self, team: str, answer_number: int):
        """Handle a sudden death answer attempt"""
        if self.game_phase != "sudden_death":
            return
            
        check_team_input(team)
        
        # Check if it's the top answer (index 0)
        if answer_number == 0:
            # Show the answer
            self.show_answer(self.current_round, answer_number)
            
            # Team wins the game
            self.handle_game_win(team)
        else:
            # Not the top answer, other team gets a chance
            self.playsound("wrong")
            opponent = self.get_opponent_team(team)
            
            # Show message
            self.fill()
            self.write_hor(f"To nie najlepsza odpowiedź!", 3, 5)
            self.write_hor(f"{self.teams[opponent]['display_name']} ma szansę!", 5, 5)
    
    def handle_game_win(self, team: str):
        """Handle a team winning the game"""
        check_team_input(team)
        
        self.fill()
        self.write_hor(f"{self.teams[team]['display_name']} wygrywa grę!", 3, 5)
        self.write_hor(f"Wynik: {self.teams[team]['score']} punktów", 5, 5)
        
        # Play fanfare
        self.playsound("bravo")
        
        # Move to final round
        Timer(5, lambda: self.init_final_round()).start()
    
    def prepare_face_off(self):
        """Prepare for the face-off phase at the start of a round"""
        self.fill()
        self.write_hor("Runda " + str(self.current_round + 1), 2, 12)
        self.write_hor("Kapitanowie drużyn do środka!", 4, 6)
        self.game_phase = "face_off"
        self.face_off_state = "initial"
        self.face_off_first_answer = None
    
    def handle_face_off_input(self, team: str, answer_number: int):
        """Handle input during the face-off phase"""
        if self.game_phase != "face_off":
            return
            
        check_team_input(team)
        
        # First player's answer
        if self.face_off_state == "initial":
            if answer_number < len(self.answers[self.current_round]) and not self.answers[self.current_round][answer_number][2]:
                # Record first player's answer
                self.face_off_first_answer = {
                    "team": team,
                    "answer_number": answer_number
                }
                
                # Show the answer
                self.show_answer(self.current_round, answer_number)
                
                # Move to second player state
                self.face_off_state = "second_player"
                
                # Show message for other team
                opponent = self.get_opponent_team(team)
                self.write_hor(f"{self.teams[opponent]['display_name']} spróbuj podać wyższą odpowiedź!", 7, 3)
            else:
                # Invalid or already shown answer
                self.playsound("wrong")
                
                # Give chance to other team
                opponent = self.get_opponent_team(team)
                self.face_off_state = "second_player"
                self.write_hor(f"{self.teams[opponent]['display_name']} twoja kolej!", 7, 7)
                
        # Second player's answer
        elif self.face_off_state == "second_player":
            if answer_number < len(self.answers[self.current_round]) and not self.answers[self.current_round][answer_number][2]:
                # Show the answer
                self.show_answer(self.current_round, answer_number)
                
                # Compare answers to determine control
                if self.face_off_first_answer and answer_number < self.face_off_first_answer["answer_number"]:
                    # Second player's answer is higher ranked (lower index)
                    self.set_starting_team(team)
                else:
                    # First player keeps control
                    first_team = self.face_off_first_answer["team"] if self.face_off_first_answer else team
                    self.set_starting_team(first_team)
            else:
                # Invalid or already shown answer - first player wins
                self.playsound("wrong")
                
                if self.face_off_first_answer:
                    # First player gets control
                    self.set_starting_team(self.face_off_first_answer["team"])
                else:
                    # Neither player got a valid answer, restart face-off
                    self.prepare_face_off()
    
    # Initialize the round printing a blank blackboard
    def round_init(self, round_number: int) -> None:
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
        
        # If we're in main play phase, show team scores and strikes
        if self.game_phase == "main_play" and self.active_team:
            self.write_hor(f"L: {self.teams['L']['score']} | R: {self.teams['R']['score']}", 1, 10)
            self.write_hor(f"Gra: {self.teams[self.active_team]['display_name']}", 2, 10)
            
            # Reset player index for the active team for a new round
            self.current_player_index[self.active_team] = 0
            
            # Show current player
            player_num = self.current_player_index[self.active_team] + 1
            self.write_hor(f"Gracz {player_num} odpowiada", 9, 10)

    # Print selected answer for selected round and handle game logic
    def show_answer(self, round_number: int, answer_number: int) -> None:
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
        
        # If we're in main play phase, check if all answers are revealed 
        # and move to next player after a correct answer
        if self.game_phase == "main_play" and self.active_team:
            # Check if all answers are revealed
            all_revealed = True
            for answer in self.answers[round_number]:
                if not answer[2]:  # If any answer is not revealed, we continue
                    all_revealed = False
                    break
                    
            if all_revealed:
                # All answers revealed, round winner is current active team
                # (round_winner should already be set to active_team)
                Timer(1, lambda: self.end_round()).start()
            else:
                # Move to the next player after a correct answer
                self.next_player_turn()

    def next_player_turn(self):
        """Move to the next player in the active team"""
        if self.game_phase != "main_play" or not self.active_team:
            return
            
        # Increment player index for active team (cycling 0-4)
        self.current_player_index[self.active_team] = (self.current_player_index[self.active_team] + 1) % 5
        
        # Show message for next player
        player_num = self.current_player_index[self.active_team] + 1
        self.write_hor(f"{self.teams[self.active_team]['display_name']} - gracz {player_num}", 9, 10)

    def init_final_round(self) -> None:
        """Initialize the Fast Money (final) round"""
        self.fill()
        self.game_phase = "final_round"
        self.round_winner = ""
        self.round_score = 0
        self.active_team = ""  # No active team in final round
        self.write_hor("RUNDA FINAŁOWA", 1, 10)
        self.write_hor("suma   0", 8, 10)
        for k in range(1, 6):
            self.write_hor("----------- @@|@@ -----------", k, 0)
        self.answers_shown_final = [[False for _ in range(5)] for _ in range(2)]

    def show_final_answer(self, answer_input, point_input, row: int, col: int) -> None:
        """Show an answer in the final round (Fast Money)"""
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
                
                # Check if final score is enough to win
                if self.round_score >= 200:
                    Timer(1, lambda: self.handle_final_round_win()).start()
            else:
                self.playsound("wrong")

        Timer(2, show_score_for_answer).start()
        
    def handle_final_round_win(self):
        """Handle win in the final round"""
        self.fill()
        self.write_hor("BRAWO! WYGRANA!", 4, 10)
        self.write_hor(f"Zdobyte punkty: {self.round_score}", 6, 8)
        self.playsound("bravo")
