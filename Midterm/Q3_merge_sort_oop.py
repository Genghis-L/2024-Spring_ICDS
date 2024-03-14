#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 17:01:12 2024

@author: bing
"""


class Node():

    def __init__(self, num_lst):
        self.numbers = num_lst

    def set_numbers(self, new_lst):
        self.numbers = new_lst

    def get_numbers(self):
        return self.numbers

    def __getitem__(self, idx):
        if 0 <= idx < self.length():
            return self.numbers[idx]
        else:
            print('Index Error')

    def length(self):
        return len(self.numbers)

    def divide(self):
        if self.length() == 1:
            return Node(self.numbers), Node([])
        pivot = self.length() // 2
        left_list = [self[index] for index in range(0, pivot)]
        right_list = [self[index] for index in range(pivot, self.length())]
        return Node(left_list), Node(right_list)

    def add_elements(self, numbers):
        if isinstance(numbers, list):
            self.numbers.extend(numbers)
        elif isinstance(numbers, int):
            self.numbers.append(numbers)
        else:
            raise ValueError

    def __str__(self):
        return str(self.numbers)

    def merge(self, other_node):
        new_node = Node([])
        i = j = 0
        while i < self.length() and j < other_node.length():
            left_value, right_value = self[i], other_node[j]
            if left_value < right_value:
                new_node.add_elements(left_value)
                i += 1
            else:
                new_node.add_elements(right_value)
                j += 1

        if i < self.length():
            new_node.add_elements(self.numbers[i:self.length()])
        elif j < other_node.length():
            new_node.add_elements(other_node.numbers[j:other_node.length()])

        return new_node


# Merge sort using Node class
def merge_sort(node):
    if node.length() <= 1:
        return node
    left_child, right_child = node.divide()
    left_child = merge_sort(left_child)
    right_child = merge_sort(right_child)
    return left_child.merge(right_child)


if __name__ == "__main__":
    # Tests of Node class
    CHECK_ON = False
    if CHECK_ON:
        node = Node([5, 3, 4, 2, 1])
        print(node.numbers)
        print(node.get_numbers())
        node.set_numbers([3, 6, 2, 8, 1])
        print(node.get_numbers())
        print(node[1])
        print(node.length())
        print(node)
        left, right = node.divide()
        print(left)
        print(right)
        node.add_elements([1, 2, 3])
        node.add_elements(10)
        print(node.get_numbers())
        node_1 = Node([1, 3, 5])
        node_2 = Node([2, 4, 6])
        result = node_1.merge(node_2)
        print(result)
        node_3 = Node([2, 4, 8])
        node_4 = Node([1, 3, 9, 10, 15])
        result = node_3.merge(node_4)
        print(result)

    # Test of merge sort
    import random
    random.seed("Midterm")
    randomized_lists_merge = []
    print("Generating randomized lists for sorting...")
    LIMIT = 10
    randomized_lists_merge = [random.randint(0, i + 1) for i in range(LIMIT)]
    print("The randomly generated list is: ", randomized_lists_merge)
    print("Sorting")
    root = Node(randomized_lists_merge)
    merge_sorted_list = merge_sort(root)
    print("merge sort: ", merge_sorted_list)
