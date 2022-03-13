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
    # reset df index for later operations
    round_input_df = round_input_df.reset_index(drop=True)
    
    # initialize df
    round_output_df = pd.DataFrame()
    
    for i in range(0, int(len(round_input_df)/2)):
        # locate teams by df index
        index = np.array([i, len(round_input_df)-1-i])
        # team matchup
        #mask = (round_input_df['seed'] == i) & (round_input_df['seed'] == len(round_input_df)-1-i])
        
        #round_input_df = 
        #matchup = [round_input_df['seed'][index[0]], round_input_df['seed'][index[1]]]
        # matchup based on index
        matchup = [index[0], index[1]]
        
        # df index to seed conversion
        #seed = np.array([index[0] + 1, index[1] + 1])
       
        #seed_difference = seed[1] - seed[0]
        seed_difference = round_input_df['seed'][index[1]] - round_input_df['seed'][index[0]]
        
        # prevent log error if seed difference equals 0
        if seed_difference < 1:
            seed_difference = 1
        
        # cannot take log of negative number
        probability = 0.177*math.log(abs(seed_difference)) + 0.500
        
        if seed_difference >= 0:
            winner = random.choices(matchup, cum_weights=(probability, 1.0), k=1)
        else:
            # reverse matchup order to account of negative seed_difference
            winner = random.choices(np.flip(matchup), cum_weights=(probability, 1.0), k=1)
        
        # df row of matchup winner
        team_advancing = round_input_df.loc[winner]
        
        # append matchup winner to output df
        # reset index otherwise indexing error occurs
        round_output_df = pd.concat([round_output_df, team_advancing],
                                    ignore_index=True, sort=False)
        
    return round_output_df

#%% run script

if __name__ == "__main__":
    
    debug = False
    
    if debug == True:
        random.seed(4)
    
    region_names = np.array(['east', 'west', 'south', 'midwest'])
    
    # initialize list of df's containing each round's winners
    round_output_df = [pd.DataFrame()]*7
    
    for i in region_names:
        
        region_df = pd.read_csv(i + '.csv')
        # add column for region name
        region_df['region'] = i
        # build single df with all teams in all regions
        #round_output_df[0] = pd.concat([round_output_df[0], region_df],
        #                               ignore_index=True, sort=False)
        if i == region_names[0]:
            round_output_df[0] = region_df
        else:
            round_output_df[0] = pd.merge(round_output_df[0], region_df,
                                          how='outer',
                                          sort=False)

    # iterate through the 4 regions
    for z in region_names:
        
        # initial input to the matchup() function
        current_round_df = round_output_df[0]
        
        mask = current_round_df['region']==z
        current_round_df = current_round_df[mask].reset_index(drop=True)     
        
        # iterate through 4 rounds to determine the region winner
        for i in range(1, 5):

            #round_output_df[i] = matchup(current_round_df)
            round_output_df[i] = pd.concat([round_output_df[i], 
                                            matchup(current_round_df)],
                                            ignore_index=True, sort=False)
            # if i == 1:
            #     round_output_df[i] = matchup(current_round_df)
            # else:
            #     round_output_df[i] = pd.merge(round_output_df[i], 
            #                               matchup(current_round_df),
            #                               how='outer',
            #                               sort=False)
            
            
            # use downselected list of teams during next iteration
            current_round_df = round_output_df[i]
            mask = current_round_df['region']==z
            current_round_df = current_round_df[mask].reset_index(drop=True)
    
    # get semi-finalists
    final_four_df = round_output_df[4]
    
    mask = (final_four_df['region'] == region_names[0]) | (final_four_df['region'] == region_names[1])
    matchup_df = final_four_df[mask]
 
    # semi-finalist 1
    round_output_df[5] = matchup(matchup_df)
    
    mask = (final_four_df['region'] == region_names[2]) | (final_four_df['region'] == region_names[3])
    matchup_df = final_four_df[mask]

    # semi-finalist 2
    round_output_df[5] = pd.concat([round_output_df[5], 
                                    matchup(matchup_df)],
                                    ignore_index=True, sort=False)
    
    # championship matchup
    round_output_df[6] = matchup(round_output_df[5])
    
    