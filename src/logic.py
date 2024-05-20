from blackboard import Blackboard

class Game(Blackboard):  # Extending the Blackboard class
    def __init__(self):
        super().__init__()
        self.fgm = True  # full game mode, turns on game logic