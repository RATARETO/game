class Controller:
    def __init__(self):
        self.state = "menu"  # menu, game, vin, game_over, exit

    def set_game_state(self):
        self.state = "game"

    def set_exit_state(self):
        self.state = "exit"