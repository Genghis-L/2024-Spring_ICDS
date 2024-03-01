#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 15:20:57 2021

@author: bing
"""


def permute(nums):
    # put your code here

    if len(nums) == 1:
        return [nums]

    result = set()  # Using a set to store unique permutations
    for i in range(len(nums)):
        current_num = nums[i]
        remaining_nums = nums[:i] + nums[i+1:]
        for perm in permute(remaining_nums):
            # Convert to tuple for hashing
            result.add(tuple([current_num] + perm))

    # Convert permutations back to lists
    return [list(perm) for perm in result]


# tests
if __name__ == "__main__":
    nums = [1, 2, 3]
    p1 = permute(nums)
    print("Permutation:", p1)

    nums = [1, 1, 2]
    p1 = permute(nums)
    print("Permutation:", p1)

    nums = ['a', 'b', 'c', 'd']
    p2 = permute(nums)
    print("Permutation:", p2)
