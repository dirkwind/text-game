# this is where the story is written

from systems import *
from aux_functions import *
from playsound import *
from time import *

# check enemy_format.txt for enemy formatting info

dog = Enemy.from_dict({
    'name': 'Gremlin',
    'intro': 'You\'ve encontered a Gremlin!', # intro message
    'description': 'A fat couch potato.', # short description of enemy
    'checkable': [True, "name can't be checked."], # whether or not player can check enemy's stats
    'attack': 1,
    'defense': 10,
    'speed': 4, # 4+ = no Great Hits, 8+ = no Good Hits, 13+ = no Fair Hits, 20+ = 100% immune to damage items, all keep Critical (nums in b/w included)
    'health': 20,
    'max_health': 20,
    'give_up': [0, 'Blarg... You Win!'],
    'can_flee': False,
    'bonus_xp': random.randint(1,40), # extra xp for the player if they defeat this enemy
    'inventory': [ # Enemy_Item(self, name, purpose='heal, stat_bonus, damage', value, uses, usage_chance, dodgable=None, turns=0) 
        Enemy_Item('Goblin Engergy Jab', 'special', None, 3, False, special_func=turn_based_damage, special_params=['$player', '$enemy', '$turns', 1, True])
    ],
    'use_item_chance': 20, # between and including 1 through 100; percentage chance (w/ precision of 3 decimal places) that the enemy will use an item
    'responses': { # use (['', ''], 0, stat, value) to change a stat's value when an act is performed
        'threaten': [
            (['"I destroy your hentai!"', 'Gremlin tenses up'], 20, 'defense', 2),
            (['"Oh what a weeb, what a weeb!"', '"Are you trying to make me laugh by insulting me and my tradition from afar?"'], 20)
            ],
        'be a chad': [
            (['You beat your chest and grunt repeatedly.', '"Are you making fun of me?"'], -5)
            ],
        'rub belly': [
            (['You carress his massive stomach.', '"Giggity giggity goo!"'], 30)
            ],
        'indulge': [
            (['You read manga with the foul creature.', 'Mmm...'], 100)
            ]
    }
})

doge = Enemy.from_dict({
    'name': 'Raptor',
    'intro': '"rawr"', # intro message
    'description': 'Just a velociraptor.', # short description of enemy
    'checkable': [True, "name can't be checked."], # whether or not player can check enemy's stats
    'attack': 7,
    'defense': 4,
    'speed': 12, # 4+ = no Great Hits, 8+ = no Good Hits, 13+ = no Fair Hits, 20+ = 100% immune to damage items, all keep Critical (nums in b/w included)
    'health': 15,
    'max_health': 15,
    'give_up': [player['level'] * 10, "rawr..."],
    'can_flee': True,
    'bonus_xp': 0, # extra xp for the player if they defeat this enemy
    'inventory': [ # Enemy_Item(self, name, purpose='heal, stat_bonus, damage', value, uses, usage_chance, dodgable=None, turns=0) 
        #Enemy_Item('Hamburger', 'stat_change', 10, 1, turns=3, changed_stat='attack')
        Enemy_Item.stat_change("Hamburger", 10, 1, 3, 'attack')
    ],
    'use_item_chance': 5, # between and including 1 through 100; percentage chance (w/ precision of 3 decimal places) that the enemy will use an item
    'responses': { # use (['', ''], 0, stat, value) to change a stat's value when an act is performed
        'feed meat': [
            (['You toss a leg of chicken in the air...', 'rawr'], 100)  
            ],
        'tame': [
            (['You hold your hand out.', 'Raptor touches you.'], 50)
            ],
        'stand still': [
            (['You stand completely still...', 'Raptor couldn\'t see you so it ran away.'], 100)
            ],
        'shoo': [
            (['You tell it to leave...', 'Raptor leaves...'], 100)
            ]
    }
}
)
print(doge.inventory)

#Player.add_item(Player_Item('Anaesthetic Bomb', 'special', None, 2, special_func=ana_bomb, special_params=['$enemy', 1]))
#Player.add_item(Player_Item('Effect Longevity Boost', 'special', None, 3, special_func=change_turns, special_params=['$turns', -4, '&turns']))
Player.add_item(Player_Item.special('Sketchy Throwing Knife', 3, vampire, ['$enemy', '$player', 3]))
#Player.add_item(Player_Item('Charge Attack', 'special', None, 2, special_func=turn_based_damage, special_params=['$enemy', '$turns', 0.45, True]))

battle(doge)