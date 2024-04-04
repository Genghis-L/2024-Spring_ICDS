#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 09:32:47 2019

@author: xg7
"""


class Contacts:
    """
    A class for storing contacts and their phone numbers
    You can refer the textbook--MIT text, Chapter 10.3 Figure 10.7
    """

    def __init__(self, numBuckets):
        """Create an empty dictionary"""
        self.buckets = []
        self.numBuckets = numBuckets
        for i in range(numBuckets):
            self.buckets.append([])
        return

    def addEntry(self, name, phoneNumber):
        """the name is a string. Adds an entry
        First, convert the name into an integer by using ord(); this has been done for you.
        Then, use the hash function: int_key % (the number of buckets) to locate its bucket.
        """
        int_key = 0
        for s in name:
            int_key += ord(s)
        # insert your code here

        index = int_key % self.numBuckets
        self.buckets[index].append((name, phoneNumber))

    def getValue(self, name):
        """The name is a string. Returns the phone number of the name"""
        int_key = 0
        for s in name:
            int_key += ord(s)
        # insert your code here

        index = int_key % self.numBuckets
        for i in range(len(self.buckets[index])):
            if self.buckets[index][i][0] == name:
                return self.buckets[index][i][1]


# no need to modify the following code
# But please read them carefully so that you will know what you need to do.
if __name__ == "__main__":

    import random

    random.seed(100)

    celebrities = ["John Lennon", "Paul MaCartney", "George Harrison",
                   "Ringo Starr", "Michael Jackson", "Kim Kardashian",
                   "John Snow", "Arya Stark", "Daenerys Targaryen",
                   "Tyrion Lannister", "Jaime Lannister", "Sansa Stark",
                   "Petyr Baelish", "Lord Varys", "Hodor", "Ygritte",
                   "Gilly", "Davos Seaworth", "Cersei Lannister",
                   "Khal Drogo", "Bran Stark", "Theon Greyjoy"]

    # code for generating the my contacts
    # the elements in myContacts are lists of [name, phone numbers]
    myContacts = []
    for name in celebrities:
        phone = random.choice(range(10**5))
        myContacts.append([name, phone])

    print("My contacts are:\n", myContacts)

    # build an instance of Contacts
    numOfBucket = 17
    D = Contacts(numOfBucket)
    for contact in myContacts:
        D.addEntry(contact[0], contact[1])

    # print("\n", "The buckets are:")
    # for hashBucket in D.buckets:
    #     print(' ', hashBucket)
    print("The phone of Tyrion Lannister is ", D.getValue("Tyrion Lannister"))
