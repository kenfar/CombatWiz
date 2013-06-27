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

<p>$ combatwiz_runner.py --charid1 3 --charid2 2 --charid3 4 --iterations 1000 --charfile data/characters.csv</p>

<pre><code>char1
----------------------------------------------------------------
charid:             char1       side:             side-2    
critid:             2           name:           orc_chieftain       
hd:                 2           hp:               13    
ac:                 7           race:             orc                 
class1:             monster    class1_level:       0     
attack1_thaco:      18         attack1_damage:   2-9    
vision:             Infra-6    move:             12    

char3
----------------------------------------------------------------
charid:             char3       side:             side-2    
critid:             4           name:           giant               
hd:                 0           hp:               50    
ac:                 4           race:             giant               
class1:             monster    class1_level:       10    
attack1_thaco:      6          attack1_damage:   11-20  
vision:             standard    move:             12    

char2
----------------------------------------------------------------
charid:             char2       side:             side-1    
critid:             3           name:           paladin
hd:                 0           hp:               86    
ac:                 -3          race:             human               
class1:             paladin    class1_level:       8     
attack1_thaco:      10         attack1_damage:   10-17  
vision:             standard    move:             8     
----------------------------------------------------------------

For: paladin
Games:                 1000
Total Wins:            740
Total Damage Taken:    31247
Total Rounds Required: 4995
Mean Rounds Required:  6.8
Percentage of Wins:    74
Mean PCT HP Taken:     49%

For: orc_chieftain
Games:                 1000
Total Wins:            7
Total Damage Taken:    10
Total Rounds Required: 45
Mean Rounds Required:  6.4
Percentage of Wins:    0
Mean PCT HP Taken:     11%

For: giant
Games:                 1000
Total Wins:            260
Total Damage Taken:    6884
Total Rounds Required: 2069
Mean Rounds Required:  8.0
Percentage of Wins:    26
Mean PCT HP Taken:     52%
</code></pre>

<h1>Installation</h1>

<ul>
<li><p>Using <a href="http://www.pip-installer.org/en/latest/">pip</a> (preferred) or <a href="http://peak.telecommunity.com/DevCenter/EasyInstall">easyinstall</a>:</p>

<p>~~~
   TBD
   ~~~</p></li>
<li><p>Or install manually from [pypi]:</p>

<p>~~~
   TBD
   ~~~</p></li>
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
