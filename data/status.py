from utils import *
import random

class Status:
    def __init__(self, duration = None, status_message = None, apply_message = None):
        self.turns = duration #can maybe run a bunch of if statements to make this without harcoding
        self.status_message = status_message
        self.apply_message = apply_message

    def apply_status(self, mon):
        pass

    def switch_logic(self, mon):
        pass

    def delay_turn_check(self, mon):
        pass

    def status_damage(self, mon):
        pass

    def turn_end(self, mon):
        if self.turns != None:
            self.turns += 1
        if self.status_message:
            print(f'{self.status_message} {mon.name}')
            self.status_damage(mon)
            delay(1)

class MajorStatus(Status):
    def __init__(self, volatile_status = False, damaging = False, pctdmg = None):
        self.volatile_status = volatile_status
        self.damaging = damaging
        self.pctdmg = pctdmg
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

    def status_damage(self, mon):
        display_damage(mon, (self.pctdmg * mon.hp))

class Confusion(MajorStatus):
    def __init__(self):
        super().__init__()
        self.volatile_status = True
        self.damaging = True
        self.pctdmg = 1/16
        self.name = 'Confused'

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
            display_damage(mon, ((self.pctdmg) * mon.hp))
            return True


    



        
    
    