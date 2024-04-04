#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021

@author: bing
"""

# import all the required  modules
import pickle
import threading
import select
from tkinter import *
from tkinter import font, messagebox
# from tkinter import ttk
from chat_utils import *
import json


# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""

    def login(self):
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=400,
                             height=300)

        # create username Label
        self.username = StringVar()
        self.label_username = Label(self.login,
                                    text="Username: ",
                                    font="Helvetica 12")
        self.label_username.place(relheight=0.15,
                                  relx=0.15,
                                  rely=0.07)

        # create password Label
        self.password = StringVar()
        self.label_password = Label(self.login,
                                    text="Password: ",
                                    font="Helvetica 12")
        self.label_password.place(relheight=0.15,
                                  relx=0.15,
                                  rely=0.23)

        # create two entry boxes
        self.entry_username = Entry(self.login,
                                    font="Helvetica 12",
                                    textvariable=self.username)
        self.entry_username.place(relwidth=0.4,
                                  relheight=0.1,
                                  relx=0.35,
                                  rely=0.1)

        self.entry_password = Entry(self.login,
                                    font="Helvetica 12",
                                    show="*",
                                    textvariable=self.password)
        self.entry_password.place(relwidth=0.4,
                                  relheight=0.1,
                                  relx=0.35,
                                  rely=0.25)

        # set the focus of the curser
        self.entry_username.focus()
        self.entry_password.focus()

        # create login and signup Button
        self.login_button = Button(self.login,
                                   text="Log In",
                                   font="Helvetica 14",
                                   fg="GREEN",
                                   command=self.log_in)

        self.login_button.place(relwidth=0.2,
                                relheight=0.1,
                                relx=0.4,
                                rely=0.45)

        self.sign_button = Button(self.login,
                                  text="Sign Up",
                                  font="Helvetica 12",
                                  command=self.sign_up)

        self.sign_button.place(relwidth=0.2,
                               relheight=0.1,
                               relx=0.4,
                               rely=0.6)

        self.login.bind('<Return>', lambda event: self.log_in())

        self.Window.mainloop()

    def __log_in(self):
        self.log_in_username = 'lu'
        self.log_in_password = 'lu'

        self.users_file = open("all_users.pickle", "rb")
        self.all_users = pickle.load(self.users_file)
        self.users_file.close()

        if self.log_in_username in self.all_users:
            if self.log_in_password == self.all_users[self.log_in_username]:
                messagebox.showinfo(message="Welcome, " + self.log_in_username + "!")
                self.login.destroy()
                self.goAhead(self.log_in_username)
            else:
                messagebox.showerror(message="Wrong password! Please try again.")
        else:
            messagebox.showerror(message="Username does not exist. Please sign up first.")

    def _log_in(self):
        self.log_in_username = 'steve'
        self.log_in_password = 'steve'

        self.users_file = open("all_users.pickle", "rb")
        self.all_users = pickle.load(self.users_file)
        self.users_file.close()

        if self.log_in_username in self.all_users:
            if self.log_in_password == self.all_users[self.log_in_username]:
                messagebox.showinfo(message="Welcome, " + self.log_in_username + "!")
                self.login.destroy()
                self.goAhead(self.log_in_username)
            else:
                messagebox.showerror(message="Wrong password! Please try again.")
        else:
            messagebox.showerror(message="Username does not exist. Please sign up first.")

    def sign_up(self):
        def sign_up():
            new_user = self.new_username.get()
            new_pwd = self.new_password.get()
            confirm_pwd = self.confirm_password.get()

            with open("all_users.pickle", "rb") as users_file:
                all_user = pickle.load(users_file)
                if new_user in all_user:
                    messagebox.showerror(message="Username exists.")
                else:
                    if new_pwd == confirm_pwd:
                        messagebox.showinfo(message="Signup succeeded. Automatically sign you in!")
                        all_user[new_user] = new_pwd
                        with open("all_users.pickle", "wb") as users_file:
                            pickle.dump(all_user, users_file)
                        self.window_sign_up.destroy()
                        self.goAhead(new_user)
                    else:
                        messagebox.showerror(message="Please confirm your password again.")

        self.window_sign_up = Toplevel(self.login)
        self.window_sign_up.title("Signup")
        self.window_sign_up.configure(width=400,
                                      height=300)

        # new username label and entry
        self.new_username = StringVar()

        self.label_new_username = Label(self.window_sign_up,
                                        text="Username: ",
                                        font="Helvetica 12")

        self.label_new_username.place(relheight=0.15,
                                      relx=0.1,
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
                                        text="Password: ",
                                        font="Helvetica 12")

        self.label_new_password.place(relheight=0.15,
                                      relx=0.1,
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
                                            text="Confirm Password: ",
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
                messagebox.showinfo(message="Welcome, " + self.log_in_username + "!")
                self.login.destroy()
                self.goAhead(self.log_in_username)
            else:
                messagebox.showerror(message="Wrong password! Please try again.")
        else:
            messagebox.showerror(message="Username does not exist. Please sign up first.")

    def goAhead(self, name):
        if len(name) > 0:
            msg = json.dumps({"action": "login", "name": name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.sm.generate_key_pairs()
                self.layout(name)
                self.textCons1.config(state=NORMAL)
                # self.textCons1.insert(END, "hello" +"\n\n")
                self.textCons1.insert(END, menu + "\n\n")
                self.textCons1.config(state=DISABLED)
                self.textCons1.see(END)
                # while True:
                #     self.proc()
            # the thread to receive messages
            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()

    # The main layout of the chat
    def layout(self, name):

        self.name = name

        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=True,
                              height=True)
        self.Window.configure(width=700,
                              height=800,
                              bg="#141615")

        self.labelHead = Label(self.Window,
                               bg="#DEDEDE",
                               fg="#141615",
                               text=self.name + '\'s Chatroom \n' + 'Choose one of the following commands\n' +
                                    'time: calendar time in the system\n' + 'who: to find out who else are there\n' +
                                    'c _peer_: to connect to the _peer_ and chat\n' + '? _term_: to search your chat logs where _term_ appears\n' +
                                    'p _#_: to get number <#> sonnet\n' + 'q: to leave the chat system',
                               font="Helvetica 14 bold"
                               )
        self.labelHead.place(relwidth=1,
                             relheight=0.17)

        self.textCons1 = Text(self.Window,
                              width=20,
                              height=2,
                              bg="#F2F2F2",
                              fg="#163dba",
                              font="Helvetica 14",
                              padx=5,
                              pady=5)

        self.textCons1.place(relheight=0.73,
                             relwidth=0.5,
                             rely=0.17)

        self.textCons2 = Text(self.Window,
                              width=20,
                              height=2,
                              bg="#F2F2F2",
                              fg="black",
                              font="Helvetica 14",
                              padx=5,
                              pady=5)

        self.textCons2.place(relheight=0.73,
                             relwidth=0.5,
                             relx=0.5,
                             rely=0.17)

        self.labelBottom = Label(self.Window,
                                 bg="#DEDEDE")

        self.labelBottom.place(relwidth=1,
                               relheight=0.08,
                               rely=0.85)

        self.entryMsg = Entry(self.labelBottom,
                              bg="#F2F2F2",
                              fg="#141516",
                              font="Helvetica 14")

        self.entryMsg.place(relwidth=0.74,
                            relheight=0.6,
                            relx=0.011,
                            rely=0.2)

        self.entryMsg.focus()

        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 15 bold",
                                width=20,
                                bg="#DEDEDE",
                                fg='GREEN',
                                highlightbackground='GREEN',
                                command=lambda: self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relwidth=0.22,
                             relheight=0.6,
                             relx=0.76,
                             rely=0.2)

        self.labelAboveBottom = Label(self.Window,
                                      bg="#DEDEDE")

        self.labelAboveBottom.place(relwidth=1,
                                    relheight=0.07,
                                    relx=0,
                                    rely=0.92)

        # create a quit Button
        self.buttonQuit = Button(self.labelAboveBottom,
                                 text="Quit",
                                 font="Helvetica 15 bold",
                                 bg="#FFFFFF",
                                 fg="RED",
                                 command=lambda: self.sendButton('q'))

        self.buttonQuit.place(relx=0.695,
                              rely=0.125,
                              relwidth=0.26,
                              relheight=0.75)

        self.buttonGame = Button(self.labelAboveBottom,
                                 text="Game",
                                 font="Helvetica 15 bold",
                                 bg="red",
                                 command=lambda: self.sendButton('game'))

        self.buttonGame.place(relx=0.5,
                              rely=0.5,
                              anchor='center',
                              relwidth=0.26,
                              relheight=0.75)

        self.buttonBye = Button(self.labelAboveBottom,
                                text="Bye",
                                font="Helvetica 15 bold",
                                bg="#DEDEDE",
                                command=lambda: self.sendButton('bye'))

        self.buttonBye.place(relx=0.055,
                             rely=0.125,
                             anchor='nw',
                             relwidth=0.26,
                             relheight=0.75)

        self.Window.bind('<Return>', lambda event: self.sendButton(self.entryMsg.get()))

        # create emoji buttons
        emoji_list = ["\U0001F600", "\U0001F604", "\U0001F601", "\U0001F606", "\U0001F605", "\U0001F923", "\U0001F602",
                      "\U0001F642", "\U0001F643", "\U0001F609", "\U0001F607", "\U0001F970", "\U0001F929", "\U0001F618",
                      "\U0001F617", "\U0001F619", "\U0001F60B", "\U0001F61D", "\U0001F917", "\U0001F92D"]
        other_emoji = ["\U0001F92B", "\U0001F914", "\U0001F910", "\U0001F928", "\U0001F610", "\U0001F611", "\U0001F636", "\U0001F644",
                      "\U0001F925", "\U0001F62A"]

        e_fg = "#141516"
        e_bg = "#DEDEDE"
        e_font = "Helvetica 15"

        for index, emoji in enumerate(emoji_list):
            button_name = f'emoji_button{index}'
            setattr(self, button_name, Button(self.Window, text=emoji, fg=e_fg, bg=e_bg, font=e_font,
                                              command=lambda e=emoji: self.insert_emoji(e)))

        emoji_button_height = 0.06
        emoji_button_width = 0.1
        x_start = 0
        y_start = 0.73

        for row in range(3):
            for col in range(10):
                index = row * 10 + col
                if index > 19:
                    break
                emoji_button = getattr(self, f"emoji_button{index}")
                emoji_button.place(relx=x_start + col * emoji_button_width, rely=y_start + row * emoji_button_height,
                                   relheight=emoji_button_height, relwidth=emoji_button_width)

        self.textCons1.config(cursor="arrow")

        '''
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons1)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.68)

        scrollbar.config(command=self.textCons1.yview)

        self.textCons1.config(state=DISABLED)
        '''

    # function to basically start the thread for sending messages

    def sendButton(self, msg):
        # self.textCons2.config(state=DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)
        self.textCons2.config(state=NORMAL)
        self.textCons2.insert(END, '\n' + msg + "\n\n\n\n")
        self.textCons2.config(state=DISABLED)
        self.textCons2.see(END)

    def proc(self):
        # print(self.msg)

        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []

            if self.socket in read:
                peer_msg = self.recv()

            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                self.system_msg = self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons1.config(state=NORMAL)
                self.textCons1.insert(END, self.system_msg + '\n')
                self.textCons1.config(state=DISABLED)
                self.textCons1.see(END)

    def run(self):
        self.login()

    def insert_emoji(self, emoji_arg):
        self.entryMsg.insert("end", emoji_arg)


# create a GUI class object
if __name__ == "__main__":
    # g = GUI()
    pass
