# TODO: сделать адекватный контроллер
class Controller:
    def __init__(self):
        self.state = "menu"  # menu, game, game over, exit

    def set_game_state(self):
        self.state = "game"

    def set_exit_state(self):
        self.state = "exit"




