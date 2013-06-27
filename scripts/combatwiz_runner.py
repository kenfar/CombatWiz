#!/usr/bin/env python

from __future__ import division
import sys
import optparse
import csv
import fileinput
import math
import random
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
    (opts, args) = get_opts_and_args()

    my_simmer = Simulator(opts.iterations, opts.charfile, opts.verbose, opts.charid1,
                          opts.charid2, opts.charid3)
    my_simmer.run_all_games()
    my_simmer.analysis()

    return 0



class Simulator(object):

    def __init__(self, games, charfile, verbose, *charids):
        self.games           = games
        self.verbose         = verbose
        self.charids         = []
        self.critter_results = []
        self.char_sum        = {}
        for charid in charids:
            if charid is not None:
                self.charids.append(int(charid))
        self.charfile     = charfile
        self.game_results = []

    def run_all_games(self):
        print
        for game in xrange(self.games):
            if self.verbose:
                print
                print '==== GAME: %d ========================================' % game
            else:
                if game % 10 == 0:
                    print '.',
            my_creatures = CreatureManager(self.charfile, self.charids)
            if game == 0:
                my_creatures.print_creature_summary()
            one_arena     = ArenaManager(my_creatures, self.verbose)
            self.game_results.append(one_arena.runner())

    def analysis(self):
        """ input:  results are a tuple consisting of rounds followed by a
                    creatures dictionary.
        """
        for game in self.game_results:
            rounds    = game[0]
            creatures = game[1]
            for key in creatures:
                if creatures[key].curr_hp > 0:
                    winner_name = creatures[key].name
                    self.critter_results.append((creatures[key].name,
                                            creatures[key].critid,
                                            int(rounds),
                                            creatures[key].hp,
                                            creatures[key].curr_hp))

        self._create_char_summary()

        print
        for char in self.char_sum:
            if 'critid' in self.char_sum[char]:
                print
                print 'For: %s' % self.char_sum[char]['name']
                print 'Games:                 %d' % self.games
                print 'Total Wins:            %d' % self.char_sum[char]['tot_wins']
                print 'Total Damage Taken:    %d' % self.char_sum[char]['tot_damage']
                print 'Total Rounds Required: %d' % self.char_sum[char]['tot_rounds']
                print 'Mean Rounds Required:  %2.1f' % (self.char_sum[char]['tot_rounds'] /
                self.char_sum[char]['tot_wins'])
                print 'Percentage of Wins:    %d' % ((self.char_sum[char]['tot_wins'] / self.games) * 100)
                print 'Mean PCT HP Taken:     %d%%' % ((self.char_sum[char]['tot_damage'] /
                  self.char_sum[char]['tot_wins']) / self.char_sum[char]['hp'] * 100)


        #print sum(critter_results[1])
        #print sum(critter_results[1]) / self.iterations


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
                self.char_sum[crit[0]]['critid']      = crit[1]
                self.char_sum[crit[0]]['hp']          = crit[3]
                self.char_sum[crit[0]]['tot_rounds']  = crit[2]
                self.char_sum[crit[0]]['tot_wins']    = 1
                self.char_sum[crit[0]]['tot_damage']  = crit[3] - crit[4]




def get_opts_and_args():
    """ gets opts & args and returns them
        Input:
            - command line args & options
        Output:
            - opts dictionary
            - args dictionary
    """
    use = ("%prog is used to ... "
           " \n"
           "   %prog [file] [misc options]")
    parser = optparse.OptionParser(usage = use)

    parser.add_option('--charid1',
           help='Specifies the id for the first character')
    parser.add_option('--charid2',
           help='Specifies the id for the second character')
    parser.add_option('--charid3',
           help='Specifies the id for the third character')
    parser.add_option('--charfile',
           default='characters.csv',
           help='Specifies the file with character details')
    parser.add_option('--iterations',
           default=1,
           type=int,
           help='Specifies the number of fights to simulate')
    parser.add_option('--verbose',
           action='store_true',
           default=False,
           help='Specifies whether or not to print details.  Default is False.')

    (opts, args) = parser.parse_args()

    if opts.charid1 is None or opts.charid2 is None:
        parser.error('charid1 & charid2 must be provided')

    return opts, args






class CreatureManager(object):
    def __init__(self, charfile, charids):
        self.creatures        = {}
        self.charids          = charids
        self.load_creatures(charfile)
        #print 'self.creatures: '
        #print self.creatures
        #print 'self.charids: '
        #print self.charids


    def is_one_side_dead(self):
        """ Only mildly useful - since creatures are currently provided
            to Arena class as a dictionary of creatures rather than as a
            class of classes.  Also - a complete copy of a function inside
            the Arena class.
        """
        side_1_alive = False
        side_2_alive = False
        for key in self.creatures.keys():
            if self.creatures[key].side == 'side-1':
                if self.creatures[key].curr_hp >= 1:
                    side_1_alive = True
            else:
                if self.creatures[key].curr_hp >= 1:
                    side_2_alive = True

        return (not side_1_alive or not side_2_alive)


    def load_creatures(self, charfile):
        """ Reads from file, transforms data, inserts into dict.
            Input:
                    - charfile - the name of the character file.
            Transforms:
                    - adds a side to each creature record
                    - adds a incrementing suffix if the same creature
                      is in combat more than once.
        """
        charnum = 1
        for record in csv.reader(fileinput.input(charfile)):
            orig_record = list(record)
            try:
                if not record:
                    break
                repeat_count = self.charids.count(int(record[0])) 
                if record[4] == 'monster':
                    record.append('side-2')
                else:
                    record.append('side-1')
                while repeat_count:
                    if self.charids.count(int(record[0])) > 1:
                        record[1] = orig_record[1] + '-' + str(repeat_count)
                    self.creatures['char%d' % charnum] = OneCreature(record)
                    charnum += 1
                    repeat_count -= 1
            except ValueError:
                pass # skipping over header row or any empty rows


    def print_creature_summary(self):

        print
        for key in self.creatures.keys():
            print key
            print
            print '----------------------------------------------------------------'
            print 'charid:             %-8.8s    side:             %-10.10s'  %  \
                (key, self.creatures[key].side)
            print 'critid:             %-4.4s        name:           %-20.20s'  %  \
                (self.creatures[key].critid, self.creatures[key].name)
            print 'hd:                 %-4.4s        hp:               %-4.4s  '  %  \
                (self.creatures[key].hd, self.creatures[key].hp)
            print 'ac:                 %-4.4s        race:             %-20.20s'  %  \
                (self.creatures[key].ac, self.creatures[key].race)
            print 'class1:             %-10.10s class1_level:       %-4.4s  '  %  \
                (self.creatures[key].class1, self.creatures[key].class1_level)
            print 'attack1_thaco:      %-4.4s       attack1_damage:   %-5.5s  '  %  \
                (self.creatures[key].attack1_thaco, self.creatures[key].attack1_damage)
            print 'vision:             %-4.10s    move:             %-4.4s  '  %  \
                (self.creatures[key].vision, self.creatures[key].move)
        print '----------------------------------------------------------------'

    def __repr__(self):
        result = 'my creatures:\n'
        for key in self.creatures.keys():
            print 'charid:    %-8.8s\n' % key
            result += 'charid:    %-8.8s\n' % key
            result += 'id:        %-4.4s        config:  %-20.20s\n'  %  \
                (self.creatures[key].id, self.creatures[key].name)
            result += 'hd:        %-4.4s        hp:      %-4.4s \n'  %  \
                (self.creatures[key].hd, self.creatures[key].hp)
        return result




class OneCreature(object):
    def __init__(self, creature_record):
        self.critid           = string2int(creature_record[0])
        self.hd               = string2int(creature_record[6])
        self.ac               = string2int(creature_record[8])
        self.race             = creature_record[3]
        self.class1           = creature_record[4]
        self.name             = creature_record[1]
        self.config           = creature_record[2]
        self.hp               = string2int(creature_record[7])
        self.attack1_distance = 2
        self.attack1_thaco    = string2int(creature_record[9])
        self.attack1_damage   = creature_record[10]
        self.class1_level     = string2int(creature_record[5])
        self.vision           = creature_record[11]
        self.move             = string2int(creature_record[12])
        self.move_this_seg    = False
        self.attack_this_seg  = False
        if self.hp == 0:
            self.hp = randomizer.roll_dice(8, self.hd)
        self.curr_hp          = self.hp
        self.curr_loc         = None
        self.side             = creature_record[13]

    def change_loc(self, new_loc):
        if new_loc != self.curr_loc:
            self.move_this_seg = True
            self.curr_loc      = new_loc
        else:
            self.move_this_seg = False

    def in_range(self, enemy_loc):
        if get_distance(self.curr_loc, enemy_loc) <= self.attack1_distance:
            return True
        else:
            return False






class ArenaManager(object):
    def __init__(self, creatures, verbose):
       self.length    = 100
       self.width     = 100
       self.verbose   = verbose
       self.creatures = creatures.creatures
       self.rounds    = 0

    def my_print(self, val=''):
        if self.verbose:
            print val

    def runner(self):
        # assign initial creature locations
        #print creatures
        self.creatures['char1'].curr_loc = [0.00, 0.00]
        self.creatures['char2'].curr_loc = [0.00, self.width]
        self.creatures['char3'].curr_loc = [self.length, self.width]

        for round in range(1, 101):
            self.rounds += 1
            self.my_print()
            self.my_print('------------round: %d---------------' % round)
            for seg in range(1, 11):
                self.my_print('   ------------segment: %d---------------' % seg)
                for key in self.creatures.keys():
                    if self.creatures[key].curr_hp > 0:
                        enemy_key = self.get_enemy_key(key)
                        enemy_loc = self.creatures[enemy_key].curr_loc
                        for move in range(1, (self.creatures[key].move + 1) ):
                            self.creatures[key].change_loc(self.move_subject(self.creatures[key].curr_loc, enemy_loc))
                        if self.creatures[key].move_this_seg:
                            self.my_print('         %-20.20s moved to location: %s' % \
                                        (self.creatures[key].name,
                                        self.creatures[key].curr_loc))
                        if not self.creatures[key].move_this_seg:
                            if self.creatures[key].in_range(enemy_loc):
                                self.attack(key, enemy_key)
                        if self.is_one_side_dead():
                            break
                if self.is_one_side_dead():
                    break
            if self.is_one_side_dead():
                break
        return (self.rounds, self.creatures)


    def is_one_side_dead(self):
        side_1_alive = False
        side_2_alive = False
        for key in self.creatures.keys():
            if self.creatures[key].side == 'side-1':
                if self.creatures[key].curr_hp >= 1:
                    side_1_alive = True
            else:
                if self.creatures[key].curr_hp >= 1:
                    side_2_alive = True

        return (not side_1_alive or not side_2_alive)


    def move_subject(self, subject_loc, enemy_loc):
        """ returns new location
        """
        results = {}
        for yadj in range(-1,2):    # actual values -1, 0, 1
            for xadj in range(-1,2):   # actual values -1, 0, 1
                dist = get_distance(subject_loc, enemy_loc, yadj, xadj)
                key  = (yadj, xadj)
                results[key] = dist
        best_key_value = 9999999
        best_key       = None
        for key in results.keys():
            if results[key] < best_key_value:
                best_key = key
                best_key_value = results[key]
        new_loc = (subject_loc[0] + best_key[0],
                subject_loc[1] + best_key[1])
        return new_loc


    def get_enemy_key(self, subject_key):
        """ Needs a test-harness.
        """
        for key in self.creatures.keys():
            if key != subject_key:
                if self.creatures[subject_key].side != self.creatures[key].side:
                    if self.creatures[key].curr_hp > 0:
                        return key
        raise ValueError, 'no enemy key found'


    def attack(self, subject_key, enemy_key):
        attacks_per_round  = 1.00
        segments_per_round = 10.00
        if random.random() > (attacks_per_round / segments_per_round):
            self.my_print('        %s fails to get an attack opportunity' %
                          self.creatures[subject_key].name)
            return

        roll   = randomizer.roll_dice(20, 1)
        ac_hit = self.creatures[subject_key].attack1_thaco - roll
        if ac_hit <= self.creatures[enemy_key].ac:
            damage = randomizer.roll_range(self.creatures[subject_key].attack1_damage)
            self.creatures[enemy_key].curr_hp -= damage
            self.my_print('        %s hits %s for %d damage with a to-hit roll of %d' % \
                  (self.creatures[subject_key].name,
                   self.creatures[enemy_key].name,
                   damage,
                   roll ))
            if self.creatures[enemy_key].curr_hp < 1:
                self.my_print('        %s dies!' % self.creatures[enemy_key].name)
        else:
            self.my_print('        %s misses %s with a to-hit roll of %d' % \
                           (self.creatures[subject_key].name,
                            self.creatures[enemy_key].name, roll))



def get_distance(loc_a, loc_b, xadj=0, yadj=0):
    """ inputs:
        - loc_a coordinates [positive x, positive y]
        - loc_b coordinates [positive x, positive y]
        - x ajustment
        - y ajustment
        outputs:
        - distance - float
    """
    assert(loc_a[0] >= 0)
    assert(loc_a[1] >= 0)
    assert(loc_b[0] >= 0)
    assert(loc_b[1] >= 0)

    xsub = 0
    ysub = 1
    dist = math.sqrt((loc_a[xsub] - loc_b[xsub] + xadj)**2 
                    + (loc_a[ysub] - loc_b[ysub] + yadj)**2)
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



if __name__ == '__main__':
    sys.exit(main())

