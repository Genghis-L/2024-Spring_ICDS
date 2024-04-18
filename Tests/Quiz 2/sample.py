#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 12:54:37 2022

@author: bing
"""


class Sample:
    def __init__(self, x, y, label=""):
        self.x = x
        self.y = y
        self.label = label

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    def get_label(self):
        return self.label

    def set_label(self, label):
        self.label = label

    def distance(self, other_sample):
        dist = (self.x-other_sample.get_x())**2 + \
            (self.y-other_sample.get_y())**2
        dist = dist**0.5
        return dist

    def __add__(self, other_sample):

        x = self.x + other_sample.get_x()
        y = self.y + other_sample.get_y()
        result = Sample(x, y, label="")
        return result

    def __sub__(self, other_sample):
        x = self.x - other_sample.get_x()
        y = self.y - other_sample.get_y()
        return Sample(x, y, label="")

    def power(self, n):
        # Complete the code
        # it returns an instance of Sample

        return Sample(self.x**n, self.y**n)

    def __truediv__(self, other):
        # Complete the code
        # it returns an instance of Sample
        if isinstance(other, Sample):
            return Sample(self.x/other.x, self.y/other.y)
        else:
            return Sample(self.x/other, self.y/other)

    def __str__(self):
        return f"[{self.get_x()}, {self.get_y()}]"


def compute_mean(samples: list):
    # Complete the code
    # it returns an instance of Sample
    mean_x, mean_y = 0, 0
    l = len(samples)
    for s in samples:
        mean_x += s.x
        mean_y += s.y
    return Sample(mean_x/l, mean_y/l)


def compute_std(samples, mean):
    # Complete the code
    # it returns an instance of Sample
    l = len(samples)
    var_x, var_y = 0, 0
    for s in samples:
        var_x += (s.x-mean.x)**2
        var_y += (s.y-mean.y)**2

    std_x = (var_x/l)**0.5
    std_y = (var_y/l)**0.5

    return Sample(std_x, std_y)


def standardization(samples):
    # Complete the code
    # it returns a list of instances of Sample
    mean = compute_mean(samples)
    std_x = compute_std(samples, mean).x
    std_y = compute_std(samples, mean).y
    for s in samples:
        s.x = (s.x-mean.x)/std_x
        s.y = (s.y-mean.y)/std_y
    return samples


if __name__ == "__main__":
    a = Sample(3, 4)
    b = Sample(1, 2)
    print("a =", a)
    print("b =", b)

    e = a.power(2)
    print("a.power(2) =", e)
    f = a/b
    print("a/b =", f)
    g = a/2
    print("a/2 =", g)

    # Tests for compute_mean, compute_std, and standardization
    samples = [a, b]
    mean = compute_mean(samples)
    print("mean:", mean)
    std = compute_std(samples, mean)
    print("std:", std)
    std_samples = standardization(samples)
    print("standardized samples:")
    if std_samples:
        print("a_std:", std_samples[0])
        print("b_std:", std_samples[1])
