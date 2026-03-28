from data.interactions import *
from data.pokemon import *
from utils import *
import random
from data.natures import *
from rich import *

#------------------------------------#
#-------------PLAYER POKEMON CODE----#
#------------------------------------#

class PlayerPokemon:
    def __init__(self, pokemon, uuid, level):
        #Traits universal to all pokemon of the species
        self.base_name=pokemon.name
        self.base_hp=pokemon.hp
        self.base_attack=pokemon.attack
        self.base_spatk=pokemon.spatk
        self.base_defense=pokemon.defense
        self.base_spdef=pokemon.spdef
        self.base_speed=pokemon.speed
        self.species=pokemon
        self.type=pokemon.type
        self.evolve_lv=pokemon.evolve_lv
        self.evolution=pokemon.evolution
        self.learnset=pokemon.learnset
        self.shiny_color=pokemon.shiny_color

        #Important identifiers
        self.id=uuid
        self.level=level
        self.temp_hp=0
        self.item=0
        self.moveset=self.establish_moves()
        self.hp_iv=random.randint(1,31)
        self.defense_iv=random.randint(1,31)
        self.spdef_iv=random.randint(1,31)
        self.atk_iv=random.randint(1,31)
        self.spatk_iv=random.randint(1,31)
        self.speed_iv=random.randint(1,31)
        self.nature=random.choice(natures)
        self.shiny=False
        self.status=[]
        self.afflicted_turns=0
        self.attack_stage=0
        self.spatk_stage=0
        self.defense_stage=0
        self.spdef_stage=0
        self.speed_stage=0
        self.charging=False
        self.flinched=False
        self.trapped=False
        self.fire_spin=False
        self.trapped_time=0
        self.active_turns=0
        self.protected=False
        self.leech_seed_draining=False
        self.consecutive_protects = 0
    
        
    def evolve_pokemon(self):
        past_name=self.name
        print('Something is happening')
        delay(1)
        print('...')
        delay(1)
        print('...')
        delay(1)
        print('...')
        delay(1)
        evolution=self.evolution
        self.base_name=evolution.name
        self.base_hp=evolution.hp
        self.base_attack=evolution.attack
        self.base_spatk=evolution.spatk
        self.base_defense=evolution.defense
        self.base_spdef=evolution.spdef
        self.base_speed=evolution.speed
        self.species=evolution
        self.type=evolution.type
        self.evolve_lv=evolution.evolve_lv
        self.evolution=evolution.evolution
        self.shiny_color=evolution.shiny_color
        print(f'{past_name} evolved into {self.name}')
        delay(4)

    def new_move(self, move):
        if len(self.moveset)<4:
            self.moveset.append(move)
            print(f'{self.name} learned {move.name} | dmg {move.damage}')
            delay(3)
        elif len(self.moveset)>=4:
            print(f'{self.name} wants to learn {move.name} | dmg{move.damage}')
            delay(3)
            print(f'What move will {move.name} replace?')
            counter=1
            for move in self.moveset:
                print(counter, move.name)
                delay(.25)
                counter+=1
            print(f'{counter} Cancel')
            choice=input().strip()
            if input_check(choice, counter)==True:
                self.moveset[int(choice)-1]=move
            if input_check(choice, counter)=='return':
                return()

    def establish_moves(self):
        moveset=[]
        for key in self.species.learnset.keys():
            if self.level>=key:
                if len(moveset)<4:
                    moveset.append(self.learnset[key])
                else:
                    counter=0
                    filled=False
                    for move in moveset:
                        if self.learnset[key].damage>move.damage and filled==False:
                            moveset[counter]=self.learnset[key]
                            filled=True
                        counter+=1
        return(moveset)
        
    def nature_modifier(self, trait):
        if self.nature.increase==trait:
            return(1.1)
        if self.nature.decrease==trait:
            return(.9)
        else:
            return(1)

    #convenient shortcuts for pre-existing calls
    @property
    def hp(self):
        return(((((
            2*self.base_hp)
            +self.hp_iv)
            *self.level)
            /100)
            +self.level
            +10
            +self.hp_item)
    
    @property
    def speed(self):
        paralyzed_mult=1
        if self.status=='paralyzed':
            paralyzed_mult=.5
        return((((((
            2*self.base_speed)
            +self.speed_iv)
            *self.level
            *stages[self.speed_stage])
            /100)
            +5)
            *self.nature_modifier('speed')
            *paralyzed_mult
            +self.speed_item)
    
    @property
    def defense(self):
        return((((((
            2*self.base_defense)
            +self.defense_iv)
            *self.level
            *stages[self.defense_stage])
            /100)
            +5)
            *self.nature_modifier('defense'))

    @property
    def spdef(self):
        return((((((
            2*self.base_spdef)
            +self.spdef_iv)
            *self.level
            *stages[self.spdef_stage])
            /100)
            +5)
            *self.nature_modifier('spdef'))

    @property
    def atk(self):
        return((((((
            2*self.base_attack)
            +self.atk_iv)
            *self.level
            *stages[self.attack_stage])
            /100)
            +5)
            *self.nature_modifier('attack'))
    
    @property
    def spatk(self):
        return((((((
            2*self.base_spatk)
            +self.spatk_iv)
            *self.level
            *stages[self.spatk_stage])
            /100)
            +5)
            *self.nature_modifier('spatk'))
    
    

    @property
    def name(self):
        if self.shiny==False:
            return(self.base_name)
        elif self.shiny==True:
            return(f"[{self.shiny_color}]{self.base_name}[/]")
        
    #checks if theres an item and returns the type accordingly
    @property
    def item_type(self):
        if type(self.item)!=int:
            return(self.item.type)
        else:
            return('none')
    
    @property
    def def_iv(self):
        return(self.defense_iv)
    #-------------------------------------------------------#
    #item checks that only do something if the type is there#
    #-------------------------------------------------------#
    @property
    def attack_item(self):
        if self.item_type=='attack':
            return(self.item.strength)
        else:
            return(0)
        
    @property
    def speed_item(self):
        if self.item_type=='speed':
            return(self.item.strength)
        else:
            return(0)
    
    @property
    def hp_item(self):
        if self.item_type=='hp':
            return(self.item.strength)
        else:
            return(0)
        
    

