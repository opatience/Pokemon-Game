import random
from utils import *
from data.interactions import *
from data.items import *
import math
from data.items import *
from rich import *

class Actions:
    
    def __init__(self, game):
        self.game = game

    #makes a list of spawn odd ranges and then picks one
    def explore(self,):
        spawns=self.player.location.spawns
        spawn_range=[]
        spawn_outcome=[]
        for key in spawns.keys():
            spawn_outcome.append(key)
            spawn_range.append(spawns[key])
        if len(spawns)>0:
           print('You search the area')
           delay(3)
           roll=random.random()
           if roll<=spawn_range[0]:
               self.player.wild_encounter(spawn_outcome[0])
           elif roll>spawn_range[0] and roll<=sum(spawn_range[0:2]):
               self.player.wild_encounter(spawn_outcome[1])
           elif roll>sum(spawn_range[0:2]) and roll<=sum(spawn_range[0:3]):
               self.player.wild_encounter(spawn_outcome[2])
           elif roll>sum(spawn_range[0:3]) and roll<=sum(spawn_range[0:4]):
               self.player.wild_encounter(spawn_outcome[3])
           elif roll>sum(spawn_range[0:4]) and roll<=sum(spawn_range[0:5]):
               self.player.wild_encounter(spawn_outcome[4])
           elif roll>sum(spawn_range[0:5]) and roll<=sum(spawn_range[0:6]):
               self.player.wild_encounter(spawn_outcome[5])
           elif roll>sum(spawn_range[0:6]) and roll<=sum(spawn_range[0:7]):
               self.player.wild_encounter(spawn_outcome[6])
        else:
            print('You find nothing here')
            
    #sends you to the next part of the code, ending the area
    def proceed(self):
        self.player.proceed=True
        return()
    
    def switch(self, player, new_mon):
        print(f'Come back {player.aname}')
        self.game.logic.switch_reset(player.active_pokemon)
        player.active_pokemon=new_mon
        print(f'Go {player.active_pokemon.name}')
        return()


    def run(self, player):
        delay(1)
        print('You fled the battle')
        player.ran=True
        return()
    

    def attack(self, player, move_choice):
        cpu_mon=player.opponent.active_pokemon
        accuracy_check=random.random()
        if accuracy_check>=move_choice.accuracy:
            print(f'{player.aname} missed\n')
            delay(2)
            return()
        print(f'\n{player.aname} used {move_choice.name}')
        damage=(self.battle.calculate_damage(move_choice, player.opponent.active_pokemon, player.active_pokemon))
        delay(1)
        if damage>0:
            self.game.logic.effectiveness_check(cpu_mon, move_choice)
            print(f'{player.aname} did {math.ceil(damage)} damage')
            cpu_mon.temp_hp-=damage
        delay(2)
        if cpu_mon.temp_hp>0 and damage>0:
            print(f'The Enemy {cpu_mon.name} has {round((cpu_mon.temp_hp/cpu_mon.hp)*100)}% hp remaining\n')
            delay(2)
        elif cpu_mon.temp_hp<=0:
            print(f'The Enemy {cpu_mon.name} has 0% hp remaining\n')
            delay(2)
        if move_choice.effect != 'none':
            self.game.logic.move_effect(move_choice, player.active_pokemon, cpu_mon)
        


    def catch(self, player):
            target_mon=player.opponent.active_pokemon
            print('You throw a pokeball\n')
            delay(1)
            player.inventory[pokeball]-=1
            print(f'You have {player.inventory[pokeball]} pokeballs remaining')
            delay(1)
            catch_rate=(((
                (3 * target_mon.hp)
                -(2 * target_mon.temp_hp))
                /(3 * target_mon.hp))
                *target_mon.species.base_catch
                *pokeball.bonus
            )

            shake_odds=(
                1048560
                /(math.sqrt(
                math.sqrt(
                (16711680/catch_rate)
                ))))
            
            catch_check=self.game.logic.shake_logic(shake_odds)
            if catch_check=='caught':
                self.player.new_pokemon(target_mon.species, target_mon.level, target_mon.shiny)
                print(f'You caught {target_mon.name}!')
                delay(4)
                new_screen()
                player.opponent.mon_caught=True
            elif catch_check=='fail': 
                print(f'{target_mon.name} breaks free')
                delay(3)

    

    def adjust_team_order(self):
        print("Which Pokemon do you want to move?")
        counter=0
        for slot in self.player.team:
            counter+=1
            if slot != '':
                print(f"{counter} {slot.name} lv{slot.level}")
                delay(.25)
        counter+=1
        mon_choice=input().strip()
        if input_check(mon_choice, counter)==True:
            print(f"Which slot do you want to move {self.player.team[(int(mon_choice)-1)].name} to?")
            counter2=0
            for slot in self.player.team:
                counter2+=1
                if slot !=self.player.team[(int(mon_choice)-1)] and slot !='':
                    print(f"{counter2} {slot.name} lv{slot.level}")
                    delay(.25)
            counter2+=1
            mon_swap_choice=input().strip()
            if input_check(mon_swap_choice, counter2)==True:
                mon_swapping1=self.player.team[(int(mon_choice)-1)]
                mon_swapping2=self.player.team[(int(mon_swap_choice)-1)]
                self.player.team[(int(mon_choice)-1)]=mon_swapping2
                self.player.team[(int(mon_swap_choice)-1)]=mon_swapping1
                print(f"You switched the position of {mon_swapping1.name} and {mon_swapping2.name}")

    def inspect_pokemon(self):
        print("Which Pokemon do you want to inspect")
        counter=1
        for pokemon in self.player.team:
            if pokemon != '':
                print(f'{counter} {pokemon.name} lv{pokemon.level}')
                counter+=1
        print(f'{counter} Return')
        choice=input().strip()
        if input_check(choice, counter)==True:
            self.edit_pokemon(self.player.team[int(choice)-1])
        if input_check(choice, counter)=='return':
            self.menu.adjust_menu()
        else:
            self.inspect_pokemon()

    def edit_pokemon(self, pokemon):
        print(f'You selected {pokemon.name} lv{pokemon.level}')
        delay(1)
        print(f'HP: {pokemon.hp}')
        delay(1)
        print(f'Speed: {pokemon.speed}')
        delay(1)
        if pokemon.item_type != 'none':
            print(f'Item: {pokemon.item.name}')
            delay(1)
        else:
            print('Item: None')
            delay(1)
        print('Moves')
        delay(1)
        move_cntr=1
        for move in pokemon.moveset:
            print(f' {move_cntr} {move.name} | dmg {move.damage}')
            delay(.25)
            move_cntr+=1
        print('What do you want to do?')
        delay(1)
        print('1. Change item')
        delay(.5)
        print('2. Return')
        choice=input().strip()
        if input_check(choice, 3)==True:
            choice=int(choice)
            if choice==1:
                self.change_item(pokemon)
            if choice==2:
                return()

    def change_item(self, pokemon):
        if pokemon.item_type != 'none':
            print(f'{pokemon.name} has {pokemon.item.name} equipped')
        else:
            print(f'{pokemon.name} has no item')
        delay(2)
        item_cntr=1
        item_list=['']
        if available_item(self.player)==True:
            print(f'Which item will you give {pokemon.name}')
            for item in self.player.inventory:
                if type(item)==ModifierItems:
                    if self.player.inventory[item]>0:
                        item_list.append(item)
                        print(f'{item_cntr} {item.name}')
                        item_cntr+=1
                        delay(.25)
            print(f'{item_cntr} Cancel')
            choice=input().strip()
            if input_check(choice, item_cntr)==True:
                if pokemon.item_type != 'none':
                    self.player.inventory[pokemon.item]+=1
                pokemon.item=item_list[int(choice)]
                self.player.inventory[item_list[int(choice)]]-=1
                delay(2)
                print(f"You have given {pokemon.name} {item_list[int(choice)].name}")
                delay(4)
                return()  
            elif input_check(choice, item_cntr)=='return':
                self.edit_pokemon(pokemon)
            else:
                delay(2)
                return(self.change_item(pokemon))
        else:
            delay(2)
            print('You have no items available to equip')
            return()
            
            

    
    def adjust_team_pokemon(self):
        for slot in self.player.team:
            if slot=='':
                print('You have no pokemon to add to your team')
                return()
        print('What Pokemon do you want to add to your team?')
        pokemon_index=1
        box_pokemon=['']
        for pokemon in self.player.pokemon:
            if not (pokemon in self.player.team):
                box_pokemon.append(pokemon)
                print(f'{pokemon_index}.  {pokemon.name} lv.{pokemon.level}')
                delay(.25)
                pokemon_index+=1
        add_choice=input().strip()
        if add_choice.isdigit() and int(add_choice) in range(0, pokemon_index):
            delay(2)
            print(f'What pokemon do you want to swap for {box_pokemon[int(add_choice)].name}?')
            team_index=1
            for pokemon in self.player.team:
                print(f'{team_index}.  {pokemon.name} lv.{pokemon.level}')
                delay(.25)
                team_index+=1
        else:
            print("That's not an option, pick again")
            return(self.adjust_team_pokemon())
        remove_choice=input().strip()
        if remove_choice.isdigit() and int(add_choice) in range(0, team_index):
            self.player.team[int(remove_choice)]=box_pokemon[add_choice]
            delay(2)
            print(f'You removed {self.player.team[remove_choice].name} and added {box_pokemon[add_choice].name}')
            delay(2)
        else:
            print("That's not an option, pick again")
            return(self.adjust_team_pokemon())
        
    
 
#Shortcuts to make accessing stuff easier, exist in most modules
    @property
    def player(self):
       return(self.game.player)
   
    @property
    def menu(self):
       return(self.game.menu)
    
    @property
    def battle(self):
       return(self.game.battle)




    
