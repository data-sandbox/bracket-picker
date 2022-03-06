#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initial creation: 2022 03

This code uses a tunable probability parameter to simulate and generate a
NCAA Basketball March Madness bracket.

"""

import numpy as np
import pandas as pd
import random
import math


#%%

def matchup(round_input_df):
    """
    Select a matchup winner based on probability parameter
    """
    # initialize df
    round_output_df = pd.DataFrame()
    
    for i in range(0, int(len(round_input_df)/2)):
        # df index
        index = np.array([i, len(round_input_df)-1-i])
        # team matchup
        matchup = [round_input_df['seed'][index[0]], round_input_df['seed'][index[1]]]
        
        # df index to seed conversion
        seed = np.array([index[0] + 1, index[1] + 1])
        
        # probability seed[0] will win
        seed_difference = seed[1] - seed[0]
        probability = 0.177*math.log(seed_difference) + 0.500
    
        winner = random.choices(matchup, cum_weights=(probability, 1.0), k=1)
        
        team_advancing = round_input_df.loc[round_input_df['seed'] == int(winner[0])]
        
        round_output_df = pd.concat([round_output_df, team_advancing])
        
        # reset index, otherwise indexing error occurs
        round_output_df = round_output_df.reset_index(drop=True)
        
    return round_output_df

#%% run script

if __name__ == "__main__":
    
    # import initial list of teams
    west_df = pd.read_csv('west.csv')
    east_df = pd.read_csv('east.csv')
    
    all_teams = [west_df, east_df]
    
    # initialize list of df's containing the round winners
    round_output_df = [pd.DataFrame()]*4
    
    final_four_df = [pd.DataFrame()]*4
    
    #current_round_df = west_df
    
    for z in range(len(all_teams)):
        
        # initial input to the matchup() function
        current_round_df = all_teams[z]
        
        for i in range(len(round_output_df)):
            
            round_output_df[i] = matchup(current_round_df)
            
            # use downselected list of teams during next iteration
            current_round_df = round_output_df[i]
        
        final_four_df[z] = round_output_df[-1]
        
    
    