import uuid
from data.interactions import *
from core.player_pokemon import PlayerPokemon
from utils import *
import math
from rich import *
import random

class Player:
    #sets up the wild encounter battle code
    def wild_encounter(self, pokemon):
       shiny_roll=random.random()
       new_screen()
       print(f'You have encountered a wild {pokemon.name}\n')
       delay(2)
       wild_cpu=Player(self.game)
       wild_cpu.new_pokemon(pokemon, self.game.player.location.level_range)
       wild_cpu.wild=True
       if shiny_roll>=.95:
           wild_cpu.team[0].shiny=True
       self.game.battle.pokemon_fights(self, wild_cpu)

    #adds a new pokemon to a players team, setting it's uuid and indexes
    def new_pokemon(self, pokemon, level, shiny=False):
        tag=uuid.uuid4
        tag=PlayerPokemon(pokemon, uuid, level)
        tag.shiny=shiny
        self.pokemon.append(tag)
        self.check_team_availability(tag)

    #runs through your team to see if the mon can be added
    def check_team_availability(self, mon_id):
        if len(self.team)<6:
            self.team.append(mon_id)
            return()

    #prints the name and level of your entire team
    @property
    def show_team(self):
        for pokemon in self.team:
            if pokemon != '':
                print(f'{pokemon.name}, Level {pokemon.level}')
    
    #prints the name and level of your entire box
    @property
    def show_box(self):
        for pokemon in self.pokemon:
            if not(pokemon in self.team):
                print(f'{pokemon.name}, Level {pokemon.level}')

        
    #establishes temp hp for your team
    @property 
    def set_team_hp(self):
        for pokemon in self.team:
            if pokemon != '':
                pokemon.temp_hp=pokemon.hp
    
    @property
    def reset_conditions(self):
        for pokemon in self.team:
            pokemon.defense_stage=0
            pokemon.spdef_stage=0
            pokemon.attack_stage=0
            pokemon.spatk_stage=0
            pokemon.speed_stage=0
            pokemon.status=[]
            pokemon.afflicted_turns=0
            pokemon.active_turns=0
            pokemon.trapped_time=0
            pokemon.charging = False


    #sets the conditions needed for battle to work
    def setup_battle(self, opponent):
        self.set_team_hp
        self.active_pokemon=self.team[0]
        self.fainted=[]
        self.opponent=opponent
        self.ran=False
        self.reset_conditions


    def faint_logic(self):
        switch=False
        self.fainted.append(self.active_pokemon)
        for pokemon in self.team:
            if pokemon != '' and pokemon not in self.fainted:
                self.game.actions.switch(self)
                switch=True
                return(False)
        if switch==False:
            return(True)
        
    def cpu_faint(self):
        switch=False
        self.fainted.append(self.active_pokemon)
        for pokemon in self.team:
            if pokemon != '' and not(pokemon in self.fainted):
                self.active_pokemon=pokemon
                switch=True
                break
        if switch==False:
            return(True)

    def cpu_attack(self, player, cpu_move_choice):
        self.game.logic.trapped_check(self)
        accuracy_check=random.random()
        if accuracy_check>=cpu_move_choice.accuracy:
            print(f'\n{self.aname} missed\n')
            delay(2)
            return()
        delay(2)
        print(f'\n{self.aname} used {cpu_move_choice.name}')
        delay(2)
        dmg=self.battle.calculate_damage(cpu_move_choice, player.active_pokemon, self.active_pokemon)
        player.active_pokemon.temp_hp-=dmg


        if dmg>0:
            self.game.logic.effectiveness_check(player.active_pokemon, cpu_move_choice)
        
            print(f'{self.aname} did {math.ceil(dmg)} damage')
            delay(2)
        
        if player.active_pokemon.temp_hp>0 and dmg>0:
            print(f'Your {player.active_pokemon.name} has {round((player.active_pokemon.temp_hp/player.active_pokemon.hp)*100)}% hp remaining\n')
        elif player.active_pokemon.temp_hp<=0:
            print(f'Your {player.active_pokemon.name} has 0% hp remaining\n')
        delay(2)
        if cpu_move_choice.effect != 'none':
            self.game.logic.move_effect(cpu_move_choice, self.active_pokemon, player.active_pokemon)


    def acquire_item(self, item, quanity):
        already_have=False
        for key in self.inventory.keys():
            if item==key:
                already_have=True
        if already_have==False:
            self.inventory[item]=quanity
        else:
            self.inventory[item]+=quanity
  
            
    #------------------------------------------#
    #-----------PLAYER VARIABLES---------------#
    #------------------------------------------#


            
    def __init__(self, game):
        self.name = ''
        self.starter=''
        self.pokemon=[]
        self.team=[]
        self.active_pokemon=''
        self.wild=False
        #make with uuid now
        self.team_hp={}
        #make with uuid
        self.fainted=[]
        self.money=0
        self.location=''
        self.inventory={'pokeball':0}
        self.mon_caught=False
        self.new_area=True
        #chopped ass way of coding run
        self.ran=False
        #stores the levels of all your pokemon
        self.mon_level={}
        #tracks opponent for easier wild code
        self.opponent=''
        self.game=game
        self.proceed=False
        self.encounter_display = None
#Convenient Player Shortcuts

    #Active Pokemon Health
    @property
    def ahp(self):
        return(self.active_pokemon.temp_hp)
    
    #Active Pokemon Name
    @property
    def aname(self):
        return(self.active_pokemon.name)
    
    #Active Pokemon
    @property
    def amon(self):
        return(self.active_pokemon)




#Shortcuts to make accessing stuff easier, exist in most modules
    @property
    def menu(self):
       return(self.game.menu)
   
    @property
    def action(self):
       return(self.game.actions)
   
    @property
    def battle(self):
        return(self.game.battle)






