\
import random


class Player:
    @property 
    def set_team_hp(self):
        for pokemon in self.team:
            if pokemon != '':
                self.team_hp[pokemon]=pokemon.base_hp+(self.pokemon_level[pokemon]*pokemon.hp_multiplier)
    
    @property
    def active_hp(self):
        return(self.team_hp[self.active_pokemon])
    
    @property
    def move_dmg(self, move_choice):
        return(move_choice.damage*self.pokemon_level[self.active_pokemon])

    #Builds a set of options for an area you enter
    def display_menu(self):
        if self.new_area==True:
            self.new_area=False
            new_screen()
            area=self.location
            print(f'You have entered {area.name}\n\n')
            delay(2)
            print(f'{area.description}\n\n')
        delay(2)
        print('What do you want to do?')
        delay(2)
        options_text=['Proceed', 'Explore']#, 'Adjust Pokemon', "Shop"]
        options=[self.proceed, self.explore] #self.adjust_pokemon, self.shop]#self.items, self.backtrack
        choices={}
        for index, option in enumerate(options_text):
            choices[index+1]=options[index]
            print(index+1, option)
            delay(.25)
        choice=int(input().strip())
        if choice in(1, 2, 3, 4):
            choices[choice]()
        else:
            print("That's not an option, try again")
            self.display_menu()

    #brings you to the next area
    def proceed(self):
        self.new_area=True
        return()
    
    #rolls for a wild pokemon
    def explore(self):
        spawns=player.location.spawns
        spawn_range=[]
        spawn_outcome=[]
        for key in spawns.keys():
            spawn_outcome.append(key)
            spawn_range.append(spawns[key])
        if len(player.location.spawns)>0:
            roll=random.random()
            if roll<=spawn_range[0]:
                player.wild_encounter(spawn_outcome[0])
            elif roll>spawn_range[0] and roll<=sum(spawn_range[0:2]):
                player.wild_encounter(spawn_outcome[1])
            elif roll>sum(spawn_range[0:2]) and roll<=sum(spawn_range[0:3]):
                player.wild_encounter(spawn_outcome[2])
            elif roll>sum(spawn_range[0:3]) and roll<=sum(spawn_range[0:4]):
                player.wild_encounter(spawn_outcome[3])
            elif roll>sum(spawn_range[0:4]) and roll<=sum(spawn_range[0:5]):
                player.wild_encounter(spawn_outcome[4])
            elif roll>sum(spawn_range[0:5]) and roll<=sum(spawn_range[0:6]):
                player.wild_encounter(spawn_outcome[5])
            elif roll>sum(spawn_range[0:6]) and roll<=sum(spawn_range[0:7]):
                player.wild_encounter(spawn_outcome[6])
        else:
            print('You find nothing here')
            self.display_menu()

    #sets up your fight with a wild pokemon
    def wild_encounter(self, pokemon):
        print(f'You have encountered a wild {pokemon.name}')
        wild_cpu=Player()
        wild_cpu.name=pokemon.name
        wild_cpu.wild=True
        wild_cpu.team=[pokemon]
        wild_cpu.pokemon_level[pokemon]=player.location.level_range
        player.pokemon_fights(wild_cpu)

    #sets the conditions needed for battle to work
    def setup_battle(self):
        self.set_team_hp
        self.active_pokemon=self.team[0]
        self.fainted=[]

    def faint_logic(self, cpu):
        switch=False
        self.fainted.append(self.active_pokemon)
        for pokemon in self.team:
            if pokemon in self.fainted==False and not(''):
                self.active_pokemon.switch(cpu)
                switch=True
                break
        if switch==False:
            return('lose')
        
    def cpu_faint(self):
        switch=False
        self.fainted.append(self.active_pokemon)
        for pokemon in self.team:
            if pokemon != '' and not(pokemon in self.fainted):
                print(pokemon)
                self.active_pokemon=pokemon
                switch=True
                break
        if switch==False:
            return('lose')

            
    def pokemon_fights(self, cpu):
        self.setup_battle()
        cpu.setup_battle()
        while cpu.active_hp>0 and self.active_hp>0:
            self.player_choice(cpu)
            if cpu.active_hp>0 and self.active_hp>0:
                if cpu.mon_caught==True:
                    cpu.mon_caught=False
                    return()
                elif self.ran==True:
                    self.ran=False
                    return()
                else:
                    cpu.active_pokemon.cpu_attack(self.active_pokemon, cpu)
            if self.active_hp<=0:
               delay(2)
               print(f'{self.active_pokemon.name} Fainted')
               if self.faint_logic(cpu)=='lose':
                    print('You Lose')
                    if cpu.wild==True:
                        player.display_menu()
                    else:
                        return()
            elif cpu.active_hp<=0:
                delay(2)
                print(f'{cpu.active_pokemon.name} Fainted')
                if cpu.cpu_faint()=='lose':
                    delay(2)
                    xp_split=0
                    for pokemon in player.team:
                        if pokemon != '':
                            if player.pokemon_level[pokemon]<player.location.level_cap:
                                xp_split+=1
                    for pokemon in player.team:
                        if pokemon != '':
                            if player.pokemon_level[pokemon]<player.location.level_cap:
                                prior_level=player.pokemon_level[pokemon]
                                player.pokemon_level[pokemon]+=(1/xp_split)
                                if prior_level != round(player.pokemon_level[pokemon]):
                                    print(f'{pokemon.name} leveled up to level {int(player.pokemon_level[pokemon])}')
                                    print(f'{pokemon.name} gained {pokemon.hp_multiplier} hp')
                                else:
                                    print(f'{pokemon.name} gained {1/xp_split} levels')
                            else:
                                print(f'{pokemon.name} is at the level cap of {player.location.level_cap}') 
                                print('Proceed to the next zone to level them again')
                    print('You Win!')
                    if cpu.wild==True:
                        player.display_menu()
                    else:
                        return()
            

    def player_choice(self, cpu):
        switch=False
        delay(1)
        print(f'{self.name}: Go {self.active_pokemon.name}!')
        delay(1)
        print(f'What will {self.name} do?')
        for slot in self.team:
            if slot != self.active_pokemon and not(slot=='') and not(slot in self.fainted):
                switch=True
        options_string=['attack']
        options=[self.active_pokemon.attack]
        if switch==True:
            options_string.append('switch')
            options.append(self.active_pokemon.switch)
        if cpu.wild==True:
            if player.inventory[pokeball.name]>0:
                options_string+=['catch', 'run']
                options+=[cpu.active_pokemon.catch, self.run]
            else:
                options_string+=['run']
                options+=[self.run]
        result={}
        for number, option in enumerate(options_string):
            result[number+1]=options[number]
            print(number+1, option)
            delay(.25)
        choice=int(input().strip())
        if choice in ((1, 2, 3, 4)):
            print(choice)
            delay(.25)
            result[choice](cpu)
        else:
            print("That's not an option")
            self.player_choice(cpu)
        
    def run(self, cpu):
        delay(1)
        print('You fled the battle')
        self.ran=True
        self.display_menu()
        return()
            
    def __init__(self):
        self.name=''
        self.starter=''
        self.pokemon=[]
        self.team=['','','','','','']
        self.active_pokemon=''
        self.wild=False
        self.team_hp={}
        self.fainted=[]
        self.money=0
        self.location=''
        self.inventory={'pokeball':0}
        self.mon_caught=False
        self.new_area=True
        #chopped ass way of coding run
        self.ran=False
        #stores the levels of all your pokemon
        self.pokemon_level={}
        
    
    
player=Player()
rival=Player()


pokemon_types = {'bulbasaur':'grass',
                 'charmander':'fire',
                 'squirtle': 'water',
                 'pidgey': 'flying',
                 'ekans': 'poison',
                 'weedle': 'bug',
                 'diglett': 'ground',}

pokemon_base_health = {'bulbasaur' : 12,
                        'charmander': 12,
                        'squirtle': 12,
                        'pidgey': 10,
                        'ekans': 14,
                        'weedle': 8,
                        'diglett': 12,}

class Move:
    def __init__(self, name, power, type):
        self.name = name
        self.damage = power
        self.type = type

vine_whip=Move('vine whip', 3, 'grass')
tackle=Move('tackle', 4, 'normal')
flame_slash=Move('flame slash', 3, 'fire')
water_gun=Move('water gun', 3, 'water')
wing_slash=Move('wing slash', 3, 'flying')
poison_jab=Move('poison jab', 3, 'poison')
bug_bite=Move('bug bite', 3, 'bug')
mud_shot=Move('mud shot', 3, 'ground')
peck=Move('peck', 4, 'normal')







class Pokemon:
    def optimize_attack(self, defending_pokemon):
        highest_damage=0
        used_move=''
        for move in self.moves:
            if calculate_damage(move, defending_pokemon)>highest_damage:
                highest_damage=calculate_damage(move, defending_pokemon)
                used_move=move
        return(used_move)
    
    def new(self):
        player.pokemon.append(self)
        player.pokemon_level[self]=self.level
        for index, slot in enumerate(player.team):
            if slot=='':
                player.team[index]=self
                return()

    


    def select_move(self):
        print(f'what move will {self.name} use?')
        move_list=self.moves
        move_choices={}
        for index, move in enumerate(move_list):
            move_choices[index+1]=move.name
            print(index+1, move.name)  
            delay(.25)
        viable_choice=[]
        for key in move_choices.keys():
            viable_choice.append(key)
        choice=int(input().lower().strip())
        if choice in viable_choice:
            return(move_list[choice-1])
        else:
            print("That's not an option")
            self.select_move()

    def switch(self, cpu):
        pokemon_added=0
        available_pokemon=[]
        for slot in player.team:
            if slot != (self) and slot !='' and not(slot in player.fainted):
                pokemon_added+=1
                available_pokemon.append(slot)
        if len(available_pokemon)>0:
            print('which pokemon do you want to switch to?')
            if pokemon_added==1:
                print(1, available_pokemon[0].name)
                choice=input().strip()
                if int(choice)==1:
                    print(f'Come back {player.active_pokemon.name}')
                    player.active_pokemon=available_pokemon[0]
                    print(f'Go {player.active_pokemon.name}')
                    return()
                else:
                    print("That's not an option, please try again")
                    self.switch(self)
            if pokemon_added>1:
                counter=0
                print(available_pokemon)
                available_pokemon_names=[]
                for pokemon in available_pokemon:
                    available_pokemon_names.append(pokemon.name)
                for pokemon in available_pokemon_names:
                    counter+=1
                    print(counter, pokemon)
                choice=input().strip()
                if int(choice)<=counter:
                    print(f'Come back {player.active_pokemon.name}')
                    player.active_pokemon=available_pokemon[int(choice)-1]
                    print(f'Go {player.active_pokemon.name}')
                    return()
                else:
                    print("That's not an option, please try again")
                    self.switch(self)
            else:
                print('There are no pokemon to switch to, pick another option')
                return('no switches')
            
    def __init__(self, name, moves, type, base_hp):
        self.name=name
        self.type=pokemon_types[name]
        self.moves=moves
        self.base_hp=pokemon_base_health[name]
        self.temp_hp=self.base_hp
        self.base_catch=base_catch
        self.level=0
        self.hp_multiplier=1
    
bulbasaur=Pokemon('bulbasaur', [vine_whip, tackle], .5)
charmander=Pokemon('charmander', [flame_slash, tackle], .5)
squirtle=Pokemon('squirtle', [water_gun, tackle], .5)
pidgey=Pokemon('pidgey', [wing_slash, peck], .75)
weedle=Pokemon('weedle', [bug_bite, tackle], .9)
ekans=Pokemon('ekans', [poison_jab, tackle], .6)
diglett=Pokemon('diglett', [mud_shot, tackle], .4)






import time
type_pool=[
    "normal",
    "fire",
    "water",
    "electric",
    "grass",
    "ice",
    "fighting",
    "poison",
    "ground",
    "flying",
    "psychic",
    "bug",
    "rock",
    "ghost",
    "dragon",
    "dark",
    "steel",
    "fairy"
]
def build_matchups(super_effective, not_effective, base_type):
    name={}
    for type in type_pool: 
        if type in (super_effective):
            name[type]=2
        elif type in (not_effective):
            name[type]=.5
        else:
            name[type]=1
    return(name)
type_interactions={}

type_interactions['normal']=build_matchups(
    '', 
    'ghost', 
    'normal'
)

type_interactions['fire']=build_matchups(
    ['grass','ice', 'bug', 'steel'], 
    ['fire', 'water','rock', 'dragon' ],
    'fire'
)

type_interactions['water']=build_matchups(
    ['ground', 'fire', 'rock'], 
    ['water', 'grass', 'dragon'], 
    'water'
)

type_interactions['electric']=build_matchups(
    ['water', 'flying'], 
    ['electric', 'grass', 'ground', 'flying'], 
    'electric'
)

type_interactions['grass']=build_matchups(
    ['water', 'ground', 'rock'], 
    ['fire', 'grass', 'poison', 'flying', 'bug', 'dragon', 'steel'], 
    'grass'
)

type_interactions['ice']=build_matchups(
    ['grass', 'ground', 'flying', 'dragon'], 
    ['fire', 'water', 'ice', 'steel'], 
    'ice'
)

type_interactions['fighting']=build_matchups(
    ['normal', 'ice', 'dark', 'steel', 'rock'], 
    ['poison', 'flying', 'psychic', 'bug', 'fairy'], 
    'fighting'
)

type_interactions['poison']=build_matchups(
    ['grass', 'fairy'], 
    ['poison', 'ground', 'rock', 'ghost', 'steel'], 
    'poison'
)

type_interactions['ground']=build_matchups(
    ['fire', 'electric', 'poison', 'rock', 'steel'], 
    ['grass', 'flying', 'bug'], 
    'ground'
)

type_interactions['flying'] = build_matchups(
    ['grass', 'fighting', 'bug'],
    ['electric', 'rock', 'steel', 'ground'],
    'flying'
)

type_interactions['psychic'] = build_matchups(
    ['fighting', 'poison'],
    ['psychic', 'steel'],
    'psychic'
)

type_interactions['bug'] = build_matchups(
    ['grass', 'psychic', 'dark'],
    ['fire', 'fighting', 'poison', 'flying', 'ghost', 'steel', 'fairy'],
    'bug'
)

type_interactions['rock'] = build_matchups(
    ['fire', 'ice', 'flying', 'bug'],
    ['fighting', 'ground', 'steel'],
    'rock'
)

type_interactions['ghost'] = build_matchups(
    ['psychic', 'ghost'],
    ['dark', 'normal'],
    'ghost'
)

type_interactions['dragon'] = build_matchups(
    ['dragon'],
    ['steel'],
    'dragon'
)

type_interactions['dark'] = build_matchups(
    ['psychic', 'ghost'],
    ['fighting', 'dark', 'fairy'],
    'dark'
)

type_interactions['steel'] = build_matchups(
    ['ice', 'rock', 'fairy'],
    ['fire', 'water', 'electric', 'steel', 'poison'],
    'steel'
)

type_interactions['fairy'] = build_matchups(
    ['fighting', 'dragon', 'dark'],
    ['fire', 'poison', 'steel'],
    'fairy'
)











def catch():
    return()



def run():
    return()




import os





        







def delay(seconds):
    if player.name!='test':
        time.sleep(seconds)






def acquire_item(name, quanity):
    already_have=False
    for key in player.inventory.keys():
        if name==key:
            already_have=True
    if already_have==False:
        player.inventory[name]=quanity
    else:
        player.inventory[name]+=quanity



run_pokemon()