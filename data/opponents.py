from core.player import Player
from data.pokemon import *
from utils import *
import requests
import csv
from core.game import *

class Opponent(Player):
    def __init__(self, name, intro):
        super().__init__(game)
        self.name = name
        self.intro = intro
    def encounter(self):
        self.encounter_text()
        delay(2)
        self.game.battle.pokemon_fights(game.player, self)


    def encounter_text(self):
        print(self.intro)

def build_opponents():
    sheet = 'https://docs.google.com/spreadsheets/d/1EWEy6Jk1te9or2DOsHfaZEYo7RjgzX2qKkAPGeuSShw/export?format=csv&gid=622183923'

    data=requests.get(sheet).text.splitlines()

    reader = csv.DictReader(data)

    for row in reader:
        var_name = row['var_name']
        display_name = row['display_name']
        team_names_list = row['team'].split('/')
        team_levels_list = row['team_levels'].split('/')
        intro = row['intro']
        lv_cntr = 0
        for level in team_levels_list:
            team_levels_list[lv_cntr] = int(level)
            lv_cntr += 1 
        globals()[var_name] = Opponent(display_name, intro)
        counter = 0
        for mon_name in team_names_list:
            globals()[var_name].new_pokemon(globals()[mon_name], team_levels_list[counter])
            counter += 1 

build_opponents()

