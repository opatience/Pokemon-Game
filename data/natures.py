class Nature:
    def __init__(self, name, increase, decrease):
        self.name = name
        self.increase = increase
        self.decrease = decrease


natures = [
    Nature("Hardy", None, None),
    Nature("Lonely", "attack", "defense"),
    Nature("Brave", "attack", "speed"),
    Nature("Adamant", "attack", "spatk"),
    Nature("Naughty", "attack", "spdef"),

    Nature("Bold", "defense", "attack"),
    Nature("Docile", None, None),
    Nature("Relaxed", "defense", "speed"),
    Nature("Impish", "defense", "spatk"),
    Nature("Lax", "defense", "spdef"),

    Nature("Timid", "speed", "attack"),
    Nature("Hasty", "speed", "defense"),
    Nature("Serious", None, None),
    Nature("Jolly", "speed", "spatk"),
    Nature("Naive", "speed", "spdef"),

    Nature("Modest", "spatk", "attack"),
    Nature("Mild", "spatk", "defense"),
    Nature("Quiet", "spatk", "speed"),
    Nature("Bashful", None, None),
    Nature("Rash", "spatk", "spdef"),

    Nature("Calm", "spdef", "attack"),
    Nature("Gentle", "spdef", "defense"),
    Nature("Sassy", "spdef", "speed"),
    Nature("Careful", "spdef", "spatk"),
    Nature("Quirky", None, None),
]