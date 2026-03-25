from core.menu import Menu
from core.player import Player
from core.player_pokemon import PlayerPokemon
from data.moves import *
from core.actions import Actions
from data.interactions import *
from core.battle import Battle
from data.pokemon import *
from data.locations import *
from core.game import *
from data.items import *
from utils import *
from rich import *
from colorama import *

#delay_on()
#game.player.money=5000
#game.player.team[0].shiny=True
#game.player.acquire_item(knife, 5)
#game.player.acquire_item(pokeball, 5)
#game.menu.new_area(test_area)
#game.menu.display_options()

rival=Player(game)

def run_pokemon():  
    delay_on()  
    new_screen()
    game.player.name=choose_name()
    print(f"Good choice {game.player.name}")
    delay(2)
    starter_interaction()
    delay(2)
    rival_interaction(rival)
    delay(3)
    game.menu.new_area(route_101)
    game.menu.display_options()


def choose_name():
    print('\nWhat do you want your name to be?')
    return(input())

def starter_interaction():
    game.player.location=pokemon_lab
    print('\nChoose Your Starter')
    print('1. Bulbasaur')
    print('2. Charmander')
    print('3. Squirtle')
    game.player.starter=starter_choice()
    game.player.new_pokemon(game.player.starter, 5)
    print(f'\nYou chose {game.player.starter.name}\n')
    delay(2)
    return()

def starter_choice():
    choice=input().strip()
    if input_check(choice, 4)==True:
        starterlist=['', bulbasaur, charmander, squirtle]
        return(starterlist[int(choice)])
    else:
        print("That's not an option")
        print('Pick Again')
        starter_interaction()

def rival_interaction(rival):
    new_screen()
    rival.name=('Gary')
    print('\nSomeone else enters the building\n')
    delay(2)
    print(f'This is your rival Gary, he hates you\n')
    delay(2)
    print(f'Gary: I hate you {game.player.name}\n')
    delay(2)
    print(f"Gary: Let's Pokemon battle!\n")
    delay(2)
    rival.starter=determine_rival_starter()
    rival.new_pokemon(rival.starter, 5)
    game.battle.pokemon_fights(game.player, rival)
    print("\n\nGary: You've beaten me, take some pokeballs and cash as a prize")
    delay(2)
    print('\n\nYou get 5 pokeballs and $1000')
    delay(2)
    print('You leave the lab and head out onto the road')
    delay(4)
    game.player.money+=1000
    game.player.acquire_item(pokeball, 5)

def determine_rival_starter():
    if game.player.starter==bulbasaur:
        return(squirtle)
    elif game.player.starter==squirtle:
        return(charmander)
    elif game.player.starter==charmander:
        return(bulbasaur)
    else:
        print('There was an error in the code')
    
def testing_environment():
    #delay_on()
    game.player.new_pokemon(bulbasaur, 100)
    game.player.team[0].base_hp=100000
    game.player.team[0].moveset[0]=leech_seed
    game.player.team[0].moveset[1] = protect
    game.player.team[0].moveset[2]=poison_powder
    game.player.team[0].moveset[3]=scary_face
    game.player.inventory[pokeball]=3000000
    test_cpu=Player(game)
    test_cpu.wild=True
    test_cpu.new_pokemon(squirtle, 100)
    test_cpu.team[0].moveset[0]=ice_shard
    test_cpu.team[0].base_hp=100000
    game.battle.pokemon_fights(game.player, test_cpu)

testing_environment()
#run_pokemon()