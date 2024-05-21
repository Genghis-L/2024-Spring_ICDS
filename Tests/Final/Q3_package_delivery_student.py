#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 13:53:38 2023

@author: bing
"""


class Package:

    def __init__(self, n="", w=0, v=0):
        self.receiver = n
        self.weight = w
        self.value = v

    def setReceiver(self, n):
        ## remove the following statements
        ##----------write your code below----------#
        self.receiver = n

    def getReceiver(self):
        ## remove the following statements
        ##----------write your code below----------#
        return self.receiver

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
            + self.receiver
            + ", "
            + "Weight: "
            + str(self.weight)
            + ", "
            + "Value: "
            + str(self.value)
            + ">"
        )
        return result


class Van:

    def __init__(self, maxW=0):
        self.packages = []
        self.maxWeight = maxW

    def addPackage(self, package):
        ## remove the following statements
        ##----------write your code below----------#
        self.packages.append(package)

    def removePackage(self, receiver):
        for i in self.packages[::-1]:
            if i.getReceiver() == receiver:
                self.packages.remove(i)

    def totalValue(self):
        ## remove the following statements
        ##----------write your code below----------#
        total_value = 0
        for package in self.packages:
            total_value += package.getValue()
        return total_value

    def totalWeight(self):
        ## remove the following statements
        ##----------write your code below----------#
        total_weight = 0
        for package in self.packages:
            total_weight += package.getWeight()
        return total_weight

    def allPackages(self):
        ## remove the following statements
        ##----------write your code below----------#
        return self.packages

    def isOverWeight(self):
        ## remove the following statements
        ##----------write your code below----------#
        return self.totalWeight() > self.maxWeight

    def __str__(self):
        ## remove the following statements
        ##----------write your code below----------#
        result_lst = [
            f"<{package.receiver}, Weight: {package.getWeight()}, Value: {package.getValue()}>"
            for package in self.packages
        ]
        return "\n".join(result_lst)


class Fill:

    def __init__(self, p, v):
        self.packages = tuple(p)  ## all packages in the table
        self.packagesRemain = list(self.packages)
        self.van = v

    def _findMax(self):
        ## remove the following statements
        ##----------write your code below----------#
        return max(self.packagesRemain, key=lambda x: x.getValue())

    def _removeItem(self, package):
        ## remove the following statements
        ##----------write your code below----------#
        self.packagesRemain.remove(package)

    def byGreedy(self):
        ## remove the following statements
        ##----------write your code below----------#
        while self.packagesRemain:
            max_value_package = self._findMax()
            max_value_package_weight = max_value_package.getWeight()
            if max_value_package_weight + self.van.totalWeight() <= self.van.maxWeight:
                self.van.addPackage(max_value_package)
            self._removeItem(max_value_package)


##---Tests---##
if __name__ == "__main__":
    packages_need_delivery = {
        "Indiana Jones": {"weight": 15, "value": 30},
        "Harry Potter": {"weight": 30, "value": 60},
        "Darth Vader": {"weight": 50, "value": 50},
        "Elsa Frost": {"weight": 20, "value": 40},
        "Sam Flynn": {"weight": 25, "value": 35},
        "Rick Deckard": {"weight": 40, "value": 45},
    }
    ## Test of Package class
    print("---Test of Package class---")
    package1 = Package()
    package1.setReceiver("Indian Jones")
    print(package1.getReceiver())
    package1.setWeight(15)
    print(package1.getWeight())
    package1.setValue(30)
    print(package1.getValue())
    print(package1)

    ## Test of Van class
    print()
    print("---Test of Van class---")
    my_van = Van(150)

    for receiver, attr in packages_need_delivery.items():
        my_van.addPackage(Package(receiver, attr["weight"], attr["value"]))
    print(my_van.totalValue())
    # print(my_van.totalWeight())
    print(my_van)
    ## Test of Fill class
    print()
    print("---Test of Fill class---")

    packages = []
    for receiver, attr in packages_need_delivery.items():
        packages.append(Package(receiver, attr["weight"], attr["value"]))
    my_van = Van(150)
    selectPackages = Fill(packages[:], my_van)
    selectPackages.byGreedy()
    print(selectPackages.van)
    print(selectPackages.van.totalWeight())
    print(selectPackages.van.totalValue())
