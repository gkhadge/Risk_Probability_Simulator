## Risk_Simulator.py
## 6/14/2016
## Author: Gourav Khadge
## The program simulates a conquest in Risk through
## multiple territories, leaving 1's behind
##  initial_offense: Starting troops on first territory
##  initial_scenario: Territories you aim to fight through
from __future__ import division
import random
import numpy as np
#np.set_printoptions(suppress=True) #Suppress Scientific Notation
np.set_printoptions(precision=4) #Set FP printing precision

# Number of trials to average over
num_trials = 100000

# Total number of troops on your starting territory
initial_offense = 37
# The number of defenders on the territories in the order to be attacked
initial_scenario = np.array([2,2,2,2,4,1,1,1,1,1,1,1,4,1,1])
##initial_scenario = np.ones(30)*2

# Try to catch the user putting in dumb inputs
assert num_trials > 0
assert initial_offense > 0
assert initial_scenario.size

# Simulate Risk single battle odds
#   attack: Total number on attacking territory
#   defend: Total number on defending territory
# Returns:
#   [attack, defend, num_lost, num_killed] after battle is finished.
# Reference: http://www.datagenetics.com/blog/november22011/
def roll(attack,defend):
    roll=random.random()
    if defend == 1:
        if attack == 2:
            if roll < 0.41666666667:
                return [attack,defend - 1, 0,1]
            else:
                return [attack -1, defend, 1,0]
        elif attack == 3:
            if roll < 0.5787037037:
                return [attack,defend - 1, 0,1]
            else:
                return [attack -1, defend, 1,0]
        elif attack > 3:
            if roll < 0.65972222222:
                return [attack,defend - 1, 0,1]
            else:
                return [attack -1, defend, 1,0]
        else:
            print "Error: Invalid Attack"
            print [attack, defend]
            return
    elif defend > 1:
        if attack == 2:
            if roll < 0.25462962963:
                return [attack,defend - 1, 0,1]
            else:
                return [attack - 1, defend, 1,0]
        elif attack == 3:
            if roll < 0.22762345679:
                return [attack,defend - 2, 0,2]
            elif roll > (1 - 0.44830246913):
                return [attack - 2, defend, 2,0]
            else:
                return [attack - 1, defend - 1, 1,1]
        elif attack > 3:
            if roll < 0.371656379:
                return [attack,defend - 2, 0,2]
            elif roll > (1 - 0.29256687242):
                return [attack - 2, defend, 2,0]
            else:
                return [attack - 1, defend - 1, 1,1]     
        else:
            print "Error: Invalid Attack"
            print [attack, defend]
            return
    else:
        print "Error: Invalid Defend"
        print [attack, defend]
        return

# Initialize Conquest Statistics
average_remaining_scenario = np.zeros(len(initial_scenario))
successes = np.zeros(len(initial_scenario))
remaining_offense = np.zeros(len(initial_scenario))
total_lost = 0
total_killed = 0

# Monte Carlo Loop
for i in range(num_trials):
    # Initialize each trial
    scenario = np.array(initial_scenario) #Make a deep copy
    offense = initial_offense
    terr = 0 # index for which territory we're on
    defense = scenario[terr] 

    success_flag = 0 # Indicates full conquest success

    # Conquest Loop
    while offense > 1:
        [offense, defense,lost,killed] = roll(offense,defense)
        total_lost += lost
        total_killed += killed
        scenario[terr] = defense #Update scenario

        # Territory defeated, advance army
        if defense == 0:
            successes[terr] += 1
            offense -= 1 #Leave one troop behind
            remaining_offense[terr] += offense
            terr += 1 #Advance one territory

            # Conquest complete
            if terr == len(scenario):
                break # Exit Conquest Loop

            # If conquest not complete, attack next territory
            defense = scenario[terr]
        
    average_remaining_scenario += scenario

successes /= num_trials
remaining_offense /= num_trials
average_remaining_scenario /= num_trials

## Print conquest statistics
print "Total Success Rate: ", successes[-1] #success rate of conquering last territory
print "Initial Offense: ", initial_offense
print "Average Scenario: "
for i in range(len(average_remaining_scenario)):
    print i+1, ":\tInitial=", initial_scenario[i], \
                "\tFinal=", average_remaining_scenario[i], \
                "\tRemaining Offense=",remaining_offense[i], \
                "\tSuccess Rate=", successes[i]
print "Average Killed: ",total_killed/num_trials
print "Average Lost: ",total_lost/num_trials
