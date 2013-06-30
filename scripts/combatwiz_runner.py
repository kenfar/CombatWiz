#!/usr/bin/env python

from __future__ import division
import sys
import csv
import fileinput
import math
import random

import argparse
from pprint import pprint as pp

#--- gristle modules -------------------
sys.path.append('../')     # allows running from project structure
sys.path.append('../../')  # allows running from project structure
import combatwiz.randomizer   as randomizer
import combatwiz.critters     as critters
import pdb



def main():
    """ runs all processes:
            - gets opts & args
            - analyzes file to determine csv characteristics unless data is 
              provided via stdin
            - runs each input record through process_cols to get output
            - writes records
    """
    args = get_args()

    my_simmer = Simulator(args.battles, args.charfile, args.verbose,
                          args.critters, args.sidea, args.sideb)
    my_simmer.run_all_battles()
    my_simmer.analysis()

    return 0



class Simulator(object):

    def __init__(self, battles, charfile, verbose, critters, sidea, sideb):
        self.battles         = battles
        self.verbose         = verbose
        self.critters        = critters
        self.critters_sidea  = sidea
        self.critters_sideb  = sideb
        self.critter_results = []
        self.char_sum        = {}
        self.charfile        = charfile
        self.battle_results  = []

    def run_all_battles(self):
        for battle in xrange(self.battles):
            if self.verbose:
                print
                print '==== Battle: %d ========================================' % battle
            my_creatures = critters.CreatureManager(self.charfile, self.critters,
                                           self.critters_sidea, self.critters_sideb)
            if battle == 0:
                my_creatures.print_creature_summary()
            one_arena     = ArenaManager(my_creatures, self.verbose)
            self.battle_results.append(one_arena.runner())

    def analysis(self):
        """ input:  results are a tuple consisting of rounds followed by a
                    creatures dictionary.
        """
        for battle in self.battle_results:
            rounds    = battle[0]
            creatures = battle[1]
            for key in creatures:
                if creatures[key].curr_hp > 0:
                    winner_name = creatures[key].name
                    self.critter_results.append((creatures[key].name,
                                            creatures[key].critter_id,
                                            int(rounds),
                                            creatures[key].hp,
                                            creatures[key].curr_hp))

        self._create_char_summary()

        print
        for char in self.char_sum:
            if 'critter_id' in self.char_sum[char]:
                print
                print 'For: %s' % self.char_sum[char]['name']
                print 'Battles:               %d' % self.battles
                print 'Total Wins:            %d' % self.char_sum[char]['tot_wins']
                print 'Total Damage Taken:    %d' % self.char_sum[char]['tot_damage']
                print 'Total Rounds Required: %d' % self.char_sum[char]['tot_rounds']
                print 'Mean Rounds Required:  %2.1f' % (self.char_sum[char]['tot_rounds'] /
                self.char_sum[char]['tot_wins'])
                print 'Percentage of Wins:    %d' %  \
                ((self.char_sum[char]['tot_wins'] / self.battles) * 100)
                print 'Mean PCT HP Taken:     %d%%' % ((self.char_sum[char]['tot_damage'] /
                  self.char_sum[char]['tot_wins']) / self.char_sum[char]['hp'] * 100)


        #print sum(critter_results[1])
        #print sum(critter_results[1]) / self.battles


    def _create_char_summary(self):
        """ Creates summary dict of creatures - using their name as the key.
        """
        for crit in self.critter_results:
            try:
                self.char_sum[crit[0]]['tot_rounds'] += crit[2]
                self.char_sum[crit[0]]['tot_wins']   += 1
                self.char_sum[crit[0]]['tot_damage'] += crit[3] - crit[4]
            except KeyError:
                self.char_sum[crit[0]]                = {}
                self.char_sum[crit[0]]['name']        = crit[0]
                self.char_sum[crit[0]]['critter_id']  = crit[1]
                self.char_sum[crit[0]]['hp']          = crit[3]
                self.char_sum[crit[0]]['tot_rounds']  = crit[2]
                self.char_sum[crit[0]]['tot_wins']    = 1
                self.char_sum[crit[0]]['tot_damage']  = crit[3] - crit[4]




def get_args():
    """ gets args and returns them
        Input:
            - command line args & options
        Output:
            - args namespace
    """
    parser = argparse.ArgumentParser(description='Simulate combat between critters')

    parser.add_argument('critters',
        nargs='*',
        type=int,
        default=[],
        help='Specifies the critters to fight by id. All monsters will be on Side-A, all humanoids on Side-B.')
    parser.add_argument('--sidea',
        nargs='*',
        type=int,
        default=[],
        help='explicitly list critters on Side-A')
    parser.add_argument('--sideb',
        nargs='*',
        type=int,
        default=[],
        help='Explicitly list critters on Side-B')
    parser.add_argument('--charfile',
        default='~/.config/combatwiz/creatures.csv',
        help='Specifies the file with character details')
    parser.add_argument('--battles',
        default=1,
        type=int,
        help='Specifies the number of battles to run')
    parser.add_argument('--verbose',
        action='store_true',
        default=False,
        help='Specifies whether or not to print details.  Default is False.')

    args = parser.parse_args()

    if (not args.critters and not args.sidea and not args.sideb):
        parser.error('Please provide critter ids for the battle')

    if args.critters and len(args.critters) == 1:
        parser.error('provide more than one critter to fight')

    if args.critters and (args.sidea or args.sideb):
        parser.error('provide either critters argument or both side options')

    if (args.sidea and not args.sideb) or (args.sideb and not args.sidea):
        parser.error('when specifying critters by side - provide both sides')

    return args






class ArenaManager(object):

    def __init__(self, creature_manager, verbose):
       self.x_max        = 100
       self.y_max        = 100
       self.verbose      = verbose
       self.creature_man = creature_manager
       self.creatures    = creature_manager.creatures
       self.rounds       = 0
       self.assign_creature_starting_locations()


    def my_print(self, val=''):
        if self.verbose:
            print val


    def assign_creature_starting_locations(self):
        # should be randomly distributed
        self.creatures['fighter1'].curr_loc     = [0, 0]
        self.creatures['fighter2'].curr_loc     = [self.x_max, self.y_max]
        if 'fighter3' in self.creatures:
            self.creatures['fighter3'].curr_loc = [0, self.y_max]
        if 'fighter4' in self.creatures:
            self.creatures['fighter4'].curr_loc = [self.x_max, 0]
        if 'fighter5' in self.creatures:
            self.creatures['fighter5'].curr_loc = [(self.x_max/2), 0]
        if 'fighter6' in self.creatures:
            self.creatures['fighter6'].curr_loc = [(self.x_max/2), self.y_max]
        if 'fighter7' in self.creatures:
            self.creatures['fighter7'].curr_loc = [0, (self.y_max/2)]
        if 'fighter8' in self.creatures:
            self.creatures['fighter8'].curr_loc = [(self.x_max), (self.y_max/2)]


    def runner(self):

        for self.curr_round in range(1, 101):
            self.rounds += 1
            self.my_print()
            self.my_print('------------round: %d---------------' % self.curr_round)
            for self.curr_seg in range(1, 11):
                self.my_print('   ------------segment: %d---------------' % self.curr_seg)
                for subject in self.creatures.keys():
                    if self.creatures[subject].curr_hp > 0:
                        enemy     = self.get_enemy(subject)
                        enemy_loc = self.creatures[enemy].curr_loc
                        self.move_subject_towards_enemy(subject, enemy)
                        if (not self.creatures[subject].moved_this_seg(self.curr_round,
                                                                   self.curr_seg)):
                            if self.creatures[subject].in_range(enemy_loc):
                                self.attack(subject, enemy)
                        if self.creature_man.is_one_side_dead():
                            break
                if self.creature_man.is_one_side_dead():
                    break
            if self.creature_man.is_one_side_dead():
                break
        return (self.rounds, self.creatures)


    def move_subject_towards_enemy(self, subject, enemy):
        enemy_loc = self.creatures[enemy].curr_loc
        for move in range(1, (self.creatures[subject].move + 1) ):
            self.creatures[subject].change_loc(self.move_subject_one_block(self.creatures[subject].curr_loc,
                                                                           enemy_loc),
                                               self.curr_round,
                                               self.curr_seg)
            #print '        %s moves to %s' % (self.creatures[subject].name, self.creatures[subject].curr_loc)
        if (self.creatures[subject].moved_this_seg(self.curr_round, self.curr_seg)):
            self.my_print('        %-20.20s moved to location: %s' % \
            (self.creatures[subject].name, self.creatures[subject].curr_loc))



    def move_subject_one_block(self, subject_loc, enemy_loc):
        """ Returns new location up to 1 block away from currrent location
            that is closer to the enemy location.

            Note that once the battle begins it will generally indicate to
            stay in the same position.
        """
        X = 0
        Y = 1

        # first get distance for all 9 movement possibilities:
        relative_moves = {}
        for xmove in range(-1, 2):
            for ymove in range(-1, 2):
                sub_loc_adj = (subject_loc[X] + xmove, subject_loc[Y] + ymove)
                if sub_loc_adj[X] < 0 or sub_loc_adj[Y] < 0:
                    relative_moves[(xmove, ymove)] = 9999 # make going off board too expensive
                else:
                    relative_moves[(xmove, ymove)] = get_distance(sub_loc_adj, enemy_loc)

        best_relative_move    = get_key_with_least_value(relative_moves)
        best_absolute_new_loc = (subject_loc[X] + best_relative_move[X],
                                 subject_loc[Y] + best_relative_move[Y])
        return best_absolute_new_loc


    def get_enemy(self, subject):
        """ Needs a test-harness.
        """
        for enemy in self.creatures.keys():
            if enemy != subject:
                if self.creatures[subject].side != self.creatures[enemy].side:
                    if self.creatures[enemy].curr_hp > 0:
                        return enemy
        raise ValueError, 'no enemy found'


    def attack(self, subject, enemy):
        attacks_per_round  = 1.00
        segments_per_round = 10.00
        if random.random() > (attacks_per_round / segments_per_round):
            self.my_print('        %s fails to get an attack opportunity against %s' % \
                          (self.creatures[subject].name, self.creatures[enemy].name))
            return

        roll   = randomizer.roll_dice(20, 1)
        ac_hit = self.creatures[subject].attack_thaco - roll
        if ac_hit <= self.creatures[enemy].ac:
            damage = randomizer.roll_range(self.creatures[subject].attack_damage)
            self.creatures[enemy].curr_hp -= damage
            self.my_print('        %s hits %s for %d damage with a to-hit roll of %d' % \
                  (self.creatures[subject].name, self.creatures[enemy].name, damage, roll ))
            if self.creatures[enemy].curr_hp < 1:
                self.my_print('        %s dies!' % self.creatures[enemy].name)
        else:
            self.my_print('        %s misses %s with a to-hit roll of %d' % \
                (self.creatures[subject].name, self.creatures[enemy].name, roll))



def get_distance(loc_a, loc_b):
    """ inputs:
        - loc_a coordinates [positive x, positive y]
        - loc_b coordinates [positive x, positive y]
        outputs:
        - distance - float
    """
    X = 0
    Y = 1
    assert(loc_a[X] >= 0)
    assert(loc_a[Y] >= 0)
    assert(loc_b[X] >= 0)
    assert(loc_b[Y] >= 0)

    dist = math.sqrt((loc_a[X] - loc_b[X])**2 
                   + (loc_a[Y] - loc_b[Y])**2)
    return dist



def string2int(val):
    """ needs test harness
    """
    if val == '':
        return 0
    else:
        try:
           return int(val)
        except TypeError:
           return 0


def get_key_with_least_value(source_dict):
    least_key_value = 9999999
    least_key       = None
    for key in source_dict.keys():
        if source_dict[key] < least_key_value:
            least_key       = key
            least_key_value = source_dict[key]
    return least_key


if __name__ == '__main__':
    sys.exit(main())

