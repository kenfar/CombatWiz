#!/usr/bin/env python
from __future__ import division
import sys
import random
import pdb
from pprint import pprint as pp


def main():
    """ Primarily used for testing
    """
    die_type, die_number, die_adj = get_user_input()

    print roll_dice(die_type, die_number, die_adj)


def _die_range_calc(die_type, point_min, point_max):
    """ Returns the largest number of dice of a given type
        and any adjustments necessary to provide a range
        that matches the min and max points given.
        Inputs:
            -
        Outputs:
    """
    #pdb.set_trace()
    if point_max < die_type:
        return None, None
    max_dice = 0
    point_range = point_max - point_min + 1
    for i in range(1, point_range):
        if (i * die_type - i) <= point_range:
            if point_max - (die_type * i) < 0:
                break  # disallow combos with negative adjustments
            else:
                max_dice = i
        else:
            break
    max_adj = point_max - (die_type * max_dice)
    min_adj = point_min - (1 * max_dice)
    if min_adj != max_adj:
        return None, None   # range not compatible with this die
    return (max_dice, max_adj)


def _die_combo_chooser(dice):
    """ Inputs:
        - dice - a dictionary of 2-element lists:
            [die_type] - the key, and number of side of die
            [number of dice] - first element in list
            [adj] - second element in list
        Assumptions
        - fewer larger dice is better than more smaller ones
        Issues - this should also be an assumption, but in reality
        we have few times when there's more than 1 combo that works.
        - smaller adjustments are better than larger ones
    """
    #----- figure out which die combo is best
    best_die     = 9999
    best_die_adj = 9999
    for die in dice.keys():
        if dice[die][0]:
            if dice[die][1] < best_die_adj:
                best_die_adj = dice[die][1]
                best_die     = die
    if best_die == 9999:
        return None, None, None
    else:
        num =  dice[best_die][0]
        adj =  dice[best_die][1]
        return (best_die, num, adj)


def transform_range_to_dice(point_range):
    """ Inputs:
           - ex:  '1-4'
           - ex:  '3-8'
           - ex:  '11-20'
        Outputs (corresponding to inputs above):
           - ex:  (4, 1, 0)
           - ex:  (6, 1, 2)
           - ex:  (10, 1, 10)
        Validation
           - if there's no validation combination of dice
             and adjustments it'll return None, None, None
    """
    #----- set up initial values
    dice = {4:[None, None],
            6:[None, None],
            8:[None, None],
            10:[None, None],
            12:[None, None],
            20:[None, None]}

    a, b = point_range.split('-')
    point_min       = int(a)
    point_max       = int(b)

    #----- determine values for each die
    for die_type in dice.keys():
        (num, adj) = _die_range_calc(die_type, point_min, point_max)
        if num:  # skip invalid results
            dice[die_type] = [num, adj]

    #----- figure out which die is best
    (best_die, num, adj) = _die_combo_chooser(dice)

    return (best_die, num, adj)



def roll_range(range):
    (die, num, adj) = transform_range_to_dice(range)
    return roll_dice(die, num, adj)


def roll_dice(die_type, number_of_dice, adjustment=0):

    # validate all input
    assert(int(die_type) > 0)
    assert(int(number_of_dice) > 0)
    assert(30 > int(adjustment) > -30)

    total= 0
    for die in range(number_of_dice):
        total += random.randrange(1, die_type+1)

    return total + int(adjustment)


def get_user_input():

   try:
       die_type = int(raw_input('Enter the die type: '))
   except ValueError:
       print 'Please provide a number from 1-100 for the die type'
       sys.exit(0)

   try:
       die_number = int(raw_input('Enter the amount of dice: '))
   except ValueError:
       print 'Please provide a number from 1-100 for the amount of dice'
       sys.exit(0)

   try:
       die_adj = int(raw_input('Enter the adjustment for the die: '))
   except ValueError:
       print 'Please provide a number from -30-30 for the adjustment'
       sys.exit(0)

   return die_type, die_number, die_adj


if __name__ == '__main__':
   sys.exit(main())
