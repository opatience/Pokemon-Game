from utils import *
import random

class Status:
    def __init__(self, duration = None, status_message = None, apply_message = None, context = None):
        self.turns = duration
        self.status_message = status_message
        self.apply_message = apply_message
        self.damaging = False
        self.pctdmg = None
        self.context = context
        self.damaging = False

    def apply_status(self, mon):
        pass

    def switch_logic(self, mon):
        pass

    def delay_turn_check(self, mon):
        pass

    def turn_end(self, mon):
        if self.turns != None:
            self.turns += 1
        if self.status_message and self.damaging:
            print(f'{self.status_message} {mon.name}')
            delay(1)
            self.status_damage(mon)
            
    
    def status_damage(self, mon):
        if self.damaging:
            display_damage(mon, (self.pctdmg * mon.hp))

    def add_context(self, context):
        self.context = context


class MajorStatus(Status):
    def __init__(self, volatile_status = False):
        self.volatile_status = volatile_status
        super().__init__()
    
    def apply_status(self, mon):
        if not any(isinstance(s, MajorStatus) for s in mon.status):
            if self.apply_message:
                print(f'{mon.name} {self.apply_message}')
            mon.status.append(self)
        else: 
            print(f'{mon.name} already has a major status')
    
    def switch_logic(self, mon):
        if mon.status.volatile_status == True:
            mon.effects.remove(self)
    
    

    
class Burn(MajorStatus):
    def __init__(self):
        super().__init__()
        self.status_message = 'Fire burns'
        self.apply_message = 'is Burnt'
        self.damaging = True
        self.pctdmg = 1/16
        self.name = 'Burnt'


class Poison(MajorStatus):
    def __init__(self):
        super().__init__()
        self.status_message = 'Poison harms'
        self.apply_message = 'is Poisoned'
        self.damaging = True
        self.pctdmg = 1/16
        self.name = 'Poisoned'

class Confusion(MajorStatus):
    def __init__(self):
        super().__init__()
        self.volatile_status = True
        self.damaging = False
        self.pctdmg = 1/16
        self.name = 'Confused'
        self.apply_message = 'is Confused'
        self.turns = 0

    def delay_turn_check(self, mon):
        confusion_check = random.random()
        confusion_end_check = random.random()
        if self.turns == 4:
            print(f'{mon.name} snaps out of their confusion')
            mon.status.remove(self)
            return False
        elif self.turns>1 and confusion_end_check<=.25:
            print(f'{mon.name} snaps out of their confusion')
            mon.status.remove(self)
            return False
        elif confusion_check <= .33:
            print(f'{mon.name} hit themselves in confusion')
            display_damage(mon, (self.pctdmg * mon.hp))
            return True

class Sleep(MajorStatus):
    def __init__(self):
        super().__init__()
        self.name = 'Asleep'
        self.apply_message = 'is Asleep'
        self.turns = 0
    
    def delay_turn_check(self, mon):
        wakeup_check = random.random()
        if self.turns == 4:
            mon.status.remove(self)
            print(f'{mon.name} woke up')
            return False
        elif wakeup_check <= .33 and self.turns > 1:
            mon.status.remove(self)
            print(f'{mon.name} woke up')
            return False
        else:
            print(f'{mon.name} sleeps through the turn')
            return True

class Paralyze(MajorStatus):
    def __init__(self):
        super().__init__()
        self.name = 'Paralyzed'
        self.apply_message = 'is Paralyzed'
    
    def delay_turn_check(self, mon):
        paralyze_check = random.random()
        if paralyze_check <= .25:
            print(f'{mon.name} is paralyzed')
            return True
        else:
            return False

class MinorStatus(Status):
    def __init__(self):
        super().__init__()
        self.damaging = False

    def switch_logic(self, mon):
        mon.effects.remove(self)

    def apply_status(self, mon):
        if not(self in mon.status):
            mon.status.append(self)
            print(f'{mon.name} {self.apply_message}')

class LeechSeed(MinorStatus):
    def __init__(self):
        super().__init__()
        self.apply_message = 'is hit by leech seed'
        self.status_message = 'Leech Seed drains'
        self.name = 'Leech Seed'
        self.damaging = True

    def status_damage(self, mon):
        mon_targeted = mon
        mon_using = self.context.source
        leech_seed_drain = ((1/8) * mon_targeted.hp)
        mon_targeted.temp_hp -= leech_seed_drain
        print(f"Plants drain {mon_targeted.name}'s health")
        delay(2)
        print(f'{mon_targeted.name} has {round(
                                ((mon_targeted.temp_hp/mon_targeted.hp)
                                 *100))}% hp remaining\n')
        delay(2)

        if round(((mon_using.temp_hp+leech_seed_drain)/mon_using.hp)*100)<100:
            print(f"{mon_using.name} is healed by leech seed")
            delay(2)
            print(f"{mon_using.name} gained {round( 
                                            (((mon_using.temp_hp+leech_seed_drain)/mon_using.hp)
                                            -(mon_using.temp_hp/mon_using.hp))
                                            *100)}% hp")
            delay(2)
            mon_using.temp_hp+=leech_seed_drain

        else:
           print(f"{mon_using.name} is healed by leech seed")
           delay(2)
           print(f'{mon_using.name} is at 100% hp') 
           delay(2)
           mon_using.temp_hp = mon_using.hp

class EffectContext:
    def __init__(self, source = None, target = None, battle = None):
        self.source = source
        self.target = target
        self.battle = battle



    



        
    
    