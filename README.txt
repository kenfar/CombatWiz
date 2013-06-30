CombatWiz is a combat simulation intended to determine the victory probabilities
of combatants using Monte Carlo simulation methods.

Current Status:  Allows combat between two sides, and produces simple output.

#Next Steps:  

   * Creature editor
   * Graphical output
   * Map-awareness in which only one object can occupy a block
   * Missile weapons
   * Intelligent manuevering
   * Surrender, Panic, Fleeing
   * Changing weapons
   * Multiple attacks per round
   * Special effect attacks

#Its objectives include:

   * run on linux or mac
   * web front-end
   * run multiple scenarios (each many times) to determine best tactics

#Example Run:

$ combatwiz_runner.py --sidea 1 3 --sideb 4 --charfile --iterations 1000 ../data/creatures.csv

    ----------------------------------------------------------------
    fighter_num:        fighter1    side:           side-a    
    critter_id:         1           name:           orc                 
    hd:                 1           hp:             6     
    ac:                 8           race:           orc                 
    class:              monster     class_level:    0     
    attack_thaco:       20          attack_damage:  1-8    
    vision:             Infra-6     move:           8     
    fighter3

    ----------------------------------------------------------------
    fighter_num:        fighter3    side:           side-b    
    critter_id:         4           name:           giant               
    hd:                 0           hp:             50    
    ac:                 4           race:           giant               
    class:              monster     class_level:    10    
    attack_thaco:       6           attack_damage:  11-20  
    vision:             standard    move:           12    
    fighter2

    ----------------------------------------------------------------
    fighter_num:        fighter2    side:           side-a    
    critter_id:         3           name:           gilgion             
    hd:                 0           hp:             86    
    ac:                 -3          race:           human               
    class:              paladin     class_level:    8     
    attack_thaco:       10          attack_damage:  10-17  
    vision:             standard    move:           8     
    ----------------------------------------------------------------

    For: gilgion
    Battles:               1000
    Total Wins:            864
    Total Damage Taken:    29672
    Total Rounds Required: 5488
    Mean Rounds Required:  6.4
    Percentage of Wins:    86
    Mean PCT HP Taken:     39%

    For: giant
    Battles:               1000
    Total Wins:            136
    Total Damage Taken:    4383
    Total Rounds Required: 1058
    Mean Rounds Required:  7.8
    Percentage of Wins:    13
    Mean PCT HP Taken:     64%

    For: orc
    Battles:               1000
    Total Wins:            12
    Total Damage Taken:    0
    Total Rounds Required: 42
    Mean Rounds Required:  3.5
    Percentage of Wins:    1
    Mean PCT HP Taken:     0%



#Installation

   * Using [pip](http://www.pip-installer.org/en/latest/) (preferred) or [easyinstall](http://peak.telecommunity.com/DevCenter/EasyInstall):

        ~~~
        $ pip install combatwiz
        $ easy_install combatwiz
        ~~~

   * Or install manually from [pypi]:

        ~~~
        $ mkdir ~\Downloads
        $ wget https://pypi.python.org/packages/source/d/combatwiz/combatwiz-0.12.tar.gz
        $ tar -xvf easy_install combatwiz
        $ cd ~\Downloads\combatwiz-*
        $ python setup.py install
        ~~~
      

#Dependencies

   * Python 2.6 or Python 2.7



#Licensing

   * Gristle uses the BSD license - see the separate LICENSE file for further 
     information


#Copyright

   * Copyright 2013 Ben Farmer, Ken Farmer

