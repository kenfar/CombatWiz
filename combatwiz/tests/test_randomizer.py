#!/usr/bin/env python

import sys
import unittest
import pytest

sys.path.append('../')
import randomizer as mod


class TestDieRangeCalc(object):

    def test_1die_0adj(self):
        assert(mod._die_range_calc(4, 1, 4)  == (1, 0))

    def test_multidie_0adj(self):
        assert(mod._die_range_calc(4, 2, 8)  == (2, 0))
        assert(mod._die_range_calc(4, 3, 12) == (3, 0))

    def test_1die_someadj(self):
        assert(mod._die_range_calc(4, 2, 5)  == (1, 1))
        assert(mod._die_range_calc(6, 2, 7)  == (1, 1))

    def test_multidie_someadj(self):
        assert(mod._die_range_calc(4, 4, 10) == (2, 2))
        assert(mod._die_range_calc(4, 6, 15) == (3, 3))
        assert(mod._die_range_calc(6, 5, 15) == (2, 3))

    def test_invalid_max_less_than_die(self):
        assert(mod._die_range_calc(4, 1, 3) == (None, None))

    def test_invalid_range_compatible(self):
        assert(mod._die_range_calc(4, 1, 5) == (None, None))

    def test_invalid_max_less_than_min(self):
        assert(mod._die_range_calc(4, 5, 4) == (None, None))



class TestDieComboChooser(object):

    def test_one_qualified_die(self):
        dice = {4:[1, 0],
                6:[None, None]}
        assert(mod._die_combo_chooser(dice)  == (4, 1, 0))

    def test_two_qualified_dice(self):
        # assume 3-12
        dice = {4:[3, 0],
                10:[1, 2]}
        assert(mod._die_combo_chooser(dice)  == (4, 3, 0))

    def test_no_qualified_dice(self):
        # assume 5-4 (invalid) 
        dice = {4:[None, None],
                6:[None, None]}
        assert(mod._die_combo_chooser(dice)  == (None, None, None))



class TestTransformRangeToDice(object):

    def setup_method(self, method):
        pass

    def test_1die_0adj(self):
        assert(mod.transform_range_to_dice('1-4')  == (4, 1, 0))
        assert(mod.transform_range_to_dice('1-10') == (10, 1, 0))

    def test_1die_1adj(self):
        assert(mod.transform_range_to_dice('2-5')  == (4, 1, 1))

    def test_manydie_someadj(self):
        assert(mod.transform_range_to_dice('3-8')  == (6, 1, 2))
        assert(mod.transform_range_to_dice('4-10')  == (4, 2, 2))

    def test_no_qualified_combo(self):
        assert(mod.transform_range_to_dice('8-3')  == (None, None, None))



class Test_roll_dice(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_bad_input(self):
        self.assertRaises(ValueError, mod.roll_dice, 'a',3,3)
        self.assertRaises(ValueError, mod.roll_dice, 8,'b',3)
        self.assertRaises(ValueError, mod.roll_dice, 8,3,'c')
        self.assertRaises(ValueError, mod.roll_dice, 2.5,3,3)
        self.assertRaises(AssertionError, mod.roll_dice, -8,3,3)
        self.assertRaises(AssertionError, mod.roll_dice, 8,-3,3)
        self.assertRaises(AssertionError, mod.roll_dice,  0,3,3 )
        self.assertRaises(AssertionError, mod.roll_dice, 8,0,3 )
 
        # bad input that isn't enforced: 
        # self.assertRaises(ValueError, mod.roll_dice, 8,2.5,3)
        # self.assertRaises(ValueError, mod.roll_dice, 8,3,2.5)

    def test_happy_path(self):
        assert(mod.roll_dice(8,3,-3) >= 0)
        assert(mod.roll_dice(8,3,-3) <= 21)

    def test_average(self):
        results = []
        for i in range(10000):
            results.append(float(mod.roll_dice(8,1,0)))
        average = sum(results) / len(results)
        print 'average: %f ' % average
        print 'min:     %d ' % min(results)
        print 'max:     %d ' % max(results)

if __name__ == "__main__":
    unittest.main()
