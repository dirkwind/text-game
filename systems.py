# all of the main required for the game

import math
import msvcrt # used solely in quicktime events
import random
import sys
import time
import shelve # used for saving data
import progbar.progbar as progbar # quicktime event visualizer
import simpleaudio as sa

class Item(object):

    def __init__(self, name: str, purpose: str, value: int, uses: int, silent=False, **unique_args):
        '''purpose is 'stat_change', 'heal', 'damage', or 'special'
        use dodgable=[True/False] if purpose = 'damage'
        use turns=[num_of_turns: int] and changed_stat=[stat_name: str] if purpose = 'stat_change'
        use special_func=[function] and special_params=[function_params: list/tuple] if purpose = 'special'
        '''

        self.name = name
        self.purpose = purpose
        self.value = value
        self.uses = uses
        self.silent = silent
        self.special_params = []
        if purpose == 'stat_change':
            self.turns = unique_args['turns']
            self.changed_stat = unique_args['changed_stat']
        elif purpose == 'damage':
            self.dodgable = unique_args['dodgable']
        elif purpose == 'special':
            self.special_func = unique_args['special_func']
            self.special_params = unique_args['special_params']

class Enemy_Item(Item):
    
    active_items = []
    
    @classmethod
    def clear_active(cls):
        cls.active_items.clear()

    @classmethod
    def check_active(cls, current_turn, enemy):
        for i, item in enumerate(cls.active_items):
            # index 0 : purpose, 1 : value, 2 : turn_when_deactivates, 3 : item_name
            if current_turn >= item[2]:
                enemy[item[0]] -= item[1]
                text_scroll(f'\n{enemy["name"]}\'s item, {item[3].upper()}, has worn off!\n')
                cls.active_items.pop(i)


    def activate(self, current_turn=0, enemy={}, bonus_def=0):
        # checks if an item should have been used
        if self.uses <= 0: 
            print('Error: Enemy_Item used with {} uses left'.format(self.turns))
            return None
        self.uses -= 1
        
        # prints a message stating that an enemy used an item
        if not self.silent:
            text_scroll(f'\n{enemy["name"]} used {self.name.upper()}!\n')
        
        # item functions
        if self.purpose == 'heal':
            enemy['health'] += self.value

            if enemy['health'] > enemy['max_health']:
                enemy['health'] = enemy['max_health']
                if not self.silent:
                    text_scroll(f'\n{enemy["name"]} reached full HP!\n')
            else:
                if not self.silent:
                    text_scroll(f'\n{enemy["name"]} recovered {self.value} HP!\n')

        elif self.purpose == 'stat_change':
            enemy[self.changed_stat] += self.value
            Enemy_Item.active_items.append([self.changed_stat, self.value, self.turns + current_turn, self.name])
            if not self.silent:
                text_scroll(f'\n{enemy["name"]}\'s {self.changed_stat.upper()} has been increased by {self.value} for {self.turns} turns!\n')

        elif self.purpose == 'damage':

            if self.dodgable: # if the item can be dodged by the player
                text_scroll(f"\nGet ready to dodge the {self.name.upper()}!\n")
                base_attack = self.value
                time.sleep(1)
                difference = quicktime_bar('f', enemy['speed'])

                if difference == 0:
                    print('Dodged!')
                    attack = 0
                elif difference <= 2:
                    print('Grazed!')
                    attack = base_attack - math.floor(base_attack*0.3)
                elif difference <= 5:
                    print('Hit!')
                    attack = base_attack - math.floor(base_attack*0.085)
                elif difference <= 15:
                    print('Solid Hit!')
                    attack = base_attack
                else:
                    print('Critical!')
                    attack = base_attack + round(base_attack*0.25)

                if attack != 0:
                    damage = attack - (player.defense + bonus_def)
                    if damage < 0: damage = 0
                    player.health -= damage
                    text_scroll(f'\nYou were hit for {damage} damage! You are now at {player["health"]} HP!\n')
                else:
                    text_scroll(f'\nThe {self.name.upper()} missed!\n')

            else: # if it is impossible for the player to dodge the item
                damage = self.value - (player.defense + bonus_def)
                if damage < 0: damage = 0
                player.health -= damage
                text_scroll(f'\nYou couldn\'t avoid the {self.name.upper()}!\n')
                text_scroll(f'\nYou were hit for {damage} damage! You are now at {player["health"]} HP!\n')
        
        elif self.purpose == 'special':
            # returned in case special_func returns a value
            return self.special_func(*configure_params(self.special_params, enemy, current_turn, self.silent))
        
class Player_Item(Item):

    active_items = []
    
    @classmethod
    def clear_active(cls):
        cls.active_items.clear()

    @classmethod
    def check_active(cls, current_turn):
        for i, item in enumerate(cls.active_items):
            # index 0 : purpose, 1 : value, 2 : turn_when_deactivates, 3 : item_name
            if current_turn >= item[2]:
                player[item[0]] -= item[1]
                text_scroll(f'\nYour item, {item[3].upper()}, has worn off!\n')
                cls.active_items.pop(i)


    def activate(self, current_turn=0, enemy={}, bonus_attack=0):
        # checks if an item should have been used
        if self.uses <= 0: 
            print('Error: Player_Item used with {} uses left'.format(self.turns))
            return None
        self.uses -= 1
        
        # item functions
        if self.purpose == 'stat_change':
            Player_Item.active_items.append((self.changed_stat, self.value, current_turn + self.turns, self.name))           

        if not self.silent:
            text_scroll(f'\nYou used {self.name.upper()}!\n')

        if self.purpose == 'heal':
            player.health += self.value
            if player.health > player.max_health:
                player.health = player.max_health
                if not self.silent: text_scroll(f'\nYou are now at MAX HP!\n')
            else:
                if not self.silent: text_scroll(f'\nYou gained {self.value} HP!\n')

        elif self.purpose == 'stat_change':
            player[self.changed_stat] += int(self.value)
            if not self.silent: text_scroll(f'\n{self.changed_stat.upper()} increased by {self.value} for {self.turns} turn(s)!\n')

        elif self.purpose == 'damage':
            chance_num = random.randint(1, 100)
            if chance_num >= int((enemy['speed'] / 20) * 100) or not self.dodgable: # checks if the enemy dodged the item (is based on random number and enemy's speed)
                item_damage = self.value - enemy['defense']
                if item_damage < 0: item_damage = 0
                enemy['health'] -= item_damage
                if not self.silent: text_scroll(f'\nYou did {item_damage} damage to {enemy["name"]}! {enemy["name"]} is now at {enemy["health"]} HP!\n')
            else:
                if not self.silent: text_scroll(f'\n{enemy["name"]} dodged the {self.name.upper()}!\n')
                
        elif self.purpose == 'special':
            return self.special_func(*configure_params(self.special_params, enemy, current_turn))

class Entity(object):
    def __getitem__(self, item):
        '''Allows for dictionary-style getting of values
        e.g. entity['health'] will still work'''
        return getattr(self, item)
    
    def __setitem__(self, item, value):
        '''Allows for dictionary-style setting of values
        e.g. entity['health'] = 100 will still work'''
        setattr(self, item, value)

class Player(Entity):

    def __init__(self, name):
        self.name = name
        self.attack = 15
        self.defense = 5
        self.health = 40
        self.max_health = 40
        self.base_attack = 15
        self.base_defense = 5
        self.xp = 0
        self.xp_to_next = 40
        self.level = 0
        self.killed = 0
        self.spared = 0
        self.fled = 0
        self.inventory = [
            #purposes are 'heal', 'stat_change', 'damage', 'special'
            Player_Item('Bandage', 'heal', 10, 2),
            Player_Item('Energy Drink', 'stat_change', 10, 3, changed_stat='attack', turns=3),
            Player_Item('Frail Shield', 'stat_change', 10, 2, changed_stat='defense', turns=3)
        ]

def text_scroll(text: str, period=0.25, comma=0.15, normal=0.03, space=None, voice_file=None, speed_factor=1):
    '''Progressively prints text to the screen instead of printing it all at once.
    \n\n* The float values of period, comma, normal, and space is the duration in seconds the program pauses after printing a character.
    \n* period is any ending punctuation (.?!), comma is any pausing punctuation (,;:), space is ' ', and normal is every other character.
    \n* If space is None then space will be the same value as normal
    \n* voice_file is a wav file that will play when a character is printed
    \n* speedfactor affects the duration of all characters
    '''
    if voice_file is not None:
        # creates a WaveObject if a voice_file was provided
        wave_obj = sa.WaveObject.from_wave_file(voice_file)
    if space is None:
        space = normal
    for letter in text:
        sys.stdout.write(letter)
        sys.stdout.flush()
        if voice_file is not None:
            # plays the voice_file if it was provided
            wave_obj.play()
        if letter in set('.?!'):
            time.sleep(period*speed_factor)
        elif letter in set(',;:'):
            time.sleep(comma*speed_factor)
        elif letter == ' ':
            time.sleep(space*speed_factor)
        else:
            time.sleep(normal*speed_factor)

def quicktime_bar(key='f', speed_factor=0):
    '''Starts a quicktime bar event. Returns a value between 0 and 30.'''
    percent = 0
    total = 60
    attack_bar.startProgress(f'Press {key.upper()}:')
    while percent < total:
        percent += 1
        inc_factor = lambda x : round(x * ((0.95) ** speed_factor))
        time.sleep(random.randint(inc_factor(10), inc_factor(20))/ 1000)
        attack_bar.updateProgress( attack_bar.toPercent( round(-2 * abs(percent - 30) + total ), total) )
        if msvcrt.kbhit():
            if ord(msvcrt.getch()) == ord(key):
                break
    attack_bar.pauseProgress()
    return abs(percent - 30)

def player_attacked(enemy: dict, bonus_def):
    '''Prompts the player to try and dodge the enemy's attack.
    enemy is the enemy dict and bonus_def is extra def the player has
    '''
    text_scroll("\nGet ready to dodge!\n")
    base_attack = enemy['attack']
    defense = player.defense
    time.sleep(1)
    difference = quicktime_bar('f', enemy['speed'])
    if difference == 0:
        print('Dodged!')
        attack = 0
    elif difference <=2:
        print('Grazed!')
        attack = base_attack - math.floor(base_attack*0.4)
    elif difference <= 5:
        print('Hit!')
        attack = base_attack - math.floor(base_attack*0.1)
    elif difference <= 15:
        print('Solid Hit!')
        attack = base_attack
    else:
        print('Critical!')
        attack = base_attack + round(base_attack*0.2)
    if attack != 0:
        damage = attack - (defense + bonus_def)
        if damage < 0: damage = 0
        player.health -= damage
        text_scroll(f'\nYou were hit for {damage} damage! You are now at {player["health"]} HP!\n')
    else:
        text_scroll(f'\n{enemy["name"]} missed!\n')
        time.sleep(0.5)

def add_item(item_object, silent=False):
    '''Help for Player_Item class initiallization:
    purpose is 'stat_change', 'heal', 'damage', or 'special'
    use dodgable=[True/False] if purpose = 'damage'
    use turns=[num_of_turns: int] and changed_stat=[stat_name: str] if purpose = 'stat_change'
    use special_func=[function] and special_params=[function_params: list/tuple] if purpose = 'special'
    '''
    existing_items = [(itm.name, itm.purpose) for itm in player['inventory']]
    if (item_object.name, item_object.purpose) in existing_items:
        for i, item in enumerate(existing_items):
            if item == (item_object.name, item_object.purpose):
                player.inventory[i].uses += item_object.uses
                break
    elif len(player.inventory) < 8:
        player.inventory.append(item_object)
        if not silent:
            text_scroll(f'\n{item_object.name.upper()} has been added to your inventory!\n')
    else:
        if not silent:
            text_scroll(f'\nYour inventory is full.\n')

def game_over():
    '''Stops the program.'''
    sys.exit()

def gain_xp(enemy, silent=False):
    '''Gives xp to the player.
    If enemy is an enemy dict xp will automatically be derived from the enemy's stats
    If enemy is an int the value of int will be given to the player
    silent determines if a message is printed or not (this is recommended to be True if a large amount of xp is being given)
    '''
    stat_mod = player.level // 5 + 1
    if type(enemy) != int:
        xp_gain = enemy["max_health"] + enemy["attack"] + enemy["defense"] + enemy["speed"] + enemy["bonus_xp"]
    else:
        xp_gain = enemy
    player.xp += xp_gain
    while player.xp >= player.xp_to_next: 
        player.level += 1
        for stat in ['attack', 'defense']:
            player[stat] += 2 * stat_mod
        player.max_health += 7 * stat_mod
        player.health = player.max_health
        player.xp_to_next = round(player.xp_to_next * 1.8)
        if not silent:
            text_scroll(f'\nYou LEVELED UP to LEVEL {player.level}!\n')
    else:
        if not silent:
            text_scroll(f'\nYou gained {xp_gain} XP! You need {player.xp_to_next - player.xp} more XP to level up!\n')

def check_win_conditions(enemy):
    '''returns True when a win condition is met'''
    if enemy['give_up'][0] >= 100: # enemy gives up peacefully
        text_scroll(f"\n{enemy['give_up'][1]}\n")
        gain_xp(enemy)
        player.spared += 1
        return True
    if player.health <= 0: # player dies
        text_scroll(f'\n{enemy["name"]} has defeated you...\n')
        game_over()
        return True
    if enemy['health'] <= 0: # player kills enemy
        text_scroll(f'\n{enemy["name"]} has fallen... You Win!\n')
        gain_xp(enemy)
        player.killed += 1
        return True
    return False

def check_positive(dict: dict, key: str, index=0):
    '''Will set value of an element/item to 0 if it is less than 0
    index is only used if the item at key in dict is a list or tuple'''
    if type(dict[key]) in (list, tuple):
        if dict[key][index] < 0:
            dict[key][index] = 0
    else:
        if dict[key] < 0:
            dict[key] = 0

def varied_response(response1, response2, pause=0.5):
    '''Text scrolls 2 messages with pause seconds in between'''
    text_scroll(f'\n{response1}\n')
    time.sleep(pause)
    text_scroll(f'\n{response2}\n')

def stat_change(entity: dict, stat: str, value: int, silent=False):
    '''Changes the provided numerical stat of an enemy/player dict by value
    This automatically does not allow for stats to become negative
    silent determines whether or not a message is scrolled
    '''
    entity[stat] += value
    if entity[stat] < 0: 
        entity[stat] = 0
    if not silent:
        if value < 0:
            text_scroll(f'\n{entity["name"]}\'s {stat.upper()} decreased by {abs(value)}!\n')
        else:
            text_scroll(f'\n{entity["name"]}\'s {stat.upper()} increased by {value}!\n')

def configure_params(params, enemy, turns, silent=False):
    '''configures parameters for enemy and player items'''
    updated_params = []
    for par in params:
        if par == '$enemy':
            updated_params.append(enemy)
        elif par == '$turns':
            updated_params.append(turns)
        elif par == '$player':
            updated_params.append(player)
        elif par == '$silent':
            updated_params.append(silent)
        else:
            updated_params.append(par)
    return updated_params

# ---------------------------------------- BATTLE ----------------------------------------

def battle(enemy: dict):
    '''Initiates a battle between player and the provided enemy.'''
    in_battle = True
    responses = enemy['responses']
    response_keys = list(enemy['responses'].keys())
    enemy_name = enemy['name']

    text_scroll(f"\n{enemy['intro']}\n")
    time.sleep(0.5)
    
    bonus_damage = 0
    bonus_def = 0
    turns = 0

    while in_battle:
    
        if check_win_conditions(enemy):
            return None

        attack = True
        
        # --- debug area ---
        #print('test', turns)
        

        #choices are below
        print(f'\nYOUR HP: {player.health}')
        text_scroll('Would you like to 1) ATTACK, 2) ITEM, 3) ACT, or 4) RUN?\n\nYour choice: ')
        choice = str(input(''))

        # ------------- CHOICE 1: ATTACK -------------

        if choice == '1':
            base_attack = player.attack
            defense = enemy['defense']
            difference = quicktime_bar('f')
            if difference == 0:
                print('Critical!\t')
                base_damage = base_attack + round(base_attack*0.2)
            elif difference + enemy['speed'] <= 3:
                print('Great Hit!\t')
                base_damage = base_attack
            elif difference + enemy['speed'] <= 7:
                print('Good Hit!\t')
                base_damage = base_attack - math.ceil(base_attack*0.2)
            elif difference + enemy['speed'] <= 12:
                print('Fair Hit!\t')
                base_damage = base_attack - math.ceil(base_attack*0.5)
            else:
                print('Miss!\t\t')
                base_damage = 0
            if base_damage > 0:
                damage = (base_damage + bonus_damage) - defense
                if damage < 0: damage = 0
                enemy['health'] -= damage
                text_scroll(f'\nYou hit {enemy_name} for {damage} damage! {enemy_name} is now at {enemy["health"]} HP!\n')
            else:
                text_scroll('\nYou missed...\n')
            
            turns += 1
            
        # ------------- CHOICE 2: ITEM -------------    

        elif choice == '2':
            inventory = player.inventory
            if len(inventory) == 0:
                text_scroll('\nYou have no ITEMS!\n')
                attack = False
            else:
                choosing = True
                while choosing:
                    print('\n0 : EXIT')
                    for i, item in enumerate(inventory):
                        print(f'{i + 1} : {item.name.upper()} x{item.uses}')
                    text_scroll('\nWhat is your choice (enter number)? ')
                    item_choice = str(input(''))
                    if item_choice in set([str(num) for num in range(1, len(inventory) + 1)]):
                        choosing = False
                        cont_item = True
                    elif item_choice == '0':
                        choosing = False
                        cont_item = False
                        attack = False
                
                if cont_item:
                    item_index = int(item_choice) - 1
                    if '&turns' in inventory[item_index].special_params:
                        turns = inventory[item_index].activate(turns, enemy, bonus_damage)
                    else:
                        inventory[item_index].activate(turns, enemy, bonus_damage)
                    if inventory[item_index].uses <= 0:
                        inventory.pop(item_index)

        # ------------- CHOICE 3: ACT -------------

        elif choice == '3':
            text_scroll(f'\n1) {response_keys[0].upper()}, 2) {response_keys[1].upper()}, 3) {response_keys[2].upper()}, 4) {response_keys[3].upper()}, 5) CHECK, or 0) EXIT?\n\nYour choice: ')
            choice = str(input(''))
            random_response = ''
            if choice == '1':
                random_response = random.choice(responses[response_keys[0]])
                varied_response(random_response[0][0], random_response[0][1])
                enemy['give_up'][0] += random_response[1]
                check_positive(enemy, 'give_up', 0)
            elif choice == '2':
                random_response = random.choice(responses[response_keys[1]])
                varied_response(random_response[0][0], random_response[0][1])
                enemy['give_up'][0] += random_response[1]
                check_positive(enemy, 'give_up', 0)
            elif choice == '3':
                random_response = random.choice(responses[response_keys[2]])
                varied_response(random_response[0][0], random_response[0][1])
                enemy['give_up'][0] += random_response[1]
                check_positive(enemy, 'give_up', 0)
            elif choice == '4':
                random_response = random.choice(responses[response_keys[3]])
                varied_response(random_response[0][0], random_response[0][1])
                enemy['give_up'][0] += random_response[1]
                check_positive(enemy, 'give_up', 0)
            elif choice == '5':
                if enemy['checkable'][0]:
                    print(f"\nNAME: {enemy_name}\nATTACK: {enemy['attack']}\nDEFENSE: {enemy['defense']}\nSPEED: {enemy['speed']}\nHEALTH: {enemy['health']}\n")
                    text_scroll(f'{enemy["description"]}\n')
                    time.sleep(1)
                    input('Press enter to continue...')
                else:
                    text_scroll(f'\n{enemy["checkable"][1]}\n') # prints reason why enemy can't be checked
            else:
                turns -= 1
                attack = False
            if len(random_response) >= 3: # changes a stat if there are enough parameters for it
                stat_change(enemy, random_response[2], random_response[3])
            turns += 1
        
        # ------------- CHOICE 4: RUN -------------

        elif choice == '4':
            if enemy['can_flee']:
                text_scroll(f'\nIt appears that {enemy_name} was too much for you...\n')
                player.spared += 1
                player.fled += 1
                return None
            else:
                text_scroll(f'\nYou can\'t run away from {enemy_name}...\n')

        else:
            text_scroll('\nThat was not a choice.\n')
            attack = False

        if check_win_conditions(enemy):
            return None

        Player_Item.check_active(turns)

         # ------------- ENEMY ACTION -------------

        Enemy_Item.check_active(turns, enemy)

        if attack:
            # number that determines whether or not the enemy will use an item
            action_factor = random.randint(1, 100000)/1000 # done this way for 3 decimal places of precision

            if action_factor <= enemy['use_item_chance'] and len(enemy['inventory']) > 0: # don't want to use and item if there are no items
                choosing_item = True
                max_loops = 100
                loop_count = 0
                while choosing_item: # looping to make sure enemy doesn't use a 'heal' item when it cant

                    if not loop_count <= max_loops:
                        # this prevents this loop from becoming an infinite loop
                        player_attacked(enemy, bonus_def)
                        break

                    item = random.choice(enemy['inventory'])

                    if item.purpose == 'heal' and enemy['health'] >= enemy["max_health"]:
                        if len(enemy['inventory']) == 1:
                            # attack the player if the enemy only has a healing item and is at full health
                            choosing_item = False
                            player_attacked(enemy, bonus_def)
                        else:
                            loop_count += 1
                            continue
                    else:

                        if '&turns' in item.special_params: # if item is a 'special' function that changes turns
                            turns = item.activate(turns, enemy, bonus_def)
                        else:
                            item.activate(turns, enemy, bonus_def)
                        
                        # checking the number of uses for item
                        if item.uses <= 0:
                            enemy['inventory'].pop(enemy['inventory'].index(item))
                            break

                        choosing_item = False   
            
            else:
                player_attacked(enemy, bonus_def)




player = Player("Bigg_Milk")

def save(stage):
    '''Saves player data and provided stage into a shelve file.'''
    save_file = shelve.open('saves/save.db')
    save_file['player_object'] = player
    save_file['stage'] = stage
    save_file.close()
    

def get_save():
    '''Gets the data for player and stage from a shelve file.'''
    global stage, player
    with open('saves/save.db.dir', 'r') as sv:
        if len(sv.readlines()) > 1:
            save_file = shelve.open('saves/save.db')
            stage = int(save_file['stage'])
            player = dict(save_file['player_object'])
            save_file.close()
        else:
            save(0)
            get_save()

def erase_save():
    '''Deletes saved data'''
    with open('saves/save.db.dir', 'w') as file1:
        file1.write('')
    with open('saves/save.db.dat', 'w') as data:
        data.write('')
    

#get_save()
attack_bar = progbar.ProgressBar(bar_size=30)
