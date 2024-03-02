#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 19:47:50 2024

@author: kehanluo
"""

from OOP_1 import Student


class MCM_Student(Student):
    '''A subclass of Student who attend MCM'''

    def curve(self):    # Students who attend MCM can get 5 bonus credit
        super().curve()
        if self.score <= 95:
            self.score += 5


class Leader(MCM_Student):
    '''A subclass of MCM_Student who are leaders'''

    # Leaders have new attribute members representing the members he is supervising
    def __init__(self, name, netID, score, members=None):
        super().__init__(name, netID, score)
        if members == None:
            self.members = []
        else:
            self.members = members

    def add_mem(self, mem):
        if mem not in self.members:
            self.members.append(mem)

    def remove_mem(self, mem):
        if mem in self.members:
            self.members.remove(mem)

    def print_mem(self):
        for mem in self.members:
            print('-->', mem.name)
            # print(mem.__dict__, end='\n'*2)


class Member(MCM_Student):
    '''A subclass of MCM_Student who are members'''

    # Members have new attribute pst representing the position of them in the team
    def __init__(self, name, netID, score, pst):
        super().__init__(name, netID, score)
        self.pst = pst


stu_1 = MCM_Student('Test User', 'abcd', 60)
stu_2 = Member('Rongyao Li', 'rl4785', 80, 'Model')
stu_3 = Member('Yuting Gao', 'yg2955', 80, 'Program')
stu_4 = Leader('Kehan Luo', 'kl4747', 80, [stu_2])


if __name__ == '__main__':
    pass
    # # Here is the code if I want to curve everyone again

    # for i in range(1, 5):
    #     stu = globals()[f'stu_{i}']
    #     stu.curve()
    #     print(stu.score)
