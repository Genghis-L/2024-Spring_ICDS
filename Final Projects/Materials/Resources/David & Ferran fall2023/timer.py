#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 01:06:34 2022

@author: bing
"""

import time
from tkinter import *
from tkinter import messagebox
import threading
 

class Timer():
    def __init__(self, parent):
        self.parent = parent
        self.hour = StringVar()
        self.minute = StringVar()
        self.second = StringVar()
        self.hour.set("00")
        self.minute.set("00")
        self.second.set("00")
        
        self.hourEntry = Entry(parent, width=3, font=("Arial", 18, ""), textvariable=self.hour)
        self.hourEntry.place(x=80, y=20)
        self.minuteEntry = Entry(parent, width=3, font=("Arial", 18, ""), textvariable=self.minute)
        self.minuteEntry.place(x=130, y=20)
        self.secondEntry = Entry(parent, width=3, font=("Arial", 18, ""), textvariable=self.second)
        self.secondEntry.place(x=180, y=20)
        self.start_button = Button(parent, text='Set Time Countdown', bd='5',
                     command=lambda:self.process_start(self.hour, self.minute, self.second))
        self.start_button.place(x = 70, y = 100)    

        self.hour2 = StringVar()
        self.minute2 = StringVar()
        self.second2 = StringVar()
        self.hour2.set("00")
        self.minute2.set("00")
        self.second2.set("00")
        self.hourEntry2 = Entry(parent, width=3, font=("Arial", 18, ""), textvariable=self.hour2)
        self.hourEntry2.place(x=80, y=180)
        self.minuteEntry2 = Entry(parent, width=3, font=("Arial", 18, ""), textvariable=self.minute2)
        self.minuteEntry2.place(x=130, y=180)
        self.secondEntry2 = Entry(parent, width=3, font=("Arial", 18, ""), textvariable=self.second2)
        self.secondEntry2.place(x=180, y=180)
        self.start_button2 = Button(parent, text='Set Time Countdown', bd='5',
                     command= lambda:self.process_start(self.hour2, self.minute2, self.second2))
        self.start_button2.place(x = 70, y = 260)         
    
    def start(self, hour, minute, second):
        try:
            # the input provided by the user is
            # stored in here :temp
            temp = int(hour.get())*3600 + int(minute.get())*60 + int(second.get())
        except:
            print("Please input the right value")
            
        while temp >-1:
            # divmod(firstvalue = temp//60, secondvalue = temp%60)
            mins,secs = divmod(temp, 60)
            # Converting the input entered in mins or secs to hours,
            # mins ,secs(input = 110 min --> 120*60 = 6600 => 1hr :
            # 50min: 0sec)
            hours=0
            if mins >60:       
                # divmod(firstvalue = temp//60, secondvalue
                # = temp%60)
                hours, mins = divmod(mins, 60)
            # using format () method to store the value up to
            # two decimal places
            hour.set("{0:2d}".format(hours))
            minute.set("{0:2d}".format(mins))
            second.set("{0:2d}".format(secs))
            # updating the GUI window after decrementing the
            # temp value every time
            self.parent.update()
            time.sleep(1)
            # when temp value = 0; then a messagebox pop's up
            # with a message:"Time's up"
            if (temp == 0):
                messagebox.showinfo("Time Countdown", "Time's up ")
            # after every one sec the value of temp will be decremented
            # by one
            temp -= 1
    
    def process_start(self, hour, minute, second):
        process = threading.Thread(target=lambda : self.start(hour, minute, second))
        process.daemon = True
        process.start()

    
        
 
# creating Tk window
root = Tk()
  
# setting geometry of tk window
root.geometry("300x300")
  
# Using title() to display a message in
# the dialogue box of the message in the
# title bar.
root.title("Time Counter")

app = Timer(root)
root.mainloop()