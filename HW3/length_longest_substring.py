#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 15:50:35 2024

@author: bing
"""


def lengthOfLongestSubstring(s: str) -> int:
    '''
    the function takes a string as the input and returns an integer
    '''
    def rp(sub):
        for i in sub:
            if sub.count(i) > 1:
                return False
            else:
                continue
        return True

    w = 1
    flag = True
    while flag == True:
        pre_w = w
        for i in range(len(s)-w+1):
            if rp(s[i:i+w]):
                w += 1
                break
        if pre_w == w:
            flag = False

    return w-1


if __name__ == "__main__":

    s = ""
    len_longest = lengthOfLongestSubstring(s)
    print(len_longest)
    s = "au"
    len_longest = lengthOfLongestSubstring(s)
    print(len_longest)
    s = "bbb"
    len_longest = lengthOfLongestSubstring(s)
    print(len_longest)
    s = "pwwkew"
    len_longest = lengthOfLongestSubstring(s)
    print(len_longest)
    s = "abcabcbb"
    len_longest = lengthOfLongestSubstring(s)
    print(len_longest)

    # #large string_1
    # s = "cbadcv"*10000
    # len_longest = lengthOfLongestSubstring(s)
    # print(len_longest)

    # #large string_2
    # s = "pwwkew"*10000
    # len_longest = lengthOfLongestSubstring(s)
    # print(len_longest)
