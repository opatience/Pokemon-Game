from utils import *
from data.items import * 
from rich import *
import math
import random
from data.interactions import *

class Battle:
    def __init__(self, game):
        self.game = game
        self.turn = 0

    # checks for speed
    def is_player_first(self, player, cpu, player_choice, cpu_move):
        if self.prio_logic(player_choice, cpu_move) == 'player_prio':
            return True
        elif self.prio_logic(player_choice, cpu_move) == 'cpu_prio':
            return False
 
        if player.active_pokemon.speed >= cpu.active_pokemon.speed:
            return True
        else:
            return False

    def prio_logic(self, player_choice, cpu_move):
        player_prio=0
        cpu_prio=0
        if isinstance(player_choice['attack'], Move) == True:
            ei=0
            for effect in player_choice['attack'].effect:
                if effect == 'priority':
                    player_prio=player_choice['attack'].magnitude[ei]
                ei+=1
        ei=0
        for effect in cpu_move.effect:
            if effect == 'priority':
                cpu_prio=cpu_move.magnitude[ei]
            ei+=1
        if cpu_prio<player_prio:
            return('player_prio')
        elif cpu_prio>player_prio:
            return ('cpu_prio')
        

    # checks if the cpu's pokemon has fainted
    def cpu_faint_check(self, cpu):
        if cpu.ahp <= 0:
            print(f'{cpu.aname} fainted!')
            win_check = cpu.cpu_faint()
            if win_check == True:
                self.player_win(self.player)
            else:
                return()

    # checks if your pokemon has fainted
    def faint_check(self, player):
        if player.ahp <= 0:
            print(f'{player.aname} fainted')
            lose_check = self.player.faint_logic()
            if lose_check == True:
                self.cpu_win(player)

    # resolves the CPU winning
    def cpu_win(self, player):
        print('You lose')
        delay(1)
        print(f'you lost {math.ceil(int((player.money * .1)))} pokedollars')
        delay(3)
        return()

    # levels up the team and ends the battle after a player win
    def player_win(self, player):
        delay(2)
        self.xp_logic(player)

    def xp_logic(self, player):
        xp_split = 0
        for pokemon in player.team:
            if pokemon != '':
                if pokemon.level < player.location.level_cap:
                    xp_split += 1

        for pokemon in player.team:
            if pokemon != '':
                if pokemon.level < player.location.level_cap:
                    prior_level = pokemon.level
                    pokemon.level += (1 / xp_split)

                    if prior_level != math.floor(pokemon.level):
                        delay(.5)
                        print(f'{pokemon.name} leveled up to level {int(pokemon.level)}')
                        delay(3)

                        if pokemon.level == pokemon.evolve_lv:
                            pokemon.evolve_pokemon()

                        if pokemon.level in pokemon.learnset.keys():
                            pokemon.new_move(pokemon.learnset[pokemon.level])
                    else:
                        print(f'{pokemon.name} gained {1/xp_split} of a level')
                        delay(3)
                else:
                    delay(.25)
                    print(f'{pokemon.name} is at the level cap of {player.location.level_cap}')
                    delay(.25)
                    print('Proceed to the next zone to level them again')
                    delay(3)


    def pokemon_fights(self, player, cpu):
        self.initialize_battle(player, cpu)
        while cpu.ahp > 0 and player.ahp > 0 and cpu.mon_caught == False and player.ran == False:
            self.menu.display_battle_info(player, cpu)
            self.execute_turn(player, cpu)
        return()

    def initialize_battle(self, player, cpu):
        self.turn = 0
        player.setup_battle(cpu)
        cpu.setup_battle(player)
        delay(1)
        print(f'{player.name}: Go {player.aname}!\n')
        delay(1)
        print(f'{cpu.name}: Go {cpu.aname}\n')
        delay(1)

    def increment_turn(self, player, cpu):
        self.turn += 1
        player.active_pokemon.active_turns += 1
        cpu.active_pokemon.active_turns += 1

    # main turn logic
    def execute_turn(self, player, cpu):
        player_choice = self.player_action_choice(player)
        cpu_move = self.cpu_action_choice(cpu)
        player_first = self.is_player_first(player, cpu, player_choice, cpu_move)

        if player_first == True:

            if self.status_delay(player) == False:
                self.run_choice(player, player_choice)
                self.cpu_faint_check(cpu)

            if self.proceed_check(player, cpu) == True:

                if self.status_delay(cpu) == False:
                    cpu.cpu_attack(player, cpu_move)
                    self.faint_check(player)

                self.cleanup_turn(player, cpu)

        # mirrored logic
        else:
            if self.status_delay(cpu) == False and player.ran == False:
                cpu.cpu_attack(player, cpu_move)
                self.faint_check(player)

            if self.proceed_check(player, cpu) == True:

                if self.status_delay(player) == False:
                    self.run_choice(player, player_choice)
                    self.cpu_faint_check(cpu)

                self.cleanup_turn(player, cpu)

    def player_action_choice(self, player):
        choice = {'attack': None, 'switch': None, 'catch': None}
        action_choice = self.menu.battle_menu(player, player.opponent)

        if action_choice == self.action.run:
            action_choice(player)

        if action_choice == self.action.attack:
            move_choice = self.menu.select_move()
            choice['attack'] = move_choice

        if action_choice == self.action.switch:
            switch_choice = self.menu.switch_menu(player)
            choice['switch'] = switch_choice

        if action_choice == self.action.catch:
            choice['catch'] = self.action.catch

        return choice

    def run_choice(self, player, choice):
        for key in choice.keys():
            if choice[key] != None:
                if key == 'switch':
                    return self.action.switch(player, choice['switch'])
                if key == 'attack':
                    return self.action.attack(player, choice['attack'])
                if key == 'catch':
                    return self.action.catch(player)

    def cpu_action_choice(self, cpu):
        move_choice = self.optimize_cpu_attack(cpu)
        return move_choice

    def cleanup_turn(self, player, cpu):
        self.increment_turn(player, cpu)
        self.resolve_status(player)
        self.resolve_status(cpu)

    # continue battle check
    def proceed_check(self, player, cpu):
        if cpu.ahp > 0 and player.ahp > 0 and cpu.mon_caught == False and player.ran == False:
            return True

    def status_delay(self, player):
        mon = player.active_pokemon

        if mon.status == 'asleep':
            wakeup_check = random.random()
            if mon.afflicted_turns == 4:
                mon.status = None
                print(f'{mon.name} woke up')
                return False
            elif wakeup_check <= .33 and mon.afflicted_turns > 1:
                mon.status = None
                print(f'{mon.name} woke up')
                return False
            else:
                print(f'{mon.name} sleeps through the turn')
                return True

        if mon.status == 'paralyzed':
            paralyze_check = random.random()
            if paralyze_check <= .25:
                print(f'{mon.name} is paralyzed')
                return True
            else:
                return False

        if mon.status == 'confused':
            confusion_check = random.random()
            confusion_end_check = random.random()
            if mon.afflicted_turns == 4:
                print(f'{mon.name} snaps out of their confusion')
                mon.status = None
                return False
            elif mon.afflicted_turns>1 and confusion_end_check<=.25:
                print(f'{mon.name} snaps out of their confusion')
                mon.status = None
                return False
            elif confusion_check <= .33:
                print(f'{mon.name} hit themselves in confusion')
                display_damage(mon, ((1/16) * mon.hp))
                return True

        if mon.flinched == True:
            print(f'{mon.name} flinched')
            mon.flinched = False
            return True

        return False

    def resolve_status(self, player):
        mon = player.active_pokemon

        if mon.status != None:
            mon.afflicted_turns += 1
    
            if mon.status == 'burn':
                player.active_pokemon.temp_hp -= ((1/16) * mon.hp)
                print(f'{mon.name} burned')
                delay(2)
                print(f'{mon.name} has {round(((mon.temp_hp/mon.hp)*100))}% hp remaining')
                delay(2)

            if mon.status == 'poisoned':
                player.active_pokemon.temp_hp -= ((1/16) * mon.hp)
                print(f'Poison hurts {mon.name}')
                delay(2)
                print(f'{mon.name} has {round(((mon.temp_hp/mon.hp)*100))}% hp remaining')

        if mon.fire_spin == True:
            player.active_pokemon.temp_hp -= ((1/16) * mon.hp)
            print(f'{mon.name} is harmed by the inferno surrounding them')
            delay(2)
            print(f'{mon.name} has {round(((mon.temp_hp/mon.hp)*100))}% hp remaining')
        

        #MAKE THIS INTO VARS
        if mon.leech_seed_draining == True:
            leech_seed_drain = ((1/8) * mon.hp)
            mon.temp_hp -= leech_seed_drain
            print(f"Plants drain {mon.name}'s health")
            delay(2)
            print(f'{mon.name} has {round(
                                        ((mon.temp_hp/mon.hp)
                                         *100))}% hp remaining\n')
            delay(2)

            if round(((player.opponent.active_pokemon.temp_hp+leech_seed_drain)/player.opponent.active_pokemon.hp)*100)<100:
                print(f"{player.opponent.aname} is healed by leech seed")
                delay(2)
                print(f"{player.opponent.aname} gained {round( 
                                                        (((player.opponent.active_pokemon.temp_hp+leech_seed_drain)/player.opponent.active_pokemon.hp)
                                                         -(player.opponent.active_pokemon.temp_hp/player.opponent.active_pokemon.hp))
                                                        *100)}% hp")
                delay(2)
                player.opponent.active_pokemon.temp_hp+=leech_seed_drain

            else:
               print(f"{player.opponent.aname} is healed by leech seed")
               delay(2)
               print(f'{player.opponent.aname} is at 100% hp') 
               delay(2)
               player.opponent.active_pokemon.temp_hp = player.opponent.active_pokemon.hp
        else:
            mon.afflicted_turns = 0


    def optimize_cpu_attack(self, cpu):
        highest_damage = 0
        used_move = ''

        for move in cpu.active_pokemon.moveset:
            if self.calculate_damage(move, self.player.active_pokemon, cpu.active_pokemon, False) >= highest_damage:
                highest_damage = self.calculate_damage(move, self.player.active_pokemon, cpu.active_pokemon, False)
                used_move = move
        return(used_move)

    def calculate_damage(self, move, defending_pokemon, attacking_mon, damage_calc=True):
        protect_mult = 1
        stab_mult = 1
        type_int_mult = 1
        crit_mult = 1
        burn_mult = 1

        crit_check = random.random()

        if defending_pokemon.protected == True:
            print(f'{defending_pokemon.name} is protected from damage this turn')
            delay(2)
            defending_pokemon.protected = False
            protect_mult = 0
        

        if damage_calc == True:
            if self.game.logic.charge_check(attacking_mon, move) == True:
                return 0

        if damage_calc == True and attacking_mon.charging == False:
            if move.effect == 'high_crit':
                if crit_check > .8:
                    delay(2)
                    print("It's a critical hit!")
                    crit_mult = 1.5
            else:
                if crit_check > .9:
                    delay(2)
                    print("It's a critical hit!")
                    crit_mult = 1.5

        
        if isinstance(attacking_mon.type, str) == True:
            if attacking_mon.type == move.type:
                stab_mult = 1.5
        else:
            for type in attacking_mon.type:
                if type == move.type:
                    stab_mult = 1.5

        if isinstance(defending_pokemon.type, str) == True:
            type_int_mult = (type_int_mult * type_interactions[move.type][defending_pokemon.type])
        else:
            for type in defending_pokemon.type:
                type_int_mult = (type_int_mult * type_interactions[move.type][type])

        if attacking_mon.status == 'burn':
            burn_mult = .5

        if move.category == 'physical':
            return ((((((2 * attacking_mon.level * crit_mult) / 5) + 2)
                     * move.damage * (attacking_mon.atk / defending_pokemon.defense)) / 50 + 2)
                    * stab_mult * burn_mult * type_int_mult * random.uniform(.85, 1) * protect_mult)

        elif move.category == 'special':
            return ((((((2 * attacking_mon.level * crit_mult) / 5) + 2)
                     * move.damage * (attacking_mon.spatk / defending_pokemon.spdef)) / 50 + 2)
                    * stab_mult * type_int_mult * random.uniform(.85, 1) * protect_mult)

        elif move.category == 'status':
            return 0

    # shortcuts
    @property
    def player(self):
        return self.game.player

    @property
    def menu(self):
        return self.game.menu

    @property
    def action(self):
        return self.game.actions