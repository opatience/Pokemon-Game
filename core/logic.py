import random
from utils import *
from data.interactions import *

class Logic:
    def __init__(self, game):
        self.game=game

    def shake_logic(self, shake_success_odds,):
        for i in range(4):
            shake_roll=random.randint(1, 65535)
            if shake_roll>=shake_success_odds:
                return('fail')
            elif shake_roll<shake_success_odds:
                if i != 3:
                    print('Shake\n')
                    delay(1.5)
                else:
                    print('Ding!\n')
                    delay(1.5)
        return('caught')

    def move_effect(self, move, mon_using, mon_attacked):
        self_stat_rng=random.random()
        if type(move.effect)==str:
            move.effect=[move.effect]
            move.effect_chance=[move.effect_chance]
            move.effect_magnitude=[move.effect_magnitude]
        
        ei=0 #effect index i js dont wanna type that shit

        for effect in move.effect:
            chance=move.effect_chance[ei]
            magnitude=move.effect_magnitude[ei]

            if mon_attacked.status == None:

                if effect == 'poison':
                    if random.random()<=move.effect_chance[ei]:
                        print(f'{mon_attacked.name} is poisoned')
                        delay(2)
                        mon_attacked.status='poisoned'
                    
            

                if effect == 'sleep':
                    if random.random()<=move.effect_chance[ei]:
                        print(f'{mon_attacked.name} falls asleep')
                        delay(2)
                        mon_attacked.status='asleep'
                    
            

                if effect == 'burn':
                    if random.random()<=move.effect_chance[ei]:
                        print(f'{mon_attacked.name} is burnt')
                        delay(2)
                        mon_attacked.status='burn'
                    


                if effect == 'paralyze':
                    if random.random()<=move.effect_chance[ei]:
                        print(f'{mon_attacked.name} is paralyzed')
                        delay(2)
                        mon_attacked.status='paralyzed'

                if effect == 'confuse':
                    if random.random()<=move.effect_chance[ei]:
                        print(f'{mon_attacked.name} is confused')
                        delay(2)
                        mon_attacked.status='confused'

            
            if effect == 'flinch':
                if random.random()<=move.effect_chance[ei]:
                    if move.name != 'Fake Out':
                        mon_attacked.flinched=True
                    elif move.name == 'Fake Out':
                        if mon_using.active_turns<1:
                            mon_attacked.flinched=True
                    


            if effect == 'trap':
                mon_attacked.trapped=True
        


            if effect == 'fire_spin':
                mon_attacked.fire_spin=True



            if effect == 'recoil':
                dmg=(self.game.battle.calculate_damage(move, mon_attacked, mon_using, False)*move.effect_magnitude[ei])
                mon_using.temp_hp-=dmg
                print(f'{mon_using.name} took {round(dmg)} dmg of recoil')
                delay(2)
                print(f'{mon_using.name} has {round(((mon_using.temp_hp/mon_using.hp)*100))}% hp remaining')
            


            if effect == 'self_attack':
                atk_stage=mon_using.attack_stage
                if self_stat_rng<=move.effect_chance[ei]:
                    prior_stage=atk_stage
                    mon_using.attack_stage=self.stage_change(atk_stage, move.magnitude[ei])
                    if prior_stage<mon_using.attack_stage:
                        print(f"{mon_using.name}'s attack increased")
                    elif prior_stage==mon_using.attack_stage:
                        if prior_stage>0:
                            print(f"{mon_using.name}'s attack cannot increase more")
                        else:
                            print(f"{mon_using.name}'s attack cannot decrease more")
                    else:
                        print(f"{mon_using.name}'s attack decreased")



            if effect == 'self_spatk':
                sp_stage=mon_using.spatk_stage
                if self_stat_rng<=move.effect_chance[ei]:
                    prior_stage=sp_stage
                    mon_using.spatk_stage=self.stage_change(sp_stage, move.magnitude[ei])
                    if prior_stage<mon_using.spatk_stage:
                        print(f"{mon_using.name}'s special attack increased")
                    elif prior_stage==mon_using.spatk_stage:
                        if prior_stage>0:
                            print(f"{mon_using.name}'s special attack cannot increase more")
                        else:
                            print(f"{mon_using.name}'s special attack cannot decrease more")
                    else:
                        print(f"{mon_using.name}'s special attack decreased")



            if effect == 'self_defense':
                def_stage=mon_using.defense_stage
                if self_stat_rng<=move.effect_chance[ei]:
                    prior_stage=def_stage
                    mon_using.defense_stage=self.stage_change(def_stage, move.magnitude[ei])
                    if prior_stage<mon_using.defense_stage:
                        print(f"{mon_using.name}'s defense increased")
                    elif prior_stage==mon_using.defense_stage:
                        if prior_stage>0:
                            print(f"{mon_using.name}'s defense cannot increase more")
                        else:
                            print(f"{mon_using.name}'s defense cannot decrease more")
                    else:
                        print(f"{mon_using.name}'s defense decreased")
            
                

            if effect == 'self_spdef':
                spdef_stage=mon_using.spdef_stage
                if self_stat_rng<=move.effect_chance[ei]:
                    prior_stage=spdef_stage
                    mon_using.spdef_stage=self.stage_change(spdef_stage, move.magnitude[ei])
                    if prior_stage<mon_using.spdef_stage:
                        print(f"{mon_using.name}'s special defense increased")
                    elif prior_stage==mon_using.spdef_stage:
                        if prior_stage>0:
                            print(f"{mon_using.name}'s special defense cannot increase more")
                        else:
                            print(f"{mon_using.name}'s special defense cannot decrease more")
                    else:
                        print(f"{mon_using.name}'s special defense decreased")
            


            if effect == 'self_speed':
                speed_stage=mon_using.speed_stage
                if self_stat_rng<=move.effect_chance[ei]:
                    prior_stage=speed_stage
                    mon_using.speed_stage=self.stage_change(speed_stage, move.magnitude[ei])
                    if prior_stage<mon_using.speed_stage:
                        print(f"{mon_using.name}'s speed increased")
                    elif prior_stage==mon_using.speed_stage:
                        if prior_stage>0:
                            print(f"{mon_using.name}'s speed cannot increase more")
                        else:
                            print(f"{mon_using.name}'s speed cannot decrease more")
                    else:
                        print(f"{mon_using.name}'s speed decreased")



            if effect == 'op_speed':
                s_stage=mon_attacked.speed_stage
                if random.random()<=chance:
                    mon_attacked.speed_stage=self.stage_change(s_stage, magnitude)
                    if s_stage != mon_attacked.speed_stage:
                        print(f"{mon_attacked.name}'s speed decreased")
                    else:
                        print(f"{mon_attacked.name}'s speed cannot decrease more")



            ei+=1
            
    def stage_change(self, stage, increase):
        if (stage+increase)>6:
            return(6)
        elif (stage+increase)<-6:
            return(-6)
        else:
            return(stage+increase)
            

    def charge_check(self, mon, move):
        if 'charge' in move.effect:
           if mon.charging==False:
               mon.charging=True
               print(f'{mon.name} is charging up')
               return(True)
           elif mon.charging==True:
               mon.charging=False
               return(False)
        
    def switch_reset(self, mon):
        mon.defense_stage=0
        mon.spdef_stage=0
        mon.attack_stage=0
        mon.spatk_stage=0
        mon.speed_stage=0
        mon.active_turns=0
        mon.fire_spin=False
        if mon.status == 'confused':
            mon.status=None

    def trapped_check(self, player):
        if player.active_pokemon.trapped==True:
           if player.active_pokemon.trapped_time<5:
               player.active_pokemon.trapped_time+=1
               return(True)
           else:
               print(f'{player.active_pokemon.name} is freed from the trap')
               player.active_pokemon.trapped_time=0
               player.active_pokemon.trapped=False
               return(False)

    def effectiveness_check(self, defending_mon, move):
        type_mult=1
            
        if isinstance(defending_mon.type, str) == True:
            type_mult*=type_interactions[move.type][defending_mon.type]
        else:
            for type in defending_mon.type:
                type_mult*=type_interactions[move.type][type]
        
        if type_mult>1:
                print('It was super effective!')
                delay(2)
        elif type_mult<1:
                print("It wasn't very effective")
                delay(2)