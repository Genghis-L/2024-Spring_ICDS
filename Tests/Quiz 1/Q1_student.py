#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 10:38:18 2021

@author: bing
"""

def count_letters(s):
    # ---remove the pass put your code here--##
    word_dict = {}
    for word in s:
        word_dict[word] = word_dict.get(word, 0) + 1
        pass

    return word_dict


def count_letter_pairs(s, pair_len):
    # ---remove the pass put your code here--##
    word_pair_dict = {}
    word_pair_list = [s[i:i+pair_len] for i in range(len(s)-pair_len+1)]
    for word in word_pair_list:
        word_pair_dict[word] = word_pair_dict.get(word, 0) + 1
        pass

    return word_pair_dict


if __name__ == "__main__":
    s = "banana"
    print(count_letters(s))
    
    s = "banana"
    print(count_letter_pairs(s, 2))
    
    s = "barbarian"
    print(count_letter_pairs(s, 3))
    