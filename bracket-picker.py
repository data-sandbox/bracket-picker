#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initial creation: 2022 03
 
"""

import random

def readFile(fileName):
        fileObj = open(fileName, "r") #opens the file in read mode
        words = fileObj.read().splitlines() #puts the file into an array
        fileObj.close()
        return words

west = readFile('west.txt')

round1 = []

# round 1
# for i in range(int(len(west)/2)):
#     matchup = [west[i], west[-1-i]]
#     winner = random.choices(matchup, cum_weights=(0.99, 1.0), k=1)
#     round1.append(winner)
#     print(winner)
    
# round 1
for i in range(0, len(west), 2):
    matchup = [west[i], west[i+1]]
    winner = random.choices(matchup, cum_weights=(0.99, 1.0), k=1)
    round1.append(winner)
    
print(round1)