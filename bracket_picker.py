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
    
    region_names = np.array(['east', 'west', 'south', 'midwest'])
    #region_names = ['west', 'east', 'south', 'midwest']
    
    # import initial list of teams
    east_df = pd.read_csv(region_names[0] + '.csv')
    east_df['region'] = region_names[0]    
    
    west_df = pd.read_csv(region_names[1] + '.csv')
    west_df['region'] = region_names[1]
    
    south_df = pd.read_csv(region_names[2] + '.csv')
    south_df['region'] = region_names[2]
    
    midwest_df = pd.read_csv(region_names[3] + '.csv')
    midwest_df['region'] = region_names[3]
    
    regions = [east_df, west_df, south_df, midwest_df]
    
    # initialize list of df's containing each round's winners
    round_output_df = [pd.DataFrame()]*6
    
    # iterate through all rounds leading to the final four
    for z in range(len(regions)):
        
        # initial input to the matchup() function
        current_round_df = regions[z]
        
        for i in range(0, 4):
            
            #round_output_df[i] = matchup(current_round_df)
            round_output_df[i] = pd.concat([round_output_df[i], 
                                           matchup(current_round_df)])
            
            # reset index, otherwise indexing error occurs
            round_output_df[i] = round_output_df[i].reset_index(drop=True)
            
            # use downselected list of teams during next iteration
            current_round_df = round_output_df[i]
            current_round_df = current_round_df[current_round_df['region'] == region_names[z]]
            
            # reset index, otherwise indexing error occurs
            current_round_df = current_round_df.reset_index(drop=True)
    
    
    # simulate final four  
    final_four_df = round_output_df[3]
    
    matchup_df = final_four_df[(final_four_df['region'] == region_names[0]) | (final_four_df['region'] == region_names[1])]
    round_output_df[4] = pd.concat([round_output_df[4], 
                                    matchup(matchup_df)])
    
    matchup_df = final_four_df[(final_four_df['region'] == region_names[2]) | (final_four_df['region'] == region_names[3])]
    matchup_df = matchup_df.reset_index(drop=True)
    
    # semifinal matchup
    round_output_df[4] = pd.concat([round_output_df[4], 
                                    matchup(matchup_df)])
    round_output_df[4] = round_output_df[4].reset_index(drop=True)
    
    # championship matchup
    round_output_df[5] = matchup(round_output_df[4])
    
    