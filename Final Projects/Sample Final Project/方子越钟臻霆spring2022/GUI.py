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
from chat_utils import *
import json

# GUI class for the chat

all_emoji_list=["\U0001F600","\U0001F493","\U0001F400","\U0001F60D","\U0001F61C","\U0001F92D","\U0001F609","\U0001F607",
                "\U0001F911","\U0001F910","\U0001F4A9","\U0001F644","\U0001F60C","\U0001F44D","\U0001F4AA","\U0001F635",
                "\U0001F64F","\U0001F91E","\U0001F615","\U0001F4A3","\U0001F915","\U0001F62C","\U0001F44A","\U0001F637",
                "\U0001F61B","\U0001F60B","\U0001F92D","\U0001F44F","\U0001F924","\U0001F912"]

dic={}
for i in range(1,31):
    dic["button{}".format(i)] = all_emoji_list[i-1]




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
        # create a Label
        self.pls = Label(self.login,
                         text="Please login to continue",
                         justify=CENTER,
                         font="Helvetica 14 bold")

        self.pls.place(relheight=0.15,
                       relx=0.2,
                       rely=0.07)
        # create a Label
        self.labelName = Label(self.login,
                               text="Name: ",
                               font="Helvetica 12")

        self.labelName.place(relheight=0.2,
                             relx=0.1,
                             rely=0.2)

        # create a entry box for
        # tyoing the message
        self.entryName = Entry(self.login,
                               font="Helvetica 14")

        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)

        # set the focus of the curser
        self.entryName.focus()

        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                         text="CONTINUE",
                         font="Helvetica 14 bold",
                         command=lambda: self.goAhead(self.entryName.get()))

        self.go.place(relx=0.4,
                      rely=0.55)
        self.Window.mainloop()

    def goAhead(self, name):
        if len(name) > 0:
            msg = json.dumps({"action": "login", "name": name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
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
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=705,
                              height=550,
                              bg="#17202A")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)

        self.labelHead.place(relwidth=2/3)
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9")

        self.line.place(relwidth=2/3,
                        rely=0.07,
                        relheight=0.012)

        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.745,
                            relwidth=2/3,
                            rely=0.08)

        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)

        self.labelBottom.place(relwidth=2/3,
                               rely=0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")

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
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.77,
                             rely=0.01,
                             relheight=0.06,
                             relwidth=0.22)


        def button1():
            self.entryMsg.insert("end", dic['button1'])
            return
        def button2():
            self.entryMsg.insert("end", dic['button2'])
            return
        def button3():
            self.entryMsg.insert("end", dic['button3'])
            return
        def button4():
            self.entryMsg.insert("end", dic['button4'])
            return
        def button5():
            self.entryMsg.insert("end", dic['button5'])
            return
        def button6():
            self.entryMsg.insert("end", dic['button6'])
            return
        def button7():
            self.entryMsg.insert("end", dic['button7'])
            return
        def button8():
            self.entryMsg.insert("end", dic['button8'])
            return
        def button9():
            self.entryMsg.insert("end", dic['button9'])
            return
        def button10():
            self.entryMsg.insert("end", dic['button10'])
            return
        def button11():
            self.entryMsg.insert("end", dic['button11'])
            return
        def button12():
            self.entryMsg.insert("end", dic['button12'])
            return
        def button13():
            self.entryMsg.insert("end", dic['button13'])
            return
        def button14():
            self.entryMsg.insert("end", dic['button14'])
            return
        def button15():
            self.entryMsg.insert("end", dic['button15'])
            return
        def button16():
            self.entryMsg.insert("end", dic['button16'])
            return
        def button17():
            self.entryMsg.insert("end", dic['button17'])
            return
        def button18():
            self.entryMsg.insert("end", dic['button18'])
            return
        def button19():
            self.entryMsg.insert("end", dic['button19'])
            return
        def button20():
            self.entryMsg.insert("end", dic['button20'])
            return
        def button21():
            self.entryMsg.insert("end", dic['button21'])
            return
        def button22():
            self.entryMsg.insert("end", dic['button22'])
            return
        def button23():
            self.entryMsg.insert("end", dic['button23'])
            return
        def button24():
            self.entryMsg.insert("end", dic['button24'])
            return
        def button25():
            self.entryMsg.insert("end", dic['button25'])
            return
        def button26():
            self.entryMsg.insert("end", dic['button26'])
            return
        def button27():
            self.entryMsg.insert("end", dic['button27'])
            return
        def button28():
            self.entryMsg.insert("end", dic['button28'])
            return
        def button29():
            self.entryMsg.insert("end", dic['button29'])
            return
        def button30():
            self.entryMsg.insert("end", dic['button30'])
            return

        self.emoji_button1 = Button(self.Window, text=dic['button1'], fg="#FFFF00", bg="#CC6600", command=button1)
        self.emoji_button2 = Button(self.Window, text=dic['button2'], fg="#FFFF00", bg="#CC6600", command=button2)
        self.emoji_button3 = Button(self.Window, text=dic['button3'], fg="#FFFF00", bg="#CC6600", command=button3)
        self.emoji_button4 = Button(self.Window, text=dic['button4'], fg="#FFFF00", bg="#CC6600", command=button4)
        self.emoji_button5 = Button(self.Window, text=dic['button5'], fg="#FFFF00", bg="#CC6600", command=button5)
        self.emoji_button6 = Button(self.Window, text=dic['button6'], fg="#FFFF00", bg="#CC6600", command=button6)
        self.emoji_button7 = Button(self.Window, text=dic['button7'], fg="#FFFF00", bg="#CC6600", command=button7)
        self.emoji_button8 = Button(self.Window, text=dic['button8'], fg="#FFFF00", bg="#CC6600", command=button8)
        self.emoji_button9 = Button(self.Window, text=dic['button9'], fg="#FFFF00", bg="#CC6600", command=button9)
        self.emoji_button10 = Button(self.Window, text=dic['button10'], fg="#FFFF00", bg="#CC6600", command=button10)
        self.emoji_button11 = Button(self.Window, text=dic['button11'], fg="#FFFF00", bg="#CC6600", command=button11)
        self.emoji_button12 = Button(self.Window, text=dic['button12'], fg="#FFFF00", bg="#CC6600", command=button12)
        self.emoji_button13 = Button(self.Window, text=dic['button13'], fg="#FFFF00", bg="#CC6600", command=button13)
        self.emoji_button14 = Button(self.Window, text=dic['button14'], fg="#FFFF00", bg="#CC6600", command=button14)
        self.emoji_button15 = Button(self.Window, text=dic['button15'], fg="#FFFF00", bg="#CC6600", command=button15)
        self.emoji_button16 = Button(self.Window, text=dic['button16'], fg="#FFFF00", bg="#CC6600", command=button16)
        self.emoji_button17 = Button(self.Window, text=dic['button17'], fg="#FFFF00", bg="#CC6600", command=button17)
        self.emoji_button18 = Button(self.Window, text=dic['button18'], fg="#FFFF00", bg="#CC6600", command=button18)
        self.emoji_button19 = Button(self.Window, text=dic['button19'], fg="#FFFF00", bg="#CC6600", command=button19)
        self.emoji_button20 = Button(self.Window, text=dic['button20'], fg="#FFFF00", bg="#CC6600", command=button20)
        self.emoji_button21 = Button(self.Window, text=dic['button21'], fg="#FFFF00", bg="#CC6600", command=button21)
        self.emoji_button22 = Button(self.Window, text=dic['button22'], fg="#FFFF00", bg="#CC6600", command=button22)
        self.emoji_button23 = Button(self.Window, text=dic['button23'], fg="#FFFF00", bg="#CC6600", command=button23)
        self.emoji_button24 = Button(self.Window, text=dic['button24'], fg="#FFFF00", bg="#CC6600", command=button24)
        self.emoji_button25 = Button(self.Window, text=dic['button25'], fg="#FFFF00", bg="#CC6600", command=button25)
        self.emoji_button26 = Button(self.Window, text=dic['button26'], fg="#FFFF00", bg="#CC6600", command=button26)
        self.emoji_button27 = Button(self.Window, text=dic['button27'], fg="#FFFF00", bg="#CC6600", command=button27)
        self.emoji_button28 = Button(self.Window, text=dic['button28'], fg="#FFFF00", bg="#CC6600", command=button28)
        self.emoji_button29 = Button(self.Window, text=dic['button29'], fg="#FFFF00", bg="#CC6600", command=button29)
        self.emoji_button30 = Button(self.Window, text=dic['button30'], fg="#FFFF00", bg="#CC6600", command=button30)




        self.emoji_button1.place(relx=0.7,rely=0.07,relheight=0.09,relwidth=0.1)
        self.emoji_button2.place(relx=0.8, rely=0.07, relheight=0.09, relwidth=0.1)
        self.emoji_button3.place(relx=0.9, rely=0.07, relheight=0.09, relwidth=0.1)
        self.emoji_button4.place(relx=0.7,rely=0.16,relheight=0.09,relwidth=0.1)
        self.emoji_button5.place(relx=0.8,rely=0.16,relheight=0.09,relwidth=0.1)
        self.emoji_button6.place(relx=0.9,rely=0.16,relheight=0.09,relwidth=0.1)
        self.emoji_button7.place(relx=0.7,rely=0.25,relheight=0.09,relwidth=0.1)
        self.emoji_button8.place(relx=0.8,rely=0.25,relheight=0.09,relwidth=0.1)
        self.emoji_button9.place(relx=0.9,rely=0.25,relheight=0.09,relwidth=0.1)
        self.emoji_button10.place(relx=0.7,rely=0.34,relheight=0.09,relwidth=0.1)
        self.emoji_button11.place(relx=0.8,rely=0.34,relheight=0.09,relwidth=0.1)
        self.emoji_button12.place(relx=0.9,rely=0.34,relheight=0.09,relwidth=0.1)
        self.emoji_button13.place(relx=0.7,rely=0.43,relheight=0.09,relwidth=0.1)
        self.emoji_button14.place(relx=0.8,rely=0.43,relheight=0.09,relwidth=0.1)
        self.emoji_button15.place(relx=0.9,rely=0.43,relheight=0.09,relwidth=0.1)
        self.emoji_button16.place(relx=0.7,rely=0.52,relheight=0.09,relwidth=0.1)
        self.emoji_button17.place(relx=0.8,rely=0.52,relheight=0.09,relwidth=0.1)
        self.emoji_button18.place(relx=0.9,rely=0.52,relheight=0.09,relwidth=0.1)
        self.emoji_button19.place(relx=0.7,rely=0.61,relheight=0.09,relwidth=0.1)
        self.emoji_button20.place(relx=0.8,rely=0.61,relheight=0.09,relwidth=0.1)
        self.emoji_button21.place(relx=0.9, rely=0.61, relheight=0.09, relwidth=0.1)
        self.emoji_button22.place(relx=0.7, rely=0.7, relheight=0.09, relwidth=0.1)
        self.emoji_button23.place(relx=0.8, rely=0.7, relheight=0.09, relwidth=0.1)
        self.emoji_button24.place(relx=0.9, rely=0.7, relheight=0.09, relwidth=0.1)
        self.emoji_button25.place(relx=0.7, rely=0.79, relheight=0.09, relwidth=0.1)
        self.emoji_button26.place(relx=0.8, rely=0.79, relheight=0.09, relwidth=0.1)
        self.emoji_button27.place(relx=0.9, rely=0.79, relheight=0.09, relwidth=0.1)
        self.emoji_button28.place(relx=0.7, rely=0.88, relheight=0.09, relwidth=0.1)
        self.emoji_button29.place(relx=0.8, rely=0.88, relheight=0.09, relwidth=0.1)
        self.emoji_button30.place(relx=0.9, rely=0.88, relheight=0.09, relwidth=0.1)



        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.Window)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=2/3)

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
