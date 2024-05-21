#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 12:16:28 2023

@author: bing
"""
import random
random.seed("ics2024spring")

class Agent():
    def __init__(self, n_state, n_act, gamma = 0.0, epsilon = 0.0):
        self.Q = [ [0 for i in range(n_act)] for j in range(n_state)]
        self.gamma = gamma
        self.epsilon = epsilon
        
    def get_maxQ(self, s, valid_acts):
        if valid_acts:
            max_q = self.Q[s][valid_acts[0]]
            for a in valid_acts:
                if self.Q[s][a] > max_q:
                    max_q = self.Q[s][a]
        else:
            max_q = 0
        return max_q
        
    def get_maxQ_act(self, s, acts):
        max_q = -1
        for a in acts:
            if self.Q[s][a] > max_q:
                max_q = self.Q[s][a]
                max_a = a
            elif self.Q[s][a] == max_q: # make some randomness when tie
                if random.random() < 0.5:
                    max_a = a
        return max_a
        
    def make_choice(self, s, valid_choices): 
        ##--You need to complete this function--#
        ##--using epsilon greedy--##
        ##--removing the following statements

        # The idea here is to use epsilon greedy algorithms to pick the choice that brings maximum values in all valid choices 
        # choice = max(valid_choices, key=lambda x: w.items[x]["value"])
        
        choice = valid_choices[-1]
        
        return choice
        
    def update_Q(self, s, a, next_s, next_valid_choices, r):
        q_star = r + self.gamma * self.get_maxQ(next_s, next_valid_choices)
        self.set_Q(s, a, q_star)
        return
        
    def set_Q(self, s, a, val):
        self.Q[s][a] = val
        
    def __str__(self):
        qstr = ''
        for i in range(len(self.Q)):
            qstr += str(self.Q[i]) + '\n'
        return qstr
      