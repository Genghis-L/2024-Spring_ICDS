#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021

@author: bing
"""

# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from chat_utils import *
import json


class GUI:
    def __init__(self, send, recv, sm, s):
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""
        self.entryName = None
        self.entryPassword = None
        self.load_registered_users()

    def load_registered_users(self):
        try:
            with open("registered_users.json", "r") as file:
                self.reg_names = json.load(file)
        except FileNotFoundError:
            self.reg_names = {}

    def save_registered_users(self):
        with open("registered_users.json", "w") as file:
            json.dump(self.reg_names, file)

    def login(self):
        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)

        self.pls = Label(
            self.login,
            text="Please login to continue",
            justify=CENTER,
            font="Helvetica 14 bold",
        )
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        self.labelUsername_login = Label(self.login, text="Name: ", font="Helvetica 12")
        self.labelUsername_login.place(relheight=0.2, relx=0.1, rely=0.2)

        self.entryUsername_login = Entry(self.login, font="Helvetica 14")
        self.entryUsername_login.place(
            relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2
        )

        self.labelPassword_login = Label(
            self.login, text="Password: ", font="Helvetica 12"
        )
        self.labelPassword_login.place(relheight=0.2, relx=0.1, rely=0.4)

        self.entryPassword_login = Entry(self.login, font="Helvetica 14", show="*")
        self.entryPassword_login.place(
            relwidth=0.4, relheight=0.12, relx=0.35, rely=0.4
        )

        self.entryUsername_login.focus()

        self.loginButton = Button(
            self.login,
            text="LOGIN",
            font="Helvetica 14 bold",
            command=lambda: self.goAhead(
                self.entryUsername_login.get(), self.entryPassword_login.get()
            ),
        )
        self.loginButton.place(relx=0.3, rely=0.55)

        self.signUpButton = Button(
            self.login,
            text="SIGN UP",
            font="Helvetica 14 bold",
            command=self.signUpWindow,
        )
        self.signUpButton.place(relx=0.6, rely=0.55)
        self.load_registered_users()
        self.Window.mainloop()

    def signUpWindow(self):
        self.signup = Toplevel()
        self.signup.title("Sign Up")
        self.signup.resizable(width=False, height=False)
        self.signup.configure(width=400, height=300)

        self.labelUsername_signup = Label(
            self.signup, text="Username: ", font="Helvetica 12"
        )
        self.labelUsername_signup.place(relheight=0.2, relx=0.1, rely=0.2)

        self.entryUsername_signup = Entry(self.signup, font="Helvetica 14")
        self.entryUsername_signup.place(
            relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2
        )

        self.labelPassword_signup = Label(
            self.signup, text="Password: ", font="Helvetica 12"
        )
        self.labelPassword_signup.place(relheight=0.2, relx=0.1, rely=0.4)

        self.entryPassword_signup = Entry(self.signup, font="Helvetica 14", show="*")
        self.entryPassword_signup.place(
            relwidth=0.4, relheight=0.12, relx=0.35, rely=0.4
        )

        self.labelConfirmPassword_signup = Label(
            self.signup, text="Confirm Password: ", font="Helvetica 12"
        )
        self.labelConfirmPassword_signup.place(relheight=0.2, relx=0.1, rely=0.6)

        self.entryConfirmPassword_signup = Entry(
            self.signup, font="Helvetica 14", show="*"
        )
        self.entryConfirmPassword_signup.place(
            relwidth=0.4, relheight=0.12, relx=0.35, rely=0.6
        )

        self.signUpButton = Button(
            self.signup, text="SIGN UP", font="Helvetica 14 bold", command=self.signUp
        )
        self.signUpButton.place(relx=0.4, rely=0.8)

    def signUp(self):

        username = self.entryUsername_signup.get()
        password = self.entryPassword_signup.get()
        confirm_password = self.entryConfirmPassword_signup.get()

        # Check if the user exists already
        if username in self.reg_names.keys():
            messagebox.showerror("Error", "The user exists already!")
            return

        # Check if password meets criteria
        if len(password) < 6:
            messagebox.showerror(
                "Error", "Please use passwords equal to or longer than 6 characters!"
            )
            return

        # Check if passwords match
        if password != confirm_password:
            messagebox.showerror(
                "Error", "Passwords do not coincide! Please confirm again!"
            )
            return

        self.reg_names[username] = password
        self.save_registered_users()
        messagebox.showinfo("Success", "Registration successful!")
        self.signup.destroy()

    def goAhead(self, name, password):

        if len(name) == 0 or name not in self.reg_names.keys():
            messagebox.showerror("Error", "User does not exist, please sign up first!")
            return

        if password != self.reg_names[name]:
            messagebox.showerror("Error", "Incorrect password!")
            return

        msg = json.dumps({"action": "login", "name": name})
        self.send(msg)
        response = json.loads(self.recv())
        if response["status"] == "ok":
            self.login.destroy()
            self.sm.set_state(S_LOGGEDIN)
            self.sm.set_myname(name)
            self.layout(name)
            self.textCons.config(state=NORMAL)
            self.textCons.insert(END, menu + "\n\n")
            self.textCons.config(state=DISABLED)
            self.textCons.see(END)

        process = threading.Thread(target=self.proc)
        process.daemon = True
        process.start()

    # The main layout of the chat
    def layout(self, name):

        self.name = name
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550, bg="#17202A")
        self.labelHead = Label(
            self.Window,
            bg="#17202A",
            fg="#EAECEE",
            text=self.name,
            font="Helvetica 13 bold",
            pady=5,
        )

        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window, width=450, bg="#ABB2B9")

        self.line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.textCons = Text(
            self.Window,
            width=20,
            height=2,
            bg="#17202A",
            fg="#EAECEE",
            font="Helvetica 14",
            padx=5,
            pady=5,
        )

        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)

        self.labelBottom = Label(self.Window, bg="#ABB2B9", height=80)

        self.labelBottom.place(relwidth=1, rely=0.825)

        self.entryMsg = Entry(
            self.labelBottom, bg="#2C3E50", fg="#EAECEE", font="Helvetica 13"
        )

        # place the given widget into the gui window
        self.entryMsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)

        self.entryMsg.focus()

        # create a Send Button
        self.buttonMsg = Button(
            self.labelBottom,
            text="Send",
            font="Helvetica 10 bold",
            width=20,
            bg="#ABB2B9",
            command=lambda: self.sendButton(self.entryMsg.get()),
        )

        self.buttonMsg.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        # place the scroll bar into the gui window
        scrollbar.place(relheight=1, relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.my_msg = msg
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, f"You: {msg}\n\n")
        self.textCons.config(state=DISABLED)
        self.entryMsg.delete(0, END)

    def proc(self):
        MAX_LINES = 100  # Set the maximum number of lines appearing on GUI
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                self.system_msg = self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons.config(state=NORMAL)
                self.textCons.insert(END, self.system_msg + "\n\n")
                lines = self.textCons.get("1.0", "end").split("\n")
                if len(lines) > MAX_LINES:
                    self.textCons.delete("1.0", f"{len(lines)-MAX_LINES}.0")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)

    def run(self):
        self.login()


# create a GUI class object
if __name__ == "__main__":
    g = GUI()
