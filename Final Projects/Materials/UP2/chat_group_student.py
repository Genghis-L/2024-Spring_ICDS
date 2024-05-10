S_ALONE = 0
S_TALKING = 1

# ==============================================================================
# Group class:
# member fields:
#   - An array of items, each a Member class
#   - A dictionary that keeps who is a chat group
# member functions:
#    - join: first time in
#    - leave: leave the system, and the group
#    - list_my_peers: who is in chatting with me?
#    - list_all: who is in the system, and the chat groups
#    - connect: connect to a peer in a chat group, and become part of the group
#    - disconnect: leave the chat group but stay in the system
# ==============================================================================

S_ALONE = 0
S_TALKING = 1

class Group:

    def __init__(self):
        self.members = {}
        self.chat_grps = {}
        self.grp_ever = 0

    def join(self, name):
        self.members[name] = S_ALONE
        return

    def is_member(self, name):

        # IMPLEMENTATION
        # ---- start your code ---- #
        return name in self.members.keys()
        # ---- end of your code --- #

    # implement
    def leave(self, name):
        """
        leave the system, and the group
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        self.disconnect(name)
        del self.members[name]
        # ---- end of your code --- #
        return

    def find_group(self, name):
        """
        Auxiliary function internal to the class; return two
        variables: whether "name" is in a group, and if true
        the key to its group
        """
        found = False
        group_key = 0
        # IMPLEMENTATION
        # ---- start your code ---- #
        for k in self.chat_grps.keys():
            if name in self.chat_grps[k]:
                found = True
                group_key = k
                break
        # ---- end of your code --- #
        return found, group_key

    def connect(self, me, peer):
        """
        me is alone, connecting peer.
        if peer is in a group, join it
        otherwise, create a new group with you and your peer
        """
        peer_in_group, group_key = self.find_group(peer)

        # IMPLEMENTATION
        # ---- start your code ---- #
        if peer_in_group:
            self.chat_grps[group_key].append(me)
            self.members[me] = S_TALKING
        else:
            self.grp_ever += 1
            self.chat_grps[self.grp_ever] = self.chat_grps.get(self.grp_ever, []) + [me] + [peer]

            self.members[me] = S_TALKING
            self.members[peer] = S_TALKING
        # ---- end of your code --- #
        return

    # implement
    def disconnect(self, me):
        """
        find myself in the group, quit, but stay in the system
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        grouping_state, group_key = self.find_group(me)
        if grouping_state:
            group_members = self.chat_grps[group_key]
            group_members.remove(me)
            self.members[me] = S_ALONE
            if len(group_members) == 1:
                peer = group_members.pop()
                self.members[peer] = S_ALONE
                del self.chat_grps[group_key]
        # ---- end of your code --- #
        return

    def list_all(self):
        # a simple minded implementation
        full_list = "Users: ------------" + "\n"
        full_list += str(self.members) + "\n"
        full_list += "Groups: -----------" + "\n"
        full_list += str(self.chat_grps) + "\n"
        return full_list

    # implement
    def list_me(self, me):
        """
        return a list, "me" followed by other peers in my group
        """
        my_list = []
        # IMPLEMENTATION
        # ---- start your code ---- #
        if me in self.members.keys():
            my_list.append(me)
            grouping_state, group_key = self.find_group(me)
            if grouping_state:
                for member in self.chat_grps[group_key]:
                    if member != me:
                        my_list.append(member)
        # ---- end of your code --- #
        return my_list


if __name__ == "__main__":
    g = Group()
    g.join('a')
    g.join('b')
    g.join('c')
    g.join('d')
    print(g.list_all())

    g.connect('a', 'b')
    print(g.list_all())
    g.connect('c', 'a')
    print(g.list_all())
    g.leave('c')
    print(g.list_all())
    g.disconnect('b')
    print(g.list_all())
