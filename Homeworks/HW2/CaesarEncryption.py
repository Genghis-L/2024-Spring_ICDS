#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 09:56:01 2021

@author: bing
"""

import random
import string


def caesarEncrypt(message, codebook, shift):
    '''
    - you can compute the index of a character, or,
    - you can convert the codebook into a dictionary
    '''

    encrypted = ""
    # put your code here

    global codebook_en
    codebook_en = {}
    l = len(codebook)
    for i in range(l):
        codebook_en[codebook[i]] = codebook[(i+shift) % l]

    for char in message:
        if char.isalpha():
            encrypted += codebook_en[char]
        else:
            encrypted += char

    return encrypted


def caesarDecrypt(message, codebook, shift):
    decrypted = ""
    # put your code here
    
    global codebook_de
    codebook_de = {}
    for k, v in codebook_en.items():
        codebook_de[v] = k

    for char in message:
        if char.isalpha():
            decrypted += codebook_de[char]
        else:
            decrypted += char

    return decrypted


if __name__ == "__main__":
    # The following several lines generate the codebook
    # Please don't change it
    random.seed("Caesar")

    codebook = []
    for e in string.ascii_letters:
        codebook.append(e)

    random.shuffle(codebook)
    print("Your codebook:")
    print(codebook)
    # end of the codebook generation

    m = "Hello Kitty!"
    shift = 3
    encoded = caesarEncrypt(m, codebook, shift)
    decoded = caesarDecrypt(encoded, codebook, shift)
    print("Origin:", m)
    print("Encoded:", encoded)
    print("Decoded", decoded)
