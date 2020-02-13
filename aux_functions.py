import json
import math
import msvcrt
import random
import sys
import time

from systems import *

def ana_bomb(params):
    entity = params[0]
    if entity["speed"] > 0:
        entity["speed"] = 0
        text_scroll(f'\n{entity["name"]} was anaesthetized! Their SPEED is now 0!\n')
    else:
        text_scroll(f'\n{entity["name"]} was too slow for the anaesthesia to take effect!\n')

def turn_based_damage(params):
    '''Attack that bases its damage on the current turn. params=[target, '$turns', damage_factor, dodgable]'''
    target = params[0]
    turn_number = params[1]
    damage_factor = params[2]
    dodgable = params[3]
    chance_num = random.randint(1, 100)
    if chance_num >= int((target['speed'] / 20) * 100) or not dodgable:
        damage = int((player['attack'] * turn_number * damage_factor)) - target['defense']
        if damage < 0: damage == 0
        target['health'] -= damage
        text_scroll(f'\n{target["name"]} took {damage} damage! They are now at {target["health"]} HP!\n')
    else:
        text_scroll(f'\n{target["name"]} dodged the attack!\n')


def change_turns(params):
    '''Changes the value of turns params=['$turns', change, '&turns']'''
    value = params[0]
    change = params[1]
    text_scroll(f'\nActive effects will now last for {-change} more turns!\n')
    return value + change

def vampire(params):
    '''Life steal. params=[target, user, divisor]
    divisor determines lifesteal (health_increment = damage // divisor)
    '''
    params = [player if par == "$player" else par for par in params]
    target = params[0]
    user = params[1]
    divisor = params[2]
    damage = random.randint(int(user['attack'] * 0.8), int(user['attack'] * 0.9)) - target['defense']
    if damage <= 0:
        text_scroll('\nThe attack did 0 damage!\n')
    else:
        text_scroll(f'\nThe attack did {damage} damage to {"you" if target == player else target["name"]}! {"You" if user == player else user["name"]} gained {int(damage // divisor)} HP due to LIFE STEAL!\n')
        target['health'] -= damage
        user['health'] += int(damage // divisor)
