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
from tkinter import ttk
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
                                  relx=0.1,
                                  rely=0.1)

        # create password Label
        self.password = StringVar()

        self.label_password = Label(self.login,
                                    text="Password: ",
                                    font="Helvetica 12")

        self.label_password.place(relheight=0.15,
                                  relx=0.1,
                                  rely=0.25)

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
                                   font="Helvetica 12",
                                   command=self.log_in)

        self.login_button.place(relx=0.1,
                                rely=0.45)

        self.sign_button = Button(self.login,
                                  text="Sign Up",
                                  font="Helvetica 12",
                                  command=self.sign_up)

        self.sign_button.place(relx=0.4,
                               rely=0.45)

        self.Window.mainloop()

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
                        messagebox.showinfo(message="Signup succeeded. Please log in.")
                        all_user[new_user] = new_pwd
                        with open("all_users.pickle", "wb") as users_file:
                            pickle.dump(all_user, users_file)
                        self.window_sign_up.destroy()
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
                self.textCons.config(state=NORMAL)
                # self.textCons.insert(END, "hello" +"\n\n")
                self.textCons.insert(END, menu + "\n\n")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)
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
        self.Window.configure(width=800,
                              height=550,
                              bg="#DEDEDE")

        self.labelHead = Label(self.Window,
                               bg="#DEDEDE",
                               fg="#141615",
                               text=self.name + '\'s chatroom',
                               font="Helvetica 14 bold",
                               pady=5)

        self.labelHead.place(relwidth=1)

        self.line = Label(self.Window,
                          width=450,
                          bg="#DEDEDE")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#F2F2F2",
                             fg="#141615",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)

        self.labelBottom = Label(self.Window,
                                 bg="#DEDEDE",
                                 height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg="#F2F2F2",
                              fg="#141516",
                              font="Helvetica 14")

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)

        self.entryMsg.focus()

        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 15 bold",
                                width=20,
                                bg="#DEDEDE",
                                command=lambda: self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)

        # create emoji buttons
        emoji_list = ["\U0001F600", "\U0001F604", "\U0001F601", "\U0001F606", "\U0001F605", "\U0001F923", "\U0001F602",
                      "\U0001F642", "\U0001F643", "\U0001F609", "\U0001F607", "\U0001F970", "\U0001F929", "\U0001F618",
                      "\U0001F617", "\U0001F619", "\U0001F60B", "\U0001F61D", "\U0001F917", "\U0001F92D", "\U0001F92B",
                      "\U0001F914", "\U0001F910", "\U0001F928", "\U0001F610", "\U0001F611", "\U0001F636", "\U0001F644",
                      "\U0001F925", "\U0001F62A"]

        dic = {}
        for i in range(30):
            dic["e{}".format(i + 1)] = emoji_list[i]

        def e1():
            self.entryMsg.insert("end", dic['e1'])
            return

        def e2():
            self.entryMsg.insert("end", dic['e2'])
            return

        def e3():
            self.entryMsg.insert("end", dic['e3'])
            return

        def e4():
            self.entryMsg.insert("end", dic['e4'])
            return

        def e5():
            self.entryMsg.insert("end", dic['e5'])
            return

        def e6():
            self.entryMsg.insert("end", dic['e6'])
            return

        def e7():
            self.entryMsg.insert("end", dic['e7'])
            return

        def e8():
            self.entryMsg.insert("end", dic['e8'])
            return

        def e9():
            self.entryMsg.insert("end", dic['e9'])
            return

        def e10():
            self.entryMsg.insert("end", dic['e10'])
            return

        def e11():
            self.entryMsg.insert("end", dic['e11'])
            return

        def e12():
            self.entryMsg.insert("end", dic['e12'])
            return

        def e13():
            self.entryMsg.insert("end", dic['e13'])
            return

        def e14():
            self.entryMsg.insert("end", dic['e14'])
            return

        def e15():
            self.entryMsg.insert("end", dic['e15'])
            return

        def e16():
            self.entryMsg.insert("end", dic['e16'])
            return

        def e17():
            self.entryMsg.insert("end", dic['e17'])
            return

        def e18():
            self.entryMsg.insert("end", dic['e18'])
            return

        def e19():
            self.entryMsg.insert("end", dic['e19'])
            return

        def e20():
            self.entryMsg.insert("end", dic['e20'])
            return

        def e21():
            self.entryMsg.insert("end", dic['e21'])
            return

        def e22():
            self.entryMsg.insert("end", dic['e22'])
            return

        def e23():
            self.entryMsg.insert("end", dic['e23'])
            return

        def e24():
            self.entryMsg.insert("end", dic['e24'])
            return

        def e25():
            self.entryMsg.insert("end", dic['e25'])
            return

        def e26():
            self.entryMsg.insert("end", dic['e26'])
            return

        def e27():
            self.entryMsg.insert("end", dic['e27'])
            return

        def e28():
            self.entryMsg.insert("end", dic['e28'])
            return

        def e29():
            self.entryMsg.insert("end", dic['e29'])
            return

        def e30():
            self.entryMsg.insert("end", dic['e30'])
            return

        e_fg = "#141516"
        e_bg = "#DEDEDE"
        e_font = "Helvetica 15"
        self.emoji_button1 = Button(self.Window, text=dic['e1'], fg=e_fg, bg=e_bg, command=e1, font=e_font)
        self.emoji_button2 = Button(self.Window, text=dic['e2'], fg=e_fg, bg=e_bg, command=e2, font=e_font)
        self.emoji_button3 = Button(self.Window, text=dic['e3'], fg=e_fg, bg=e_bg, command=e3, font=e_font)
        self.emoji_button4 = Button(self.Window, text=dic['e4'], fg=e_fg, bg=e_bg, command=e4, font=e_font)
        self.emoji_button5 = Button(self.Window, text=dic['e5'], fg=e_fg, bg=e_bg, command=e5, font=e_font)
        self.emoji_button6 = Button(self.Window, text=dic['e6'], fg=e_fg, bg=e_bg, command=e6, font=e_font)
        self.emoji_button7 = Button(self.Window, text=dic['e7'], fg=e_fg, bg=e_bg, command=e7, font=e_font)
        self.emoji_button8 = Button(self.Window, text=dic['e8'], fg=e_fg, bg=e_bg, command=e8, font=e_font)
        self.emoji_button9 = Button(self.Window, text=dic['e9'], fg=e_fg, bg=e_bg, command=e9, font=e_font)
        self.emoji_button10 = Button(self.Window, text=dic['e10'], fg=e_fg, bg=e_bg, command=e10, font=e_font)
        self.emoji_button11 = Button(self.Window, text=dic['e11'], fg=e_fg, bg=e_bg, command=e11, font=e_font)
        self.emoji_button12 = Button(self.Window, text=dic['e12'], fg=e_fg, bg=e_bg, command=e12, font=e_font)
        self.emoji_button13 = Button(self.Window, text=dic['e13'], fg=e_fg, bg=e_bg, command=e13, font=e_font)
        self.emoji_button14 = Button(self.Window, text=dic['e14'], fg=e_fg, bg=e_bg, command=e14, font=e_font)
        self.emoji_button15 = Button(self.Window, text=dic['e15'], fg=e_fg, bg=e_bg, command=e15, font=e_font)
        self.emoji_button16 = Button(self.Window, text=dic['e16'], fg=e_fg, bg=e_bg, command=e16, font=e_font)
        self.emoji_button17 = Button(self.Window, text=dic['e17'], fg=e_fg, bg=e_bg, command=e17, font=e_font)
        self.emoji_button18 = Button(self.Window, text=dic['e18'], fg=e_fg, bg=e_bg, command=e18, font=e_font)
        self.emoji_button19 = Button(self.Window, text=dic['e19'], fg=e_fg, bg=e_bg, command=e19, font=e_font)
        self.emoji_button20 = Button(self.Window, text=dic['e20'], fg=e_fg, bg=e_bg, command=e20, font=e_font)
        self.emoji_button21 = Button(self.Window, text=dic['e21'], fg=e_fg, bg=e_bg, command=e21, font=e_font)
        self.emoji_button22 = Button(self.Window, text=dic['e22'], fg=e_fg, bg=e_bg, command=e22, font=e_font)
        self.emoji_button23 = Button(self.Window, text=dic['e23'], fg=e_fg, bg=e_bg, command=e23, font=e_font)
        self.emoji_button24 = Button(self.Window, text=dic['e24'], fg=e_fg, bg=e_bg, command=e24, font=e_font)
        self.emoji_button25 = Button(self.Window, text=dic['e25'], fg=e_fg, bg=e_bg, command=e25, font=e_font)
        self.emoji_button26 = Button(self.Window, text=dic['e26'], fg=e_fg, bg=e_bg, command=e26, font=e_font)
        self.emoji_button27 = Button(self.Window, text=dic['e27'], fg=e_fg, bg=e_bg, command=e27, font=e_font)
        self.emoji_button28 = Button(self.Window, text=dic['e28'], fg=e_fg, bg=e_bg, command=e28, font=e_font)
        self.emoji_button29 = Button(self.Window, text=dic['e29'], fg=e_fg, bg=e_bg, command=e29, font=e_font)
        self.emoji_button30 = Button(self.Window, text=dic['e30'], fg=e_fg, bg=e_bg, command=e30, font=e_font)

        emoji_button_height = 0.075
        emoji_button_width = 0.1
        self.emoji_button1.place(relx=0.7, rely=0.078, relheight=emoji_button_height, relwidth=emoji_button_width)
        self.emoji_button2.place(relx=0.8, rely=0.078, relheight=emoji_button_height, relwidth=emoji_button_width)
        self.emoji_button3.place(relx=0.9, rely=0.078, relheight=emoji_button_height, relwidth=emoji_button_width)
        self.emoji_button4.place(relx=0.7, rely=0.078 + emoji_button_height, relheight=emoji_button_height,
                                 relwidth=emoji_button_width)
        self.emoji_button5.place(relx=0.8, rely=0.078 + emoji_button_height, relheight=emoji_button_height,
                                 relwidth=emoji_button_width)
        self.emoji_button6.place(relx=0.9, rely=0.078 + emoji_button_height, relheight=emoji_button_height,
                                 relwidth=emoji_button_width)
        self.emoji_button7.place(relx=0.7, rely=0.078 + emoji_button_height * 2, relheight=emoji_button_height,
                                 relwidth=emoji_button_width)
        self.emoji_button8.place(relx=0.8, rely=0.078 + emoji_button_height * 2, relheight=emoji_button_height,
                                 relwidth=emoji_button_width)
        self.emoji_button9.place(relx=0.9, rely=0.078 + emoji_button_height * 2, relheight=emoji_button_height,
                                 relwidth=emoji_button_width)
        self.emoji_button10.place(relx=0.7, rely=0.078 + emoji_button_height * 3, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)
        self.emoji_button11.place(relx=0.8, rely=0.078 + emoji_button_height * 3, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)
        self.emoji_button12.place(relx=0.9, rely=0.078 + emoji_button_height * 3, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)
        self.emoji_button13.place(relx=0.7, rely=0.078 + emoji_button_height * 4, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)
        self.emoji_button14.place(relx=0.8, rely=0.078 + emoji_button_height * 4, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)
        self.emoji_button15.place(relx=0.9, rely=0.078 + emoji_button_height * 4, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)
        self.emoji_button16.place(relx=0.7, rely=0.078 + emoji_button_height * 5, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)
        self.emoji_button17.place(relx=0.8, rely=0.078 + emoji_button_height * 5, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)
        self.emoji_button18.place(relx=0.9, rely=0.078 + emoji_button_height * 5, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)
        self.emoji_button19.place(relx=0.7, rely=0.078 + emoji_button_height * 6, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)
        self.emoji_button20.place(relx=0.8, rely=0.078 + emoji_button_height * 6, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)
        self.emoji_button21.place(relx=0.9, rely=0.078 + emoji_button_height * 6, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)
        self.emoji_button22.place(relx=0.7, rely=0.078 + emoji_button_height * 7, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)
        self.emoji_button23.place(relx=0.8, rely=0.078 + emoji_button_height * 7, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)
        self.emoji_button24.place(relx=0.9, rely=0.078 + emoji_button_height * 7, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)
        self.emoji_button25.place(relx=0.7, rely=0.078 + emoji_button_height * 8, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)
        self.emoji_button26.place(relx=0.8, rely=0.078 + emoji_button_height * 8, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)
        self.emoji_button27.place(relx=0.9, rely=0.078 + emoji_button_height * 8, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)
        self.emoji_button28.place(relx=0.7, rely=0.078 + emoji_button_height * 9, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)
        self.emoji_button29.place(relx=0.8, rely=0.078 + emoji_button_height * 9, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)
        self.emoji_button30.place(relx=0.9, rely=0.078 + emoji_button_height * 9, relheight=emoji_button_height,
                                  relwidth=emoji_button_width)

        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.68)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    # function to basically start the thread for sending messages

    def sendButton(self, msg):
        # self.textCons.config(state=DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, msg + "\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    def proc(self):
        # print(self.msg)
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            # print(self.msg)
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # print(self.system_msg)
                self.system_msg = self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons.config(state=NORMAL)
                self.textCons.insert(END, self.system_msg + "\n\n")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)

    def run(self):
        self.login()


# create a GUI class object
if __name__ == "__main__":
    # g = GUI()
    pass
