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

def get_winners(round_input_df):
    """
    Get matchup winners based on probability parameter
    """
    # clean input df. reset index for later operations
    round_input_df = round_input_df.reset_index(drop=True)
    
    # initialize output df
    round_output_df = pd.DataFrame()
    
    for i in range(0, int(len(round_input_df)/2)):
        # locate teams by df index
        index = np.array([i, len(round_input_df)-1-i])
        
        matchup = [index[0], index[1]]
        
        seed_difference = round_input_df['seed'][index[1]] - round_input_df['seed'][index[0]]
        
        # avoid log error if seed difference equals 0
        if seed_difference < 1:
            seed_difference = 1
        
        # abs seed difference because cannot take log of negative number
        probability = 0.177*math.log(abs(seed_difference)) + 0.500
        
        # check if seed difference is positive or negative
        if seed_difference >= 0:
            winner = random.choices(matchup, cum_weights=(probability, 1.0), k=1)
        else:
            # reverse matchup order to account of negative seed_difference
            winner = random.choices(np.flip(matchup), cum_weights=(probability, 1.0), k=1)
        
        # get df row of matchup winner
        team_advancing = round_input_df.loc[winner]
        
        # concat matchup winner to output df
        round_output_df = pd.concat([round_output_df, team_advancing],
                                    ignore_index=True, sort=False)
        
    return round_output_df

#%% run script

if __name__ == "__main__":
    
    debug = False
    
    if debug == True:
        random.seed(4)
    
    regions = np.array(['east', 'west', 'south', 'midwest'])
    
    # build df with all 1st round teams
    round_output_df = [pd.DataFrame()]*7
    
    for i in regions:
        # read csv file
        region_df = pd.read_csv(i + '.csv')
        # add column for region name
        region_df['region'] = i
        
        # special case when round_output_df is still empty df
        if i == regions[0]:
            round_output_df[0] = region_df
        else:
            round_output_df[0] = pd.merge(round_output_df[0], region_df,
                                          how='outer',
                                          sort=False)

    # iterate through the 4 regions
    for z in regions:
        # initial input to the get_winners() function
        current_round_df = round_output_df[0]
        # boolean mask for region of iterest
        mask = current_round_df['region']==z
        current_round_df = current_round_df[mask].reset_index(drop=True)     
        
        # iterate through 4 rounds to determine the overall region winner
        for i in range(1, 5):

            round_output_df[i] = pd.concat([round_output_df[i], 
                                            get_winners(current_round_df)],
                                            ignore_index=True, sort=False)
            
            # use downselected team list during next iteration
            current_round_df = round_output_df[i]
            mask = current_round_df['region']==z
            current_round_df = current_round_df[mask].reset_index(drop=True)
    
    # get semi-finalist 1
    final_four_df = round_output_df[4]  
    mask = (final_four_df['region'] == regions[0]) | (final_four_df['region'] == regions[1])
    matchup1_df = final_four_df[mask]
    round_output_df[5] = get_winners(matchup1_df)

    # get semi-finalist 2
    mask = (final_four_df['region'] == regions[2]) | (final_four_df['region'] == regions[3])
    matchup2_df = final_four_df[mask]
    round_output_df[5] = pd.merge(round_output_df[5], get_winners(matchup2_df),
                                  how='outer', sort=False)
    
    # get championship winner
    round_output_df[6] = get_winners(round_output_df[5])
    
    