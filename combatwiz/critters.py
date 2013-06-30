#!/usr/bin/env python

from __future__ import division
import sys
import csv
import fileinput
import math

from pprint import pprint as pp

#--- gristle modules -------------------
import randomizer




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



