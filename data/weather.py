from utils import *

class Weather:
    def __init__(self, duration, start_message = None, damaging = False,  dmg_immune = None):
        self.duration = duration
        self.boosted_types = []
        self.weakened_types = []
        self.start_message = start_message
        self.damaging = damaging
        self.dmg_immune = dmg_immune or []

        if self.start_message:
            self.display_start_message(start_message)

    def turn_end(self):
        self.duration -= 1
        if self.duration>0:
        
            self.turn_end_display()

        else:
            self.effect_end_display()
    
    def modify_damage(self, move_type):

        if move_type in self.boosted_types:
            return 1.5
        elif move_type in self.weakened_types:
            return .5
        else:
            return 1

    def display_start_message(self):
        print(self.start_message)

    def turn_end_display(self):
        pass
    
    def effect_end_display(self):
        pass

    def damage_pokemon(self, mon):
        if self.damaging:
            if not (mon.type in self.dmg_immune):
                dmg = (1/16 * mon.hp)
                display_damage(mon, dmg)
        


class Rain(Weather):
    def __init__(self):
        super().__init__(5, start_message = 'It starts to rain')
        self.boosted_types = ['water']
        self.weakened_types = ['fire']
    
    def turn_end_display(self):
        print('Steady rain falls onto the battlefield')
    
    def effect_end_display(self):
        print('The rainfall ends')

class Sun(Weather):
    def __init__(self):
        super().__init__(5, start_message = "The sun's intensity increases")
        self.boosted_types = ['fire']
        self.weakened_types = ['water']

    def turn_end_display(self):
        print('Harsh sunlights beats down onto the battlefield')

    def effect_end_display(self):
        print('The sun returns to normal')

#needs to increase rock spdef
class Sandstorm(Weather):
    def __init__(self):
        super().__init__(5, start_message = 'A sandstorm starts', damaging = True, dmg_immune = ['rock', 'ground', 'steel'])
        
    def turn_end_display(self):
        print('Sand continues to bite into the pokemon')

    def effect_end_display(self):
        print('The sandstorm dies down')

class Hail(Weather):
    def __init__(self):
        super().__init__(5, start_message = 'Hail begins to fall on the arena', damaging = True, dmg_immune = ['ice'])
    
    def turn_end_display(self):
        print('Hail chunks hit the pokemon')

    def effect_end_display(self):
        print('The hail stops')


#base weather state
class ClearWeather(Weather):
    def __init__(self):
        super().__init__(0)

        
