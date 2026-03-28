from data.moves import *
import csv
from rich import *


import requests


class Pokemon:
    def __init__(self, name, type, hp, attack, spatk, defense, spdef, speed, catch_rate, shiny_color, evolve_lv, evolution_str=None):
        self.name=name
        self.type=type
        self.hp=hp
        self.attack=attack
        self.spatk=spatk
        self.defense=defense
        self.spdef=spdef
        self.speed=speed
        self.base_catch=catch_rate
        self.shiny_color=shiny_color
        self.evolve_lv=evolve_lv
        self.evolution_str=evolution_str
        self.learnset={}


    @property
    def evolution(self):
        if self.evolution_str != '':
            return(globals()[self.evolution_str])
        else:
            return(None)
    

def build_pokemon():
    global mon_display
    sheet_url = 'https://docs.google.com/spreadsheets/d/1EWEy6Jk1te9or2DOsHfaZEYo7RjgzX2qKkAPGeuSShw/export?format=csv&gid=1996585217'

    data=requests.get(sheet_url).text.splitlines()

    reader=csv.DictReader(data)

    for row in reader:
        var_name=row['var_name']
        display_name=row['display_name']
        type=row['type'].split('/')
        type = [type] if isinstance(type, str) else type
        hp=int(row['hp'])
        atk=int(row['attack'])
        spatk=int(row['spatk'])
        defense=int(row['def'])
        spdef=int(row['spdef'])
        speed=int(row['speed'])
        catch_rate=int(row['catch_rate'])
        shiny_color=row['shiny_color']
        evolve_lv=int(row['evolve_level'])
        evolution_str=row['evolution']
        globals()[var_name]=Pokemon(display_name, type, hp, atk, spatk, defense, spdef, speed, catch_rate, shiny_color, evolve_lv, evolution_str)
        #print(f"[{globals()[var_name].shiny_color}]{globals()[var_name].name}[/]")


def build_learnset():
        sheet_url = 'https://docs.google.com/spreadsheets/d/1EWEy6Jk1te9or2DOsHfaZEYo7RjgzX2qKkAPGeuSShw/export?format=csv&gid=0'

        data=requests.get(sheet_url).text.splitlines()

        reader=csv.DictReader(data)

        mon_list=[]
        for row in reader:
            mon_name=row['pokemon']
            move_name=row['move']
            mon=globals()[mon_name]
            move=globals()[move_name]
            lv=int(row['level'])
            mon.learnset[lv]=move
            if mon not in mon_list:
                 mon_list.append(mon)
        
        for mon in mon_list:
            if mon.evolution!=None:
                for level in mon.learnset.keys():
                    mon.evolution.learnset[level]=mon.learnset[level]


build_pokemon()
build_learnset()


