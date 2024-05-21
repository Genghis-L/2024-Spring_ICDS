#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 12:37:06 2023

@author: bing
"""
from Q32world import World
from Q32agent import Agent


def train_agent(treasures_found, bag_capacity):
    ''' set up the world'''
    w = World(treasures_found, bag_capacity)
    num_states = w.get_num_states()
    num_actions = w.get_num_acts()
        
    ''' set up the agent '''
    gamma = 1
    epsilon = 0.1 
    agent = Agent(num_states, num_actions, gamma, epsilon)
    
    ''' set up the runs '''
    total_iter = 1000
    num_iter = 0
    
    ''' start learning '''
    while num_iter < total_iter: 
        ''' init state to bag_capacity, choices to empty'''
        s = bag_capacity
        
        while True:
            ''' make a choice 
                by calling make_choice() in the Agent class,
                and you need to compelte the function in agent.py
            Note: 
                valid_choices is a list of indices of items in the item list
                choice is the index of the chosen item
                
            '''
            valid_choices = w.get_valid_acts(s)
            choice = agent.make_choice(s, valid_choices)
            
            '''
            label the item as picked by calling set_items_available
            '''
            w.set_items_available(choice)
            
            '''get the instant reward of the choice 
               by calling get_reward_in_state_act() in the World class,
               and you need to complete the function in world.py
            '''
            this_reward = w.get_reward_in_state_act()
            
            '''
            next state is the bag's remaining capacity after picking the item;
            next_s = s - w.get_item_weight(choice)
            '''
            next_s = s - w.get_item_weight(choice)
            valid_choices = w.get_valid_acts(next_s)
            agent.update_Q(s, choice, next_s, valid_choices, this_reward)       
            s = next_s
            
            '''check if the state is the final state'''
            if w.is_final_state(s):
                w.reset_items_available()
                break
        num_iter += 1
    print(agent)
    return w, agent


def pick_items(world, agent):
    s = world.bag_capacity
    treasures = world.items
    picked = []
    while True:
        max_q = -1
        idx = -1
        for j in range(len(agent.Q[s])):
            if j not in picked:
                if treasures[j]["weight"]<=s:
                    if max_q < agent.Q[s][j]:
                        max_q = agent.Q[s][j]
                        idx = j
        if idx == -1:
            break
        s -= treasures[idx]["weight"]
        picked.append(idx)
        if s == 0:
            break
    total_value = 0
    total_weight = 0
    print("Items picked:")
    for p in picked:
        print(treasures[p])
        total_value += treasures[p]["value"]
        total_weight += treasures[p]["weight"]
    print("total value:", total_value, "total weight:", total_weight)
    return picked


if __name__=="__main__":
    
    treasures_found = [
            {"name": "Golden Idol", "weight": 5, "value": 3},
            {"name": "Peacock's eye", "weight": 3, "value": 6},
            {"name": "Lost Ark", "weight": 7, "value": 5},
            {"name": "Holy Grail","weight": 2, "value": 4},
            {"name": "Crystal skull", "weight": 3, "value": 3},
            {"name": "Truncheon", "weight": 4, "value": 4},
        ]
        
    
    bag_capacity = 15
   
    world, agent = train_agent(treasures_found, bag_capacity)
    pick_items(world, agent)
    
   