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

    # Read & Load Sign-up Memories
    def load_registered_users(self):
        try:
            with open("registered_users.json", "r") as file:
                self.reg_names = json.load(file)
        except FileNotFoundError:
            self.reg_names = {}

    def save_registered_users(self):
        with open("registered_users.json", "w") as file:
            json.dump(self.reg_names, file)

    # Log-in Section
    def login(self):
        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)

        self.pls1 = Label(
            self.login,
            text="Please login to continue.",
            justify=CENTER,
            font="Helvetica 14 bold",
        )
        self.pls1.place(relheight=0.15, relx=0.2, rely=0.07)

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

    # Sign-up Window Layout
    def signUpWindow(self):
        self.signup = Toplevel()
        self.signup.title("Sign Up")
        self.signup.resizable(width=False, height=False)
        self.signup.configure(width=400, height=300)

        self.pls2 = Label(
            self.signup,
            text="Please create a password that is six characters or longer.",
            justify=CENTER,
            font="Helvetica 10 bold",
        )
        self.pls2.place(relheight=0.15, relx=0.2, rely=0.07)

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

    # Sign-up Section
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

    # Go-ahead from Sign-up to Log-in
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

    # Chatroom Layout
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

        self.entryMsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)

        self.entryMsg.focus()

        self.buttonMsg = Button(
            self.labelBottom,
            text="Send",
            font="Helvetica 10 bold",
            width=20,
            bg="#ABB2B9",
            command=lambda: self.sendButton(self.entryMsg.get()),
        )

        self.buttonMsg.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.11)

        self.buttonG = Button(
            self.labelBottom,
            text="Game",
            font="Helvetica 10 bold",
            width=20,
            bg="#ABB2B9",
            command=self.start_game,
        )
        self.buttonG.place(relx=0.88, rely=0.008, relheight=0.06, relwidth=0.11)

        self.textCons.config(cursor="arrow")

        scrollbar = Scrollbar(self.textCons)

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

    # Game Section
    def start_game(self):
        self.my_msg = "request_to_start_a_game"

    def game_layout(self):
        self.gameWindow = Toplevel(self.Window)
        self.gameWindow.title("Tic-Tac-Toe")
        Label(self.gameWindow, text="Player 1 : X", font="times 18").grid(
            row=0, column=1
        )
        Label(self.gameWindow, text="Player 2 : O", font="times 18").grid(
            row=0, column=3
        )
        self.button1 = Button(
            self.gameWindow,
            width=15,
            height=7,
            font=("Times 16 bold"),
            command=self.checker1,
        )
        self.button1.grid(row=1, column=1)
        self.button2 = Button(
            self.gameWindow,
            width=15,
            height=7,
            font=("Times 16 bold"),
            command=self.checker2,
        )
        self.button2.grid(row=1, column=2)
        self.button3 = Button(
            self.gameWindow,
            width=15,
            height=7,
            font=("Times 16 bold"),
            command=self.checker3,
        )
        self.button3.grid(row=1, column=3)
        self.button4 = Button(
            self.gameWindow,
            width=15,
            height=7,
            font=("Times 16 bold"),
            command=self.checker4,
        )
        self.button4.grid(row=2, column=1)
        self.button5 = Button(
            self.gameWindow,
            width=15,
            height=7,
            font=("Times 16 bold"),
            command=self.checker5,
        )
        self.button5.grid(row=2, column=2)
        self.button6 = Button(
            self.gameWindow,
            width=15,
            height=7,
            font=("Times 16 bold"),
            command=self.checker6,
        )
        self.button6.grid(row=2, column=3)
        self.button7 = Button(
            self.gameWindow,
            width=15,
            height=7,
            font=("Times 16 bold"),
            command=self.checker7,
        )
        self.button7.grid(row=3, column=1)
        self.button8 = Button(
            self.gameWindow,
            width=15,
            height=7,
            font=("Times 16 bold"),
            command=self.checker8,
        )
        self.button8.grid(row=3, column=2)
        self.button9 = Button(
            self.gameWindow,
            width=15,
            height=7,
            font=("Times 16 bold"),
            command=self.checker9,
        )
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

    # Ask players whether to play again
    def play_again_dialog(self):
        choice = messagebox.askquestion("Play Again", "Do you want to play again?")
        if choice == "yes":
            self.gameWindow.destroy()
            self.start_game()
        else:
            self.gameWindow.destroy()

    # Chatroom Information Process Section
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
                    messagebox.showinfo(
                        title="Result", message="Player 1 wins the game!"
                    )
                    self.play_again_dialog()
                elif self.system_msg == "serverinfoPlayer 2":
                    messagebox.showinfo(
                        title="Result", message="Player 2 wins the game!"
                    )
                    self.play_again_dialog()
                elif self.system_msg == "serverinfodraw":
                    messagebox.showinfo(title="Result", message="This is a draw!")
                    self.play_again_dialog()

                else:
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
