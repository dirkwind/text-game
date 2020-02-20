# this is where special item functions go

import json
import math
import msvcrt
import random
import sys
import time

from systems import *

def ana_bomb(target: dict):
    '''Sets targeted entity's speed to 0 unless its speed is <= 0. params=[target]
    NOTE: cannot be used on players because they have no 'speed' value
    '''
    if target["speed"] > 0:
        target["speed"] = 0
        text_scroll(f'\n{entity["name"]} was anaesthetized! Their SPEED is now 0!\n')
    else:
        text_scroll(f'\n{entity["name"]} was too slow for the anaesthesia to take effect!\n')

def turn_based_damage(target: dict, user: dict, turn_number: int, damage_factor: float, dodgable: bool):
    '''Attack that bases its damage on the current turn. params=[target, user, '$turns', damage_factor, dodgable]'''

    if target is player and dodgable:
        text_scroll("\nGet ready to dodge!\n")
        time.sleep(1)
        chance_num = int(100 - ((quicktime_bar('f', user['speed']) / 30) * 100))
        speed = user['speed']
    else:
        chance_num = random.randint(1, 10000)/100
        speed = target['speed']

    if speed == 20:
        percent = 100
    else:
        percent = -100 * (((speed/20)-1)**2) + 100

    if chance_num <= percent or not dodgable:
        damage = int((user['attack'] * turn_number * damage_factor)) - target['defense']
        if damage <= 0: damage = 0
        target['health'] -= damage
        text_scroll(f'\n{"You" if target is player else target["name"]} took {damage} damage! {"You" if target is player else "They"} are now at {target["health"]} HP!\n')
    else:
        text_scroll(f'\n{"You" if target is player else target["name"]} dodged the attack!\n')


def change_turns(turn_number: int, change_amount: int, clarifier="&turns"):
    '''Changes the value of turns params=['$turns', change, '&turns']'''
    text_scroll(f'\nActive effects will now last for {-change_amount} more turns!\n')
    return turn_number + change_amount

def vampire(target: dict, user: dict, divisor: float):
    '''Life steal. params=[target, user, divisor]
    divisor determines lifesteal (health_increment = damage // divisor)
    '''
    damage = random.randint(int(user['attack'] * 0.8), int(user['attack'] * 0.9)) - target['defense']
    if damage <= 0:
        text_scroll('\nThe attack did 0 damage!\n')
    else:
        text_scroll(f'\nThe attack did {damage} damage to {"you" if target == player else target["name"]}! {"You" if user == player else user["name"]} gained {int(damage // divisor)} HP due to LIFE STEAL!\n')
        target['health'] -= damage
        user['health'] += int(damage // divisor)
