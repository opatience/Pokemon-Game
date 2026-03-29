from utils import *
from data.items import * 
from rich import *
from data.status import *

class Menu:
    def __init__(self, game):
        self.game = game

    # States that you have entered an area, reads a description, and then shows the spawn
    def new_area(self, area):
        self.player.location = area
        new_screen()
        print(f'\nYou have entered {area.name}\n\n')
        delay(1)
        print(f'{area.description}\n\n')
        delay(1)
        print(f'The level cap for the area is {area.level_cap}\n')
        delay(1)
        print(f'These are the potential spawns')
        delay(1)
        for spawn in area.spawns.keys():
            print(f'{spawn.name}')
            delay(.25)
        print('\n')

    # prints a list of the options and then calls one of them
    def display_options(self):
        delay(2)
        options_text = ['Proceed', 'Explore', 'Adjust Pokemon', "Shop"]
        options = [self.actions.proceed, self.actions.explore, self.adjust_menu, self.display_shop]
        while self.player.proceed == False:
            new_screen()
            print('What do you want to do?')
            delay(2)
            choice_list(options, options_text, '', True)
        self.player.proceed = False
        return()

    # establishes player choices for combat:
    def battle_menu(self, player, cpu):
        switch = False
        print(f'What will you do?')
        for slot in player.team:
            if slot != player.active_pokemon and not (slot == '') and not (slot in player.fainted):
                switch = True
        if self.game.logic.trapped_check(player) == True:
            switch = False

        options_string = ['Attack']
        options = [self.actions.attack]

        if switch == True:
            options_string.append('Switch')
            options.append(self.actions.switch)

        if cpu.wild == True:
            if player.inventory[pokeball] > 0:
                options_string += ['Catch', 'Run']
                options += [self.actions.catch, self.actions.run]
            else:
                options_string += ['Run']
                options += [self.actions.run]

        choices_library = {}
        len_choices = 1
        for function in options:
            print(f'{len_choices} {options_string[len_choices-1]}')
            choices_library[len_choices] = function
            len_choices += 1
            delay(.25)

        choice = input().strip()
        if input_check(choice, len_choices) == True:
            choice = int(choice)
            return choices_library[choice]

        # code that runs if check fails
        print("That's not an option, pick again")
        return self.battle_menu(player, cpu)

    def select_move(self):
        print(f'\n\n\nWhat move will {self.player.aname} use?')
        move_list = self.player.active_pokemon.moveset

        # will bug with 2 charge moves but im not hardcoding around that
        if self.player.active_pokemon.charging == True:
            print(self.player.active_pokemon.charging)
            for move in self.player.active_pokemon.moveset:
                if 'charge' in move.effect:
                    move_list = [move]

        counter = 1
        for move in move_list:
            print(counter, move.name)
            counter += 1
            delay(.25)

        choice = input().strip()
        if choice.isdigit() and int(choice) in range(0, counter):
            return move_list[int(choice) - 1]
        else:
            print("That's not an option")
            self.select_move()

    def display_shop(self):
        delay(2)
        print(f'You have ${self.player.money}')
        delay(2)
        print('What type of item do you want to buy')

        item_categories = [
            self.pokeball_shop,
            self.attack_items_shop,
            self.hp_items_shop,
            self.speed_items_shop
        ]
        item_categories_text = ['Pokeballs', 'Attack Items', 'HP Items', 'Speed Items']

        return choice_list(item_categories, item_categories_text, '', False)

    def pokeball_shop(self):
        print('What kind of Pokeball do you want to buy?')
        pokeball_costs = {pokeball: 50}
        pokeball_options = [pokeball]

        ball_cntr = 1
        for ball in pokeball_options:
            print(f'{ball_cntr} {ball.name}  ${pokeball_costs[ball]}')
            ball_cntr += 1
            delay(.25)

        pball_choice = input().strip()
        if pball_choice.isdigit() and int(pball_choice) in range(0, ball_cntr):
            qnty_choice = input('How many do you want to buy').strip()
            if qnty_choice.isdigit() and (
                int(qnty_choice) * pokeball_costs[pokeball_options[int(pball_choice) - 1]]
            ) <= self.player.money:

                self.player.money -= (
                    int(qnty_choice) * pokeball_costs[pokeball_options[int(pball_choice) - 1]]
                )
                delay(1)
                print(f'You bought {qnty_choice} {pokeball_options[int(pball_choice) - 1].name}')
                delay(4)
                self.player.acquire_item(
                    pokeball_options[int(pball_choice) - 1],
                    int(qnty_choice)
                )
                return()
            else:
                print("You don't have enough money for that many pokeballs")
                print(f"You have ${self.player.money}")
                delay(4)
                return()
        else:
            pass

    def attack_items_shop(self):
        print('Which attack item do you want to buy?')
        available_items = ['']
        counter = 1

        for item in item_list:
            if item.type == 'attack':
                available_items.append(item)
                print(f"{counter} {item.name} ${item.cost}  | damage +{item.strength}")
                delay(.25)
                counter += 1

        print(f'{counter} Return')
        choice = input().strip()

        if input_check(choice, counter) == True:
            if available_items[int(choice)].cost <= self.player.money:
                self.player.money -= available_items[int(choice)].cost
                self.player.acquire_item(available_items[int(choice)], 1)
                print(f"You bought {available_items[int(choice)].name} for ${available_items[int(choice)].cost}")
                delay(4)
            else:
                print("You don't have enough money for that")
                delay(4)
                return()
        elif input_check(choice, counter) == 'return':
            self.display_shop()
        else:
            print("That's not an option, pick again")
            return self.attack_items_shop()

    def hp_items_shop(self):
        print('Which HP item do you want to buy?')
        available_items = ['']
        counter = 1

        for item in item_list:
            if item.type == 'hp':
                available_items.append(item)
                print(f"{counter} {item.name} ${item.cost}  | hp +{item.strength}")
                delay(.25)
                counter += 1

        print(f'{counter} Return')
        choice = input().strip()

        if input_check(choice, counter) == True:
            if available_items[int(choice)].cost <= self.player.money:
                self.player.money -= available_items[int(choice)].cost
                self.player.acquire_item(available_items[int(choice)], 1)
                print(f"You bought {available_items[int(choice)].name} for ${available_items[int(choice)].cost}")
                delay(4)
            else:
                print("You don't have enough money for that")
                delay(4)
                return self.hp_items_shop()
        elif input_check(choice, counter) == 'return':
            self.display_shop()
        else:
            return self.hp_items_shop()

    def speed_items_shop(self):
        print('Which speed item do you want to buy?')
        available_items = ['']
        counter = 1

        for item in item_list:
            if item.type == 'speed':
                available_items.append(item)
                print(f"{counter} {item.name} ${item.cost}  | speed +{item.strength}")
                delay(.25)
                counter += 1

        print(f'{counter} Return')
        choice = input().strip()

        if input_check(choice, counter) == True:
            if available_items[int(choice)].cost <= self.player.money:
                self.player.money -= available_items[int(choice)].cost
                self.player.acquire_item(available_items[int(choice)], 1)
                print(f"You bought {available_items[int(choice)].name} for ${available_items[int(choice)].cost}")
                delay(4)
            else:
                print("You don't have enough money for that")
                delay(4)
                return()
        elif input_check(choice, counter) == 'return':
            return()
        else:
            return self.speed_items_shop()

    def adjust_menu(self):
        print("What do you want to do?")
        options = [
            self.actions.adjust_team_pokemon,
            self.actions.adjust_team_order,
            self.actions.inspect_pokemon
        ]
        options_string = [
            'Change Team Pokemon',
            'Adjust Team Order',
            'Inspect Pokemon'
        ]
        return choice_list(options, options_string, '', False)

    def switch_menu(self, player):
        pokemon_added = 0
        available_pokemon = []

        for slot in player.team:
            if slot != player.active_pokemon and slot != '' and not (slot in player.fainted):
                pokemon_added += 1
                available_pokemon.append(slot)

        if len(available_pokemon) > 0:
            print('\n\n\nWhich pokemon do you want to switch to?')
            if pokemon_added == 1:
                print(1, available_pokemon[0].name)
                choice = input().strip()

                if int(choice) == 1:
                    return(available_pokemon[0])
                else:
                    print("That's not an option, please try again")
                    return(self.switch_menu(player))
        if pokemon_added>1:
               counter=0
               available_pokemon_names=[]
               for pokemon in available_pokemon:
                   available_pokemon_names.append(pokemon.name)
               for pokemon in available_pokemon_names:
                   counter+=1
                   print(counter, pokemon)
               choice=input().strip()
               if int(choice)<=counter:
                   return(available_pokemon[int(choice)-1])
               else:
                   print("That's not an option, please try again")
                   return(self.switch_menu(player))
               


    def display_battle_info(self, player, cpu):
        new_screen()
        print(f'\nTurn: {self.battle.turn}')
        delay(2)
        print(f'{player.aname}: Lv{round(player.active_pokemon.level)}')
        delay(.5)
        print(f'Type: {'/'.join(player.active_pokemon.type)}')
        delay(.5)
        show_status(player.active_pokemon.status)
        delay(.5)
        print(f'HP: {round(((player.active_pokemon.temp_hp/player.active_pokemon.hp)*100))}%')
        delay(2)
        print("\nVS\n")
        delay(.5)
        print(f'{cpu.aname}: Lv{round(cpu.active_pokemon.level)}')
        delay(.5)
        print(f'Type: {'/'.join(cpu.active_pokemon.type)}')
        delay(.5)
        show_status(cpu.active_pokemon.status)
        delay(.5)
        print(f'HP: {round(((cpu.active_pokemon.temp_hp/cpu.active_pokemon.hp)*100))}%\n\n')
        delay(2)
    
    # Shortcuts to make accessing stuff easier
    @property
    def player(self):
        return self.game.player

    @property
    def actions(self):
        return self.game.actions

    @property
    def battle(self):
        return self.game.battle