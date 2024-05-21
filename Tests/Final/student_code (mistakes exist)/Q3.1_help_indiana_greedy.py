#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 09:42:13 2024

@author: bing
"""

import copy


##The code of the Item class is given.
class Item:

    def __init__(
        self,
        n="",
        w=0,
        v=0,
    ):
        self.name = n
        self.weight = w
        self.value = v

    def setName(self, n):
        self.name = n

    def getName(self):
        return self.name

    def setWeight(self, w):
        self.weight = w

    def getWeight(self):
        return self.weight

    def setValue(self, v):
        self.value = v

    def getValue(self):
        return self.value

    def __str__(self):
        result = (
            "<"
            + self.name
            + ", "
            + "Weight: "
            + str(self.weight)
            + ", "
            + "Value: "
            + str(self.value)
            + ">"
        )
        return result


##Q3.1.1: Knapsack class
class Knapsack:

    def __init__(self, maxW=0):
        self.items = []
        self.maxWeight = maxW

    def addItem(self, item):
        # ---start you code here---#

        self.items.append(item)

        # ---end of your code---#

    def totalValue(self):
        # ---start you code here---#

        total_value = 0
        for item in self.items:
            total_value += item.getValue()
        return total_value

        # ---end of your code---#

    def totalWeight(self):
        # ---start you code here---#

        total_weight = 0
        for item in self.items:
            total_weight += item.getWeight()
        return total_weight

        # ---end of your code---#

    def allItems(self):
        # ---start you code here---#

        return self.items

        # ---end of your code---#

    def __str__(self):
        # ---start you code here---#

        ##replace the following with your code
        result_lst = [
            f"<{item.name}, Weight: {item.getWeight()}, Value: {item.getValue()}>"
            for item in self.items
        ]
        return "\n".join(result_lst)
        # ---end of your code---#


##Q3.1.2 the greedy algorithm
def find_max(treasures: list):
    # ---start you code here---#

    return max(treasures, key=lambda x: x.getValue())
    # ---end of your code---#


def run_greedy(treasures: list, knapsack):
    # ---start you code here---#

    while treasures:
        max_value_item = find_max(treasures)
        max_value_item_weight = max_value_item.getWeight()
        if max_value_item_weight + knapsack.totalWeight() <= knapsack.maxWeight:
            knapsack.addItem(max_value_item)
        treasures.remove(max_value_item)
    # ---end of your code---#


##---Tests---##
if __name__ == "__main__":
    treasures_found = {
        "Golden Idol": {"weight": 5, "value": 3},
        "Peacock's eye": {"weight": 3, "value": 6},
        "Lost Ark": {"weight": 7, "value": 5},
        "Holy Grail": {"weight": 2, "value": 4},
        "Crystal skull": {"weight": 3, "value": 3},
        "Truncheon": {"weight": 4, "value": 4},
    }

    ## Test of Knapsack class
    print()
    print("---Test of Knapsack class---")
    bag = Knapsack(15)

    for name, attr in treasures_found.items():
        bag.addItem(Item(name, attr["weight"], attr["value"]))
    print(bag.totalValue())

    print(bag)
    ## Test of greedy algorithm
    print()
    print("---Test of greedy algorithm---")

    treasures = []
    for name, attr in treasures_found.items():
        treasures.append(Item(name, attr["weight"], attr["value"]))
    bag = Knapsack(15)

    run_greedy(treasures, bag)
    print(bag)
