class Pokeball:
    def __init__(self, name, bonus):
        self.name=name
        self.bonus=bonus

pokeball=Pokeball('Pokeball', 1)



item_list=[]
class ModifierItems:
    def __init__(self, name, type, strength, cost):
        self.name=name
        self.type=type
        self.strength=strength
        item_list.append(self)
        self.cost=cost
slides=ModifierItems('Slides', 'speed', 20, 50)
knife=ModifierItems('Knife', 'attack', 1, 50)
shield=ModifierItems('Shield', 'hp', 4, 50)