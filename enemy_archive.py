# an archive of scrapped enemys
# NOTE: these are likely not up to date with the most recent syntax for enemies
#   warning: these enemies are probably a bit cringey

grunt = {
    'name': 'Tobu',
    'intro': 'Tobu waddles in! He doesn\'t look like he wants to fight...', # intro message
    'description': 'Just a normal guy conscripted into the army. Doesn\'t like war.', # short description of enemy
    'checkable': [True, "name can't be checked."], # whether or not player can check enemy's stats
    'attack': 21,
    'defense': 6,
    'speed': 5, # 4+ = no Great Hits, 8+ = no Good Hits, 13+ = no Fair Hits, 20+ = 100% immune to damage items, all keep Critical (nums in b/w included)
    'health': 50,
    'max_health': 50,
    'give_up': [0, "Tobu can't muster the willpower to keep fighting you..."],
    'can_flee': True,
    'bonus_xp': 30, # extra xp for the player if they defeat this enemy
    'responses': {
        'flirt': [
            (['"Damn, Tobu, you lookin mighty fine..."', 'Tobu is flattered, but is more concerned about not dying.'], 15),
            (['"If your ass was a cake I\'d devour it..."', '"Thanks, but no thanks..."'], 5)
            ],
        'sympathize': [
            (['You talk about how this war is a bunch of bullshit.', 'Tobu\'s eyes light up.'], 30)
            ],
        'insult': [
            (['"I thought that you had to train to become a soldier, but, obviously, you don\'t."', 'Tobu is unaffected...'], -10),
            (['"You\'re one ugly motherfucker."', 'Tobu seems agitated...'], -30, 'attack', 2)
            ],
        'threaten': [
            (['You threaten to kill Tobu\'s family...', 'Tobu is horrified...'], 0, 'defense', -2),
            (['You threaten to maim Tobu\'s cat...', 'Tobu doesn\'t have a cat...'], 0)
            ]
    }
}

anger = {
    'name': 'Carle',
    'intro': 'Carle charges in...', # intro message
    'description': '', # short description of enemy
    'checkable': [False, "Carle refuses to share his personal information."], # whether or not player can check enemy's stats
    'attack': 60,
    'defense': 10,
    'speed': 7, # 4+ = no Great Hits, 8+ = no Good Hits, 13+ = no Fair Hits, 20+ = 100% immune to damage items, all keep Critical (nums in b/w included)
    'health': 65,
    'max_health': 65,
    'give_up': [0, "Carle pities you for your apparent lack of intelligence."],
    'can_flee': False,
    'bonus_xp': 100, # extra xp for the player if they defeat this enemy
    'responses': { # use (['', ''], 0, stat, value) to change a stat's value when an act is performed
        'flirt': [
            (['"Fuck me."', '"...Hell no."'], -15)  
            ],
        'insult': [
            (['"You have no style."', '"You\'re one to talk."'], -20)
            ],
        'soil him': [
            (['You throw mud on his shirt.', '"What the fuck is your issue?"'], 25)
            ],
        'disgust': [
            (['You roll on the ground and scream "I am a worm, look at me sqirm" repeatedly.', 'Carle stares, dumbfounded.'], 35)
            ]
    }
}

ashley = {
    'name': 'Ashley',
    'intro': 'Ashley hops in!',
    'description': 'Artist, animator, etc. Also, a rabbit.',
    'checkable': [True, "name can't be checked."], # whether or not player can check enemy's stats
    'attack': 20,
    'defense': 5,
    'speed': 0, # 4+ = no Great Hits, 8+ = no Good Hits, 13+ = no Fair Hits, 20+ = 100% immune to damage items, all keep Critical (nums in b/w included)
    'health': 45,
    'max_health': 45,
    'give_up': [0, "Ashley is too flustered to keep fighting... You Win!"],
    'can_flee': False,
    'bonus_xp': -15, # extra xp for the player if they defeat this enemy
    'responses': {
        'flirt': [[['"Oh Ashley..."', 'Ashley is flustered!'], 60]],
        'hug': [[['You try to hug her...', 'She declines because you are a stranger.'], -10]],
        'eat carrots': [[['You eat a few carrots...', 'Ashley becomes jealous!'], -10]],
        'pet': [[['You approach Ashley to enact the pet...', 'It fails.'], -10]]
    }
}

enemy1 = {
    'name': 'Cretin',
    'intro': 'Cretin shimmies before you!',
    'description': 'A lowly creature lacking relationships.',
    'checkable': [True, "name can't be checked."], # whether or not player can check enemy's stats
    'attack': 25,
    'defense': 7,
    'speed': -20, # 4+ = no Great Hits, 8+ = no Good Hits, 13+ = no Fair Hits, 20+ = 100% immune to damage items, all keep Critical (nums in b/w included)
    'health': 70,
    'max_health': 70,
    'give_up': [0, "Cretin thinks you're too cool to kill... You Win!"],
    'can_flee': True,
    'bonus_xp': 10, # extra xp for the player if they defeat this enemy
    'responses': {
        'flirt': [
            (['"Your... cool?"', 'Smooth.'], 20), 
            (['"You really be lookin like a snacc..."', 'Cretin doesn\'t know what this means but is flattered anyway.'], 40)
            ],
        'compliment': [
            (['"You\'re pretty neat."', 'Cretin is confused yet happy!'], 50),
            (['"You may not look cool, but you\'re definitely cool on the inside."', 'Cretin ignored the insult and accepted the compliment!'], 30)
            ],
        'insult': [
            (['"You\'re the ugliest thing I\'ve ever seen, and I\'ve seen some real nasty stuff"', 'Cretin is very hurt by this.'], -70),
            (['"Scum like you make me want to see the world burn."', 'Ouch...'], -90)
            ],
        'take a pee break': [
            (['You urinate...', 'Cretin seems aroused.'], 30),
            (['You try to urinate...', 'It fails! Try next turn...'], 0)
            ]
    }
}

fly = {
    'name': 'Fly',
    'intro': 'Fly buzzes in!',
    'description': 'Just an ordinary fly.',
    'checkable': [True, "name can't be checked."], # whether or not player can check enemy's stats
    'attack': 1,
    'defense': 0,
    'speed': 18, # 4+ = no Great Hits, 8+ = no Good Hits, 13+ = no Fair Hits, 20+ = 100% immune to damage items, all keep Critical (nums in b/w included)
    'health': 1,
    'max_health': 1,
    'give_up': [0, "Fly was too bored to stay... You Win!"],
    'can_flee': True,
    'bonus_xp': 50, # extra xp for the player if they defeat this enemy
    'responses': {
        'flirt': [
            (['"Hey, baby girl, I know you want some of my juice..."', 'Fly didn\'t understand that... noone would understand that...'], 5),
            (['"I can see us having children..."', 'What are you on about?'], 5),
            (['"My dad once told me that flies were mindless idiots, but you proved him wrong."', 'Fly doesn\'t recognize this language...'], 10),
            (['"I can hardly contain myself in your presence..."', 'Fly wasn\'t paying attention...'], 5)
            ],
        'shoo': [
            (['"Leave, please."', '...'], 5),
            (['You swat at Fly...', 'Fly seems displeased.'], -10),
            (['"Go away."', '...'], 5),
            (['"Leave this "', ''], 0)
            ],
        'sit': [
            (['You sit down......', 'You stand up.'], 30),
            (['You stop standing....', 'You start standing'], 30)
            ],
        'ignore': [
            (['You ignore Fly...', 'It\'s super effective!'], 30),
            (['You divert your attention to a pebble on the ground...', 'It\'s working!'], 30)
            ]
    }
}

ofe = {
    'name': 'Ofe',
    'intro': 'Ofe lumbers...',
    'description': 'Strongest warrior of E army.',
    'checkable': [False, "Ofe refuses to be CHECKED."], # whether or not player can check enemy's stats
    'attack': 370,
    'defense': 100,
    'speed': 2, # 4+ = no Great Hits, 8+ = no Good Hits, 13+ = no Fair Hits, 20+ = 100% immune to damage items, all keep Critical (nums in b/w included)
    'health': 600,
    'max_health': 600,
    'give_up': [0, "Ofe is too tired to continue fighting..."],
    'can_flee': False,
    'bonus_xp': 100, # extra xp for the player if they defeat this enemy
    'responses': {
        'flirt': [
            (['"Hey, big guy, we should hang out sometime..."', 'Ofe stares, disgusted.'], 1)
            ],
        'insult': [
            (['"I thought you were supposed E\'s strongest."', 'Ofe is unaffected...'], 1)
            ],
        'sing': [
            (['You sing a peaceful lullaby...', 'Ofe seems to get tired...'], 20)
            ],
        'threaten': [
            (['You spout words that threaten Ofe\'s family...', 'Ofe seems agitated...'], -10)
            ]
    }
}