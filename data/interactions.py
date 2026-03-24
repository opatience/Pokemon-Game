type_pool=[
    "normal",
    "fire",
    "water",
    "electric",
    "grass",
    "ice",
    "fighting",
    "poison",
    "ground",
    "flying",
    "psychic",
    "bug",
    "rock",
    "ghost",
    "dragon",
    "dark",
    "steel",
    "fairy"
]
def build_matchups(super_effective, not_effective, base_type):
    name = {}
    for t in type_pool:
        if t in super_effective:
            name[t] = 2
        elif t in not_effective:
            name[t] = 0.5
        else:
            name[t] = 1
    return name

type_interactions = {}
type_interactions['normal'] = build_matchups(
    [], 
    ['ghost'], 
    'normal'
)
type_interactions['fire'] = build_matchups(
    ['grass', 'ice', 'bug', 'steel'], 
    ['fire', 'water', 'rock', 'dragon'],
    'fire'
)
type_interactions['water'] = build_matchups(
    ['ground', 'fire', 'rock'], 
    ['water', 'grass', 'dragon'], 
    'water'
)
type_interactions['electric'] = build_matchups(
    ['water', 'flying'], 
    ['electric', 'grass', 'ground', 'flying'], 
    'electric'
)
type_interactions['grass'] = build_matchups(
    ['water', 'ground', 'rock'], 
    ['fire', 'grass', 'poison', 'flying', 'bug', 'dragon', 'steel'], 
    'grass'
)
type_interactions['ice'] = build_matchups(
    ['grass', 'ground', 'flying', 'dragon'], 
    ['fire', 'water', 'ice', 'steel'], 
    'ice'
)
type_interactions['fighting'] = build_matchups(
    ['normal', 'ice', 'dark', 'steel', 'rock'], 
    ['poison', 'flying', 'psychic', 'bug', 'fairy'], 
    'fighting'
)
type_interactions['poison'] = build_matchups(
    ['grass', 'fairy'], 
    ['poison', 'ground', 'rock', 'ghost', 'steel'], 
    'poison'
)
type_interactions['ground'] = build_matchups(
    ['fire', 'electric', 'poison', 'rock', 'steel'], 
    ['grass', 'flying', 'bug'], 
    'ground'
)
type_interactions['flying'] = build_matchups(
    ['grass', 'fighting', 'bug'],
    ['electric', 'rock', 'steel', 'ground'],
    'flying'
)
type_interactions['psychic'] = build_matchups(
    ['fighting', 'poison'],
    ['psychic', 'steel'],
    'psychic'
)
type_interactions['bug'] = build_matchups(
    ['grass', 'psychic', 'dark'],
    ['fire', 'fighting', 'poison', 'flying', 'ghost', 'steel', 'fairy'],
    'bug'
)
type_interactions['rock'] = build_matchups(
    ['fire', 'ice', 'flying', 'bug'],
    ['fighting', 'ground', 'steel'],
    'rock'
)
type_interactions['ghost'] = build_matchups(
    ['psychic', 'ghost'],
    ['dark', 'normal'],
    'ghost'
)
type_interactions['dragon'] = build_matchups(
    ['dragon'],
    ['steel'],
    'dragon'
)
type_interactions['dark'] = build_matchups(
    ['psychic', 'ghost'],
    ['fighting', 'dark', 'fairy'],
    'dark'
)
type_interactions['steel'] = build_matchups(
    ['ice', 'rock', 'fairy'],
    ['fire', 'water', 'electric', 'steel', 'poison'],
    'steel'
)
type_interactions['fairy'] = build_matchups(
    ['fighting', 'dragon', 'dark'],
    ['fire', 'poison', 'steel'],
    'fairy'
)

stages = {
    -6: 0.25,
    -5: 0.2857,
    -4: 0.3333,
    -3: 0.4,
    -2: 0.5,
    -1: 0.6667,
     0: 1.0,
     1: 1.5,
     2: 2.0,
     3: 2.5,
     4: 3.0,
     5: 3.5,
     6: 4.0
}