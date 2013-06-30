<p>CombatWiz is a combat simulation intended to determine the victory probabilities
of combatants using Monte Carlo simulation methods.</p>

<p>Current Status:  Allows combat between two sides, and produces simple output.</p>

<h1>Next Steps:</h1>

<ul>
<li>Creature editor</li>
<li>Graphical output</li>
<li>Map-awareness in which only one object can occupy a block</li>
<li>Missile weapons</li>
<li>Intelligent manuevering</li>
<li>Surrender, Panic, Fleeing</li>
<li>Changing weapons</li>
<li>Multiple attacks per round</li>
<li>Special effect attacks</li>
</ul>

<h1>Its objectives include:</h1>

<ul>
<li>run on linux or mac</li>
<li>web front-end</li>
<li>run multiple scenarios (each many times) to determine best tactics</li>
</ul>

<h1>Example Run:</h1>

<p>$ combatwiz_runner.py --sidea 1 3 --sideb 4 --charfile --iterations 1000 ../data/creatures.csv</p>

<pre><code>----------------------------------------------------------------
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
</code></pre>

<h1>Installation</h1>

<ul>
<li><p>Using <a href="http://www.pip-installer.org/en/latest/">pip</a> (preferred) or <a href="http://peak.telecommunity.com/DevCenter/EasyInstall">easyinstall</a>:</p>

<pre><code>~~~
$ pip install combatwiz
$ easy_install combatwiz
~~~
</code></pre></li>
<li><p>Or install manually from [pypi]:</p>

<pre><code>~~~
$ mkdir ~\Downloads
$ wget https://pypi.python.org/packages/source/d/combatwiz/combatwiz-0.12.tar.gz
$ tar -xvf easy_install combatwiz
$ cd ~\Downloads\combatwiz-*
$ python setup.py install
~~~
</code></pre></li>
</ul>

<h1>Dependencies</h1>

<ul>
<li>Python 2.6 or Python 2.7</li>
</ul>

<h1>Licensing</h1>

<ul>
<li>Gristle uses the BSD license - see the separate LICENSE file for further 
 information</li>
</ul>

<h1>Copyright</h1>

<ul>
<li>Copyright 2013 Ben Farmer, Ken Farmer</li>
</ul>
