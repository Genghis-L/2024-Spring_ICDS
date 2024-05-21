#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 13:48:37 2021

@author: bing
"""

import random
random.seed(2022) # fix seed for reproducibility

class Dice:
    def __init__(self, bias=0.5):
        self.bias = bias

    def roll(self):
        return random.uniform(0, 1) < self.bias
    
    
def pick_vaccine(your_dice, candidates_data):
    #----------your code below----------#
    # IMPLEMENT THE FOLLOWING PART
    # Hint:
    # the variable "pick" is the vaccine chose by your algorithm
    # use your dice to decide whether to do exploration or do exploitation
    # if do exploitation, pick the vaccine has the highest estimated success rate
    # success/volunteers gives the estimated success rate

    # Now, modify the following lines and implement e-greedy
    if your_dice.roll():
        pick = random.choice(range(len(candidates_data))) ##randomly chooses one
    # if here we are to do exploitation, then goes into the if branch
    else:
        # pick = 0
        success_rate_max = candidates_data[0]['success'] / candidates_data[0]['volunteers']
        most_successful_vaccine_index = 0
        for index in range(1, len(candidates_data)):
            current_success_rate = candidates_data[index]['success'] / candidates_data[index]['volunteers']
            if current_success_rate > success_rate_max:
                most_successful_vaccine_index, success_rate_max = index, current_success_rate
        pick = most_successful_vaccine_index
    # #----------your code ends----------#
    return pick


## read the following code carefully
if __name__ == "__main__":
    
    epsilon = 0.1
    your_dice = Dice(epsilon)
    
    success_rates = [0.85, 0.75, 0.42, 0.25, 0.52]
    num_candidates = len(success_rates)
    candidates = []
    for i in range(num_candidates):
       m = Dice(success_rates[i])
       candidates.append(m)
       
    
    num_volunteers = 10000
    candidates_data = {}
    
    for i in range(num_candidates):
       candidates_data[i] = {'success': 0, 'volunteers': 1e-100}
       
    for i in range(num_volunteers):
        # pick_caccine() is the function you need to implement
        pick = pick_vaccine(your_dice, candidates_data)
        candidates_data[pick]['volunteers'] += 1
        candidates_data[pick]['success'] += candidates[pick].roll()
        
            
    print("++++++++ true success rates:")
    for i in range(num_candidates): print(i, success_rates[i])
    print("\n")
    print("++++++++ after simulation ", num_volunteers)
    for i in range(num_candidates): print(i, candidates_data[i])
    print("-------- estimated success rates:")
    for i in range(num_candidates):
        print(i, candidates_data[i]['success']/candidates_data[i]['volunteers'])
    
