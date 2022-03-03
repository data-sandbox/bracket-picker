#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initial creation: 2022 03
 
"""

import random

west = ['team1', 'team2']

for i in range(10):
    round1 = random.choices(west, cum_weights=(0.5, 1.0), k=1)
    print(round1)