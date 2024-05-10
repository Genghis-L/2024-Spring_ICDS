#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021

@author: bing
"""

# import all the required  modules
# import os
# from tkinter_tic_tac_toe_module import start_game
import pickle
import threading
import select
from tkinter import *
from tkinter import font
import tkinter.messagebox as msgb
# from tkinter import ttk
from chat_utils import *
import json

# GUI class for the chat
class GUI:
    # def launch_tic_tac_toe(self):
    #     self.send({'action':'play_game', 'game':'tic_tac_toe'})
    #     start_game()
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()

        # self.buttonGame = Button(self.Window, text="Game!!!", font="Helvetica 10 bold", command=self.launch_tic_tac_toe)
        # self.buttonGame.pack(side=TOP, pady=10)

        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""

    def login(self):
        # Create a "login window"
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width = False, 
                             height = False)
        self.login.configure(width = 400,
                             height = 300)
        
        # Create a username label
        self.username = StringVar()
        self.label_username = Label(self.login,
                                    text="Username: ",
                                    font="Arial 12")
        self.label_username.place(relheight=0.15,
                                  relx=0.15,
                                  rely=0.07)
        # Create a password label
        self.password = StringVar()
        self.label_password = Label(self.login,
                                    text="Password: ",
                                    font="Arial 12")
        self.label_password.place(relheight=0.15,
                                  relx=0.15,
                                  rely=0.23)
        
        # Create "username" and "password" entry boxes
        self.entry_username = Entry(self.login,
                                    font="Arial 12",
                                    textvariable=self.username)
        self.entry_username.place(relwidth=0.4,
                                  relheight=0.1,
                                  relx=0.35,
                                  rely=0.1)

        self.entry_password = Entry(self.login,
                                    font="Arial 12",
                                    show="*",
                                    textvariable=self.password)
        self.entry_password.place(relwidth=0.4,
                                  relheight=0.1,
                                  relx=0.35,
                                  rely=0.25)
        # Set the focus of the curser
        self.entry_username.focus()
        
        # Create login and sign-up button
        self.login_button = Button(self.login,
                                   text="Log In",
                                   font="Arial 12",
                                   command=self.log_in)

        self.login_button.place(relwidth=0.2,
                                relheight=0.1,
                                relx=0.4,
                                rely=0.45)

        self.sign_button = Button(self.login,
                                  text="Sign Up",
                                  font="Arial 12",
                                  command=self.sign_up)

        self.sign_button.place(relwidth=0.2,
                               relheight=0.1,
                               relx=0.4,
                               rely=0.6)
        

        self.Window.mainloop()
        
        # create a Label
        self.pls = Label(self.login, 
                       text = "Please login to continue",
                       justify = CENTER, 
                       font = "Arial 14 bold")
          
        self.pls.place(relheight = 0.15,
                       relx = 0.2, 
                       rely = 0.10)
        # create a Label
        self.labelName = Label(self.login,
                               text = "Name: ",
                               font = "Arial 12")
          
        self.labelName.place(relheight = 0.2,
                             relx = 0.1, 
                             rely = 0.22)
          
        # create a entry box for 
        # tyoing the message
        self.entryName = Entry(self.login, 
                             font = "Arial 14")
          
        self.entryName.place(relwidth = 0.4, 
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.2)
          
        # set the focus of the curser
        self.entryName.focus()
          
        # create a Continue Button 
        # along with action
        self.go = Button(self.login,
                         text = "CONTINUE", 
                         font = "Arial 14 bold", 
                         command = lambda: self.goAhead(self.entryName.get()))
  
        self.go.place(relx = 0.4,
                      rely = 0.55)
        
        self.Window.mainloop()
        
    def sign_up(self):
        def sign_up():
            new_user = self.new_username.get()
            new_pwd = self.new_password.get()
            again_pwd = self.confirm_password.get()

            with open("all_users.pickle", "rb") as users_file:
                all_user = pickle.load(users_file)
                if new_user in all_user:
                    msgb.showerror(message="Username already exists.")
                else:
                    if new_pwd == again_pwd:
                        msgb.showinfo(message="Signup succeeded!")
                        all_user[new_user] = new_pwd
                        with open("all_users.pickle", "wb") as users_file:
                            pickle.dump(all_user, users_file)
                        self.window_sign_up.destroy()
                        self.goAhead(new_user)
                    else:
                        msgb.showerror(message="Please confirm your password again.")

        self.window_sign_up = Toplevel(self.login)
        self.window_sign_up.title("Signup")
        self.window_sign_up.configure(width=400,
                                      height=300)
        
        # new username label and entry
        self.new_username = StringVar()

        self.label_new_username = Label(self.window_sign_up,
                                        text="Username ",
                                        font="Helvetica 12")

        self.label_new_username.place(relheight=0.15,
                                      relx=0.2,
                                      rely=0.1)

        self.entry_username = Entry(self.window_sign_up,
                                    font="Helvetica 12",
                                    textvariable=self.new_username)

        self.entry_username.place(relwidth=0.4,
                                  relheight=0.1,
                                  relx=0.45,
                                  rely=0.1)

        # new password label and entry
        self.new_password = StringVar()

        self.label_new_password = Label(self.window_sign_up,
                                        text="Password ",
                                        font="Helvetica 12")

        self.label_new_password.place(relheight=0.15,
                                      relx=0.2,
                                      rely=0.25)

        self.entry_new_password = Entry(self.window_sign_up,
                                        font="Helvetica 12",
                                        show="*",
                                        textvariable=self.new_password)

        self.entry_new_password.place(relwidth=0.4,
                                      relheight=0.1,
                                      relx=0.45,
                                      rely=0.25)

        # confirm password label and entry
        self.confirm_password = StringVar()

        self.label_confirm_password = Label(self.window_sign_up,
                                            text="Password Again ",
                                            font="Helvetica 12")

        self.label_confirm_password.place(relheight=0.15,
                                          relx=0.1,
                                          rely=0.4
                                          )

        self.entry_password = Entry(self.window_sign_up,
                                    font="Helvetica 12",
                                    show="*",
                                    textvariable=self.confirm_password)

        self.entry_password.place(relwidth=0.4,
                                  relheight=0.1,
                                  relx=0.45,
                                  rely=0.4)

        # create a signup button
        self.signup_button = Button(self.window_sign_up,
                                    text="Sign up",
                                    font="Helvetica 12",
                                    command=sign_up)

        self.signup_button.place(relx=0.35,
                                 rely=0.65)

        self.window_sign_up.bind('<Return>', lambda event: sign_up())
        
    def log_in(self):
        self.log_in_username = self.username.get()
        self.log_in_password = self.password.get()

        self.users_file = open("all_users.pickle", "rb")
        self.all_users = pickle.load(self.users_file)
        self.users_file.close()

        if self.log_in_username in self.all_users:
            if self.log_in_password == self.all_users[self.log_in_username]:
                msgb.showinfo(message="Welcome, " + self.log_in_username + "!")
                self.login.destroy()
                self.goAhead(self.log_in_username)
            else:
                msgb.showerror(message="Password isn't correct! Please try again.")
        else:
            msgb.showerror(message="Username doesn't exist. Please sign up first.")
        
    def goAhead(self, name):
        if len(name) > 0:
            msg = json.dumps({"action":"login", "name": name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.textCons.config(state = NORMAL)
                # self.textCons.insert(END, "hello" +"\n\n")   
                self.textCons.insert(END, menu +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)
                # while True:
                #     self.proc()
        # the thread to receive messages
            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()
  
    # The main layout of the chat
    def layout(self,name):
        
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 550,
                              bg = "#17202A")
        self.labelHead = Label(self.Window,
                             bg = "#17202A", 
                              fg = "#EAECEE",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
          
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#ABB2B9")
          
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
          
        self.textCons = Text(self.Window,
                             width = 20, 
                             height = 2,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Helvetica 14", 
                             padx = 5,
                             pady = 5)
          
        self.textCons.place(relheight = 0.745,
                            relwidth = 1, 
                            rely = 0.08)
          
        self.labelBottom = Label(self.Window,
                                 bg = "#ABB2B9",
                                 height = 80)
          
        self.labelBottom.place(relwidth = 1,
                               rely = 0.825)
          
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
          
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
          
        self.entryMsg.focus()
          
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))
          
        self.buttonMsg.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.06, 
                             relwidth = 0.11)
        
        self.buttonG = Button(self.labelBottom,
                             text = "Game",
                             font="Helvetica 10 bold",
                             width=20,
                             bg="#ABB2B9",
                             command = self.start_game)
        self.buttonG.place(relx=0.88,
                              rely=0.008,
                              relheight=0.06,
                              relwidth=0.11)
          
        self.textCons.config(cursor = "arrow")
          
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
          
        # place the scroll bar 
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
          
        scrollbar.config(command = self.textCons.yview)
          
        self.textCons.config(state = DISABLED)
  
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)
    
    def start_game(self):
        self.my_msg = "request_to_start_a_game"
        
    
    def game_layout(self):
        self.gameWindow = Toplevel(self.Window)
        self.gameWindow.title('Tic-Tac-Toe')
        Label(self.gameWindow, text="Player 1 : X", font="times 18").grid(row=0, column=1)
        Label(self.gameWindow, text="Player 2 : O", font="times 18").grid(row=0, column=3)
        self.button1 = Button(self.gameWindow, width=15, height=7, font=('Times 16 bold'), command= self.checker1)
        self.button1.grid(row=1, column=1)
        self.button2 = Button(self.gameWindow, width=15, height=7, font=('Times 16 bold'), command= self.checker2)
        self.button2.grid(row=1, column=2)
        self.button3 = Button(self.gameWindow, width=15, height=7, font=('Times 16 bold'), command= self.checker3)
        self.button3.grid(row=1, column=3)
        self.button4 = Button(self.gameWindow, width=15, height=7, font=('Times 16 bold'), command= self.checker4)
        self.button4.grid(row=2, column=1)
        self.button5 = Button(self.gameWindow, width=15, height=7, font=('Times 16 bold'), command= self.checker5)
        self.button5.grid(row=2, column=2)
        self.button6 = Button(self.gameWindow, width=15, height=7, font=('Times 16 bold'), command= self.checker6)
        self.button6.grid(row=2, column=3)
        self.button7 = Button(self.gameWindow, width=15, height=7, font=('Times 16 bold'), command= self.checker7)
        self.button7.grid(row=3, column=1)
        self.button8 = Button(self.gameWindow, width=15, height=7, font=('Times 16 bold'), command= self.checker8)
        self.button8.grid(row=3, column=2)
        self.button9 = Button(self.gameWindow, width=15, height=7, font=('Times 16 bold'), command= self.checker9)
        self.button9.grid(row=3, column=3)
        
        
    def checker1(self):
        self.my_msg = "press_button_1"
    def checker2(self):
        self.my_msg = "press_button_2"
    def checker3(self):
        self.my_msg = "press_button_3"
    def checker4(self):
        self.my_msg = "press_button_4"
    def checker5(self):
        self.my_msg = "press_button_5"
    def checker6(self):
        self.my_msg = "press_button_6"
    def checker7(self):
        self.my_msg = "press_button_7"
    def checker8(self):
        self.my_msg = "press_button_8"
    def checker9(self):
        self.my_msg = "press_button_9"
    def play_again_dialog(self):
        


        choice = msgb.askquestion("Play Again", "Do you want to play again?")
        if choice == 'yes':
            self.gameWindow.destroy()
            self.start_game()
            # self.my_msg = "request_to_start_a_game"
        else:
            self.gameWindow.destroy()
    
    def proc(self):

        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # print(self.system_msg)
                               
                                        
                self.system_msg = self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = '' 
                if self.system_msg == "[Server]: Enjoy the game!":
                    self.game_layout()
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, self.system_msg + "\n\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
                    

                    
                elif self.system_msg[:11] == "systeminfo1":
                    self.button1.config(text=self.system_msg[11:])
                elif self.system_msg[:11] == "systeminfo2":
                    self.button2.config(text=self.system_msg[11:])
                elif self.system_msg[:11] == "systeminfo3":
                    self.button3.config(text=self.system_msg[11:])
                elif self.system_msg[:11] == "systeminfo4":
                    self.button4.config(text=self.system_msg[11:])
                elif self.system_msg[:11] == "systeminfo5":
                    self.button5.config(text=self.system_msg[11:])
                elif self.system_msg[:11] == "systeminfo6":
                    self.button6.config(text=self.system_msg[11:])
                elif self.system_msg[:11] == "systeminfo7":
                    self.button7.config(text=self.system_msg[11:])
                elif self.system_msg[:11] == "systeminfo8":
                    self.button8.config(text=self.system_msg[11:])
                elif self.system_msg[:11] == "systeminfo9":
                    self.button9.config(text=self.system_msg[11:])
                
                        
                
                elif self.system_msg == "serverinfoPlayer 1":
                    msgb.showinfo(title= "Result", message= "Player 1 wins the game!")
                
                    self.play_again_dialog()
                    
                    
                elif self.system_msg == "serverinfoPlayer 2":
                    msgb.showinfo(title= "Result", message= "Player 2 wins the game!")
                    self.play_again_dialog()
                    
                elif self.system_msg == "serverinfodraw":
                    msgb.showinfo(title= "Result", message= "This is a draw!")
                    self.play_again_dialog()
                    
                    
                    
                else: 
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, self.system_msg + "\n\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
                    
                   
            # print(self.msg)
            # if self.socket in read:
            #     peer_msg = self.recv()
            # if len(self.my_msg) > 0 or len(peer_msg) > 0:
            #     # print(self.system_msg)
            #     self.system_msg += self.sm.proc(self.my_msg, peer_msg)
            #     self.my_msg = ""
            #     self.textCons.config(state = NORMAL)
            #     self.textCons.insert(END, self.system_msg +"\n\n")      
            #     self.textCons.config(state = DISABLED)
            #     self.textCons.see(END)
        
    def run(self):
        self.login()
# create a GUI class object
if __name__ == "__main__": 
    g = GUI()