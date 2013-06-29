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
            my_creatures = CreatureManager(self.charfile, self.critters,
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




class CreatureManager(object):
    def __init__(self, charfile, critters, critters_sidea, critters_sideb):
        self.creatures        = {}
        self.critters         = critters
        self.critters_sidea   = critters_sidea
        self.critters_sideb   = critters_sideb
        self.load_creatures(charfile)


    def is_one_side_dead(self):
        """ output:
               - True if the members of either side are completely dead
               - False otherwise
        """
        side_a_dead = True
        side_b_dead = True
        for key in self.creatures.keys():
            if self.creatures[key].side == 'side-a':
                if self.creatures[key].curr_hp >= 1:
                    side_a_dead = False
            else:
                if self.creatures[key].curr_hp >= 1:
                    side_b_dead = False
        return (side_a_dead or side_b_dead)


    def _get_side_and_count(self, critter_id, critter_class):
        side  = None
        count = 0
        assert(int(critter_id))
        if int(critter_id) in self.critters_sidea:
            count = self.critters_sidea.count(int(critter_id))
            side  = 'side-a'
        elif int(critter_id) in self.critters_sideb:
            count = self.critters_sideb.count(int(critter_id))
            side  = 'side-b'
        elif int(critter_id) in self.critters:
            count = self.critters.count(int(critter_id))
            if critter_class == 'monster':
                side  = 'side-b'
            else:
                side  = 'side-a'

        return (side, count)


    def load_creatures(self, charfile):
        """ Reads from file, transforms data, inserts into dict.
            Input:
                    - charfile - the name of the character file.
            Transforms:
                    - adds a side to each creature record
                    - adds a incrementing suffix if the same creature
                      is in combat more than once.
        """
        fighter_num = 1
        for record in csv.reader(fileinput.input(charfile)):
            orig_record = list(record)
            try:
                if record[0] in ['id', '', ' ']:
                    continue  # header-record
                if not record:
                    break
                (side, count) = self._get_side_and_count(record[0], record[4])
                record.append(side)
                while count:
                    if self.critters.count(int(record[0])) > 1:
                        record[1] = orig_record[1] + '-' + str(count)
                    self.creatures['fighter%d' % fighter_num] = OneCreature(record)
                    fighter_num += 1
                    count       -= 1
            except ValueError:
                pass # skipping over header row or any empty rows


    def print_creature_summary(self):

        for key in self.creatures.keys():
            print key
            print
            print '----------------------------------------------------------------'
            print 'fighter_num:        %-8.8s    side:           %-10.10s'  %  \
                (key, self.creatures[key].side)
            print 'critter_id:         %-4.4s        name:           %-20.20s'  %  \
                (self.creatures[key].critter_id, self.creatures[key].name)
            print 'hd:                 %-4.4s        hp:             %-4.4s  '  %  \
                (self.creatures[key].hd, self.creatures[key].hp)
            print 'ac:                 %-4.4s        race:           %-20.20s'  %  \
                (self.creatures[key].ac, self.creatures[key].race)
            print 'class:              %-10.10s  class_level:    %-4.4s  '  %  \
                (self.creatures[key].critter_class,  self.creatures[key].class_level)
            print 'attack_thaco:       %-4.4s        attack_damage:  %-5.5s  '  %  \
                (self.creatures[key].attack_thaco, self.creatures[key].attack_damage)
            print 'vision:             %-10.10s  move:           %-4.4s  '  %  \
                (self.creatures[key].vision, self.creatures[key].move)
        print '----------------------------------------------------------------'


    def __repr__(self):
        result = 'my creatures:\n'
        for key in self.creatures.keys():
            result += 'critter_id: %-8.8s       side:    %-8.8s  \n' % (key, self.creatures[key].side)
            result += 'id:        %-4.4s        config:  %-20.20s\n' % (self.creatures[key].critter_id, self.creatures[key].name)
            result += 'hd:        %-4.4s        hp:      %-4.4s  \n' % (self.creatures[key].hd, self.creatures[key].hp)
        return result




class OneCreature(object):
    def __init__(self, creature_record):
        self.critter_id       = string2int(creature_record[0])
        self.hd               = string2int(creature_record[6])
        self.ac               = string2int(creature_record[8])
        self.race             = creature_record[3]
        self.critter_class    = creature_record[4]
        self.name             = creature_record[1]
        self.config           = creature_record[2]
        self.hp               = string2int(creature_record[7])
        self.attack_distance  = 2
        self.attack_thaco     = string2int(creature_record[9])
        self.attack_damage    = creature_record[10]
        self.class_level      = string2int(creature_record[5])
        self.vision           = creature_record[11]
        self.move             = string2int(creature_record[12])
        self.attack_this_seg  = False
        if self.hp == 0:
            self.hp = randomizer.roll_dice(8, self.hd)
        self.curr_hp          = self.hp
        self.curr_loc         = None
        self.side             = creature_record[13]
        self.last_round       = None # last round that creature moved
        self.last_seg         = None # last seg that creature moved

    def moved_this_seg(self, curr_round, curr_seg):
        if (self.last_round == curr_round
        and self.last_seg == curr_seg):
            return True
        else:
            return False


    def change_loc(self, new_loc, curr_round, curr_seg):
        if new_loc != self.curr_loc:
            self.last_round    = curr_round
            self.last_seg      = curr_seg
            self.curr_loc      = new_loc

    def in_range(self, enemy_loc):
        #print '%s, %s, %s' % (self.curr_loc, enemy_loc, get_distance(self.curr_loc, enemy_loc))
        if get_distance(self.curr_loc, enemy_loc) <= self.attack_distance:
            return True
        else:
            return False

    def __repr__(self):
        result  = 'critter_id: %-8.8s       side:    %-8.8s  \n' % (self.critter_id, self.side)
        result += 'id:        %-4.4s        config:  %-20.20s\n' % (self.critter_id, self.name)
        result += 'hd:        %-4.4s        hp:      %-4.4s  \n' % (self.hd, self.hp)
        return result







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

