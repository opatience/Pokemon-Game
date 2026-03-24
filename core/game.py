from core.player import Player
from core.menu import Menu
from core.actions import Actions
from core.battle import Battle
from core.logic import Logic

class Game:

    def __init__(self):
        self.player = Player(self)
        self.menu = Menu(self)
        self.actions = Actions(self)
        self.battle = Battle(self)
        self.logic = Logic(self)

game=Game()