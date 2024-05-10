# import all the required  modules
import threading
import select
import tkinter as tk
from chat_utils import *
import json


class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""

    def login(self):

        # create a window object
        root = tk.Tk()

        # set the window size and background color
        root.geometry("400x400")
        root.configure(bg="#F0F0F0")

        # set the title of the window
        root.title("Chatting App Login")

        # create a label for the title of the interface
        title_label = tk.Label(root, text="Chatting App", font=("Helvetica", 24, "bold"), fg="#333333", bg="#F0F0F0")
        title_label.pack(pady=20)

        # create a label for the username
        username_label = tk.Label(root, text="Username", font=("Helvetica", 14), fg="#333333", bg="#F0F0F0")
        username_label.pack(pady=10)

        # create an entry for the username
        username_entry = tk.Entry(root, font=("Helvetica", 14), fg="#333333", bg="#FFFFFF", bd=0, highlightthickness=1,
                                  highlightcolor="#333333", highlightbackground="#333333")
        username_entry.pack(pady=10)

        # create a label for the password
        password_label = tk.Label(root, text="Password", font=("Helvetica", 14), fg="#333333", bg="#F0F0F0")
        password_label.pack(pady=10)

        # create an entry for the password
        password_entry = tk.Entry(root, font=("Helvetica", 14), fg="#333333", bg="#FFFFFF", bd=0, highlightthickness=1,
                                  highlightcolor="#333333", highlightbackground="#333333", show="*")
        password_entry.pack(pady=10)

        # create a button to login
        login_button = tk.Button(root, text="Login", font=("Helvetica", 14, "bold"), fg="#FFFFFF", bg="#007AFF", bd=0,
                                 highlightthickness=0, pady=10, padx=50, command=lambda: self.goAhead(username_entry.get()))
        login_button.pack(pady=20)

        # run the window
        root.mainloop()

    def goAhead(self, name):
        if len(name) > 0:
            msg = json.dumps({"action": "login", "name": name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                # self.login.tk.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                # self.layout(name)
                # self.kaylee.config(state=NORMAL)
                # self.kaylee.insert(END, "hello" +"\n\n")
                # self.kaylee.insert(END, menu + "\n\n")
                # self.kaylee.config(state=DISABLED)
                # self.kaylee.see(END)
                # while True:
                #     self.proc()
        # the thread to receive messages
        #     process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()


a =GUI(1, 2, 3, 4)
a.login()