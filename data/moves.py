import requests
import csv

class Move:
    def __init__(self, name, power, type, category, effect, chance, magnitude, accuracy):
        self.name = name
        self.damage = power
        self.type = type
        self.category = category
        self.effect = effect
        self.effect_chance = chance
        self.effect_magnitude = magnitude
        self.accuracy = accuracy

    @property
    def magnitude(self):
        return(self.effect_magnitude)
        
    @property
    def chance(self):
        return(self.effect_chance)

def build_moves():
    sheet_url = 'https://docs.google.com/spreadsheets/d/1EWEy6Jk1te9or2DOsHfaZEYo7RjgzX2qKkAPGeuSShw/export?format=csv&gid=912195015'

    data=requests.get(sheet_url).text.splitlines()

    reader=csv.DictReader(data)


    for row in reader:
        move_var_name=row['var_name']
        move_display_name=row['display_name']
        move_damage=int(row['damage'])
        move_type=row['type']
        move_category=row['category']
        move_effect=row['effect']
        move_chance=row['chance']
        move_magnitude=row['magnitude']
        move_accuracy=(int(row['accuracy'])/100)
        if '/' in row['effect']:
            move_effect=move_effect.split('/')
            move_chance=move_chance.split('/')
            move_magnitude=move_magnitude.split('/')
            ci=0 #chance index
            for chance in move_chance:
                move_chance[ci]=(int(chance)/100)
                ci+=1
            mi=0 #magnitude index
            for magnitude in move_magnitude:
                if magnitude[0]=='0':
                    move_magnitude[mi]=float(magnitude)
                else:
                    move_magnitude[mi]=int(magnitude)
                mi+=1
        elif move_magnitude[0]=='0':
            move_chance=int(move_chance)/100
            move_magnitude=float(move_magnitude)
        else:
           move_chance=int(move_chance)/100
           move_magnitude=int(move_magnitude)
        globals()[move_var_name]=Move(move_display_name, move_damage, move_type, move_category, move_effect, move_chance, move_magnitude, move_accuracy)

build_moves()
