"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
# from chat_client_class import Client
from chat_utils import *
import json
from secured_messaging import RSA
from Five_in_a_row import OnlineFiveInARow


class ClientSM:
    __slots__ = 'state', 'peer', 'me', 'out_msg', 's', 'public_key', 'private_key', 'peer2key', 'hold'

    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s

        # for RSA encrypt
        self.public_key = ()
        self.private_key = ()

        self.peer2key = {}

        self.hold = None

    def generate_key_pairs(self):
        rsa_instance = RSA()
        self.public_key, self.private_key = rsa_instance.show_public_private_key_pair()
        print(self.public_key, self.private_key)
        msg = json.dumps({"action": "send_key", "from": self.me, "pub_key": self.public_key})
        # msg = json.dumps({"action": "send_key", "from": self.me, "pub_key": self.public_key.decode('utf-8')})
        mysend(self.s, msg)

    def get_peer_keys(self):
        msg = json.dumps({"action": "get_key", "from": self.me})
        mysend(self.s, msg)
        res = json.loads(myrecv(self.s))
        self.peer2key = res['results']

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action": "connect", "target": peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with ' + self.peer + '\n'
            return True
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return False

    def disconnect(self):
        msg = json.dumps({"action": "disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
        # ==============================================================================
        # Once logged in, do a few things: get peer listing, connect, search
        # And, of course, if you are so bored, just go
        # This is event handling instate "S_LOGGEDIN"
        # ==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next delay_accumulator!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'delay_accumulator':
                    mysend(self.s, json.dumps({"action": "delay_accumulator"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action": "list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer):
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action": "search", "target": term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action": "poem", "target": poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    # print(poem)
                    if len(poem) > 0:
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING

        # ==============================================================================
        # Start chatting, 'bye' for quit
        # This is event handling instate "S_CHATTING"
        # ==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:  # my stuff going out
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''

                elif my_msg == 'game':
                    # to notify the other side that you want to play a game
                    # print(666666666666666)
                    mysend(self.s,
                           json.dumps({"action": "exchange", "from": "[" + self.me + "]",
                                       "msg": 'I want to play a game with you'}))
                    self.hold = 'BLACK'
                    self.state = S_GAME

                else:
                    self.get_peer_keys()
                    print(
                        f'--------------< check if received {self.peer2key} >--------------')  # check if messages are sent
                    message_dict = {}
                    for i in self.peer2key.keys():
                        message_dict[i] = RSA.encrypt(self.peer2key[i], my_msg)
                    # print(message_dict)
                    mysend(self.s,
                           json.dumps({"action": "exchange", "from": "[" + self.me + "]", "msg": message_dict}))

            if len(peer_msg) > 0:  # peer's stuff, coming in
                print(peer_msg)
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"
                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN
                elif peer_msg["msg"] == 'I want to play a game with you':
                    # print(666)
                    mysend(self.s,
                           json.dumps({'action': 'chess_state_update', "from": "[" + self.me + "]", "to": self.peer,
                                       "msg": []}))
                    self.hold = 'WHITE'
                    self.state = S_GAME
                else:
                    self.out_msg += peer_msg["from"] + str(RSA.decrypt(self.private_key, peer_msg["msg"][self.me]))

            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu

        elif self.state == S_GAME:
            game = OnlineFiveInARow(self.s, self.me, self.peer, self.hold)

            game.main_game()
            self.state = S_CHATTING
            # if self.game_flag:
            #     game = FiveINARow()
            #     self.game_flag = False
            # else:
            #     game = None
            # game = FiveINARow()
            # while True:
            #     game.screen_initiator_exit()
            #     game.make_chess_board()
            #
            #     # temp_dict = {i: game.chess[i] for i in range(len(game.chess))}
            #
            #     mysend(self.s,
            #            json.dumps({'action': 'chess_state_update', "from": "[" + self.me + "]", "to": self.peer,
            #                        "msg": game.chess}))
            #
            #     peer_state = myrecv(self.s)
            #     if len(peer_state) > 0:
            #         peer_state = json.loads(peer_state)
            #         print(peer_state['msg'])
            #
            #         if peer_state['action'] == 'Surrender':
            #             # TODO: here to fill in the code for surrender
            #             return
            #         elif peer_state['action'] == 'Ask for tie':
            #             # TODO: here to fill in the code for tie up
            #             return
            #         elif peer_state['action'] == 'chess_state_update':
            #             print(type(peer_state['msg']))
            #             print(peer_state['msg'])
            #             if len(peer_state['msg']) > len(game.chess):
            #                 game.chess = peer_state['msg']
            #                 # game.update_bitboard(new_chess)
            #         else:
            #             pass
            #
            #     game.show_chess()
            #
            #     game.check_win()
            #
            #     x, y = game.report_cursor()
            #     game.chess_guider(x, y)
            #     game.put_down_chess(x, y)

        # ==============================================================================
        # invalid state
        # ==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
