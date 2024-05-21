#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 12:02:48 2023

@author: bing
"""


class World():
    
    def __init__(self, treasures, bag_capacity):
        self.items = treasures
        self.bag_capacity = bag_capacity
        self.num_states = bag_capacity + 1
        self.num_acts = len(self.items)
        self.items_available = [True for i in range(len(self.items))] 
        
    def is_final_state(self, s):
        '''
        Note: the input s is always >= 0
        '''
        item_remained = [i for i in range(self.num_acts) if self.items_available[i]]
        if s == 0:
            return True
        if s > 0 and s < min([self.items[idx]["weight"] for idx in item_remained]):
            return True
        return False
        
    def get_num_states(self):
        
        return self.num_states
    
    def get_num_acts(self):
        
        return self.num_acts
        
    def get_valid_acts(self, s):
        valid_acts = []
        for i in range(self.num_acts):
            if self.items_available[i]:
                if self.items[i]["weight"] <= s:
                    valid_acts.append(i)
        return valid_acts
        
    def get_reward_in_state_act(self):
        ##-- You need to complete this function--#
        values = 0
        for i in range(len(self.items)):
            values += self.items_available[i] * self.items[i]["value"]
        return values
    
    def get_item_weight(self, item_idx):
        return self.items[item_idx]["weight"]
    
    def set_items_available(self, item_idx):
        self.items_available[item_idx] = False
    
    def reset_items_available(self):
        self.items_available = [True for i in range(self.num_acts)]
        