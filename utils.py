import os
import time
test=True
from data.items import ModifierItems
from colorama import *
from data.pokemon import *


def new_screen():
    _ = os.system('clear')

def delay(seconds):
    global test
    if test==False:
        time.sleep(seconds)

def delay_on():
    global test
    test=False

def choice_list(choice_funcs, choice_text, pass_variable, first_layer):
    choices_library={}
    len_choices=1
    for function in choice_funcs:
        print(f'{len_choices} {choice_text[len_choices-1]}')
        choices_library[len_choices]=function
        len_choices+=1
        delay(.25)
    if first_layer==False:
        print(f'{len_choices} Return')
    choice=input().strip()
    if input_check(choice, len_choices)==True:
        choice=(int(choice))
        if pass_variable != '':
             return(choices_library[choice](pass_variable))
        else:
            return(choices_library[choice]())
        
    elif input_check(choice, len_choices)=='return':
        return()
    #code that runs if check fails
    print("That's not an option, pick again")
    return(choice_list(choice_funcs, choice_text, pass_variable))

def input_check(choice, options):
    if choice.isdigit() and int(choice) in range(0, options):
        return(True)
    elif choice.isdigit() and int(choice)==(options):
        return('return')
    else:
        print("That's not an option, pick again")
        return(False)
    
def available_item(player):
    for item in player.inventory:
        if type(item)==ModifierItems:
            return(True)
    return(False)

def display_shiny(mon, color):
    if color=='red':
        return(Fore.RED+mon.name+default)
    if color=='blue':
        return(Fore.BLUE+mon.name+default)
    
def display_damage(mon, dmg):
    delay(2)
    mon.temp_hp-=dmg
    print(f'{mon.name} has {round(((mon.temp_hp/mon.hp)*100))}% hp remaining')
    delay(2)

default=Fore.WHITE
