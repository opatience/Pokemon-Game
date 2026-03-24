
from data.pokemon import *
import random
import csv
import requests

class Location:
    def __init__(self, name, description, lv_min, lv_max, level_cap):
        self.name=name
        self.description=description
        self.spawns={}
        self.lv_min=lv_min
        self.lv_max=lv_max
        self.level_cap=level_cap

    @property
    def level_range(self):
        return(random.randint(self.lv_min, self.lv_max))
pokemon_lab=Location('pokemon lab',
                     '',
                     {},
                     0,
                     6)

test_area=Location('Route 101',
                   'You are in a tall grassy meadow with a path through the center',
                    {pidgey: .35, weedle: .3, ekans: .3, diglett:.05},
                    random.randint(3,5),
                    100)

def build_locations():
    sheet = 'https://docs.google.com/spreadsheets/d/1EWEy6Jk1te9or2DOsHfaZEYo7RjgzX2qKkAPGeuSShw/export?format=csv&gid=1114117595'

    data = requests.get(sheet).text.splitlines()

    reader=csv.DictReader(data)

    for row in reader:
        var_name=row['var_name']
        display_name=row['Display Name']
        description=row['description']
        spawn_lv_min=int(row['spawn_lv_min'])
        spawn_lv_max=int(row['spawn_lv_max'])
        level_cap=int(row['level_cap'])
        globals()[var_name]=Location(display_name, description, spawn_lv_min, spawn_lv_max, level_cap)

def add_spawns(route, spawn_rate_dict):
    route.spawns=spawn_rate_dict


build_locations()

add_spawns(
    route_101, 
    {pidgey:.35,
     ekans:.3,
     weedle:.3,
     diglett:.05}
           )