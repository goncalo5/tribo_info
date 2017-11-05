#!/usr/bin/python
import os
import sys
import time
import json
import urllib
import re
# all_info = {"tribes": {"tribe1": {"player1": {"id": 12345, "points": 123, "info": "msg"},
#                                   "player2": {"id": 12346, "info": "msg"}},
#                        "tribe2": {}}}


class Run(object):
    def __init__(self):
        if __name__ == '__main__':
            self.file_name = "DB.json"
            self.try_open_file()
            self.open_file()
            self.run()

    # File
    def try_open_file(self):
        try:
            self.open_file()
        except IOError:
            self.create_a_new_file_from_scrath()

    def create_a_new_file_from_scrath(self):
        print "\ncreate a new file from scrath"
        self.all_info = {"tribes": {}}
        self.save_file()

    def open_file(self):
        self.f = open(self.file_name, "r")
        self.all_info = json.load(self.f)

    def save_file(self):
        self.f = open(self.file_name, "w")
        json.dump(self.all_info, self.f)

    def clear_screen(self):
        if os.name == "nt":
            os.system("cls")  # windows
        else:
            os.system("clear")

    def add_new_tribe(self, new_tribe_name):
        self.all_info["tribes"][new_tribe_name] = {}
        print self.all_info

    def add_new_player(self, new_player_name, tribe):
        self.all_info["tribes"][tribe][new_player_name] = {"info": ""}

    def modify_tribe(self, tribe, new_tribe_name):
        self.all_info["tribes"][new_tribe_name] = self.all_info["tribes"][tribo]
        del self.all_info["tribes"][tribo]

    def delete_tribe(self, tribe):
        del self.all_info["tribes"][tribe]

    def delete_player(self, player):
        tribe = self.find_tribe(player)
        try:
            self.all_info["tribes"][tribe].pop(player)
        except:
            print "\nthat player don't exist"
            time.sleep(3)

    def check_if_the_tribe_exist(self, tribe):
        print self.all_info
        if tribe in self.all_info["tribes"]:
            return True
        return False

    def find_tribe(self, player):
        for tribe in self.all_info["tribes"]:
            if player in self.all_info["tribes"][tribe]:
                return tribe
        return False

    def option_sa(self):
        # print self.all_info
        for tribe in self.all_info["tribes"]:
            print "\n{}:".format(tribe)
            for player in sorted(self.all_info["tribes"][tribe], key=lambda s: s.lower()):
                info = self.all_info["tribes"][tribe][player]
                print "\t{}:\t{}".format(player, info)
        raw_input()

    def option_sf(self):
        # print self.all_info
        for tribe in self.all_info["tribes"]:
            print "\n[ally]{}[/ally]:".format(tribe)
            for player in sorted(self.all_info["tribes"][tribe], key=lambda s: s.lower()):
                info = self.all_info["tribes"][tribe][player]
                print "[player]{}[/player]:\t{}".format(player, info)
        raw_input()

    def option_sq(self):  # see quit
        self.print_menu()

    def option_s(self):
        self.print_menu(["alphabetical", "points", "forum", "quit"], "s")

    def option_at(self):  # at = add tribe
        tribe = raw_input("\n\nwhich tribe you wanna add?  ").decode(sys.stdin.encoding)
        # check if that word doesn't already exist and give the points in case of existing
        tribe_exist = self.check_if_the_tribe_exist(tribe)
        if not tribe_exist:
            print "that tribe don't exist"
            self.add_new_tribe(tribe)
        else:
            print "\nthe tribe %s already exists" % (tribe)
            time.sleep(3)

    def option_ap(self):  # at = add player
        player = raw_input("\n\nwhich player you wanna add?  ").decode(sys.stdin.encoding)
        # check if that word doesn't already exist and give the points in case of existing
        player_tribe = self.find_tribe(player)
        if player_tribe:
            print "\nthe player {} already exists, in the tribe {}".format(player, player_tribe)
            time.sleep(3)
        else:
            tribe = raw_input("\n\nwhich tribe you wanna add that player?  ").decode(sys.stdin.encoding)
            tribe_exist = self.check_if_the_tribe_exist(tribe)
            if not tribe_exist:
                print "that tribe don't exist"
                answer = raw_input("want to add that tribe?  ")
                if answer.lower() in ["y", "yes"]:
                    self.add_new_tribe(tribe)
                    self.add_new_player(player, tribe)
            else:
                print self.all_info
                self.add_new_player(player, tribe)

    def option_aq(self):
        self.print_menu()

    def option_a(self):
        self.print_menu(["tribe", "player", "quit"], "a")

    def option_mt(self):  # modify tribe
        tribe = raw_input("\n\nwhich tribe?  ").decode(sys.stdin.encoding)
        new_tribe_name = raw_input("new tribe name?  ").decode(sys.stdin.encoding)
        self.modify_tribe(tribe=tribe, new_tribe_name=new_tribe_name)

    def option_mc(self):  # change player tribe
        player = raw_input("\n\nwhich player?  ").decode(sys.stdin.encoding)
        current_tribe = self.find_tribe(player)
        if not current_tribe:
            print "\nthe player {} don't exist".format(player)
            time.sleep(3)
            return
        try:
            new_tribe = raw_input("\n\nwhich new tribe?  ").decode(sys.stdin.encoding)
        except KeyError:
            print "\nthe tribe {} don't exist".format(new_tribe)
            time.sleep(3)
            return
        save_info_player = self.all_info["tribes"][current_tribe][player]
        print save_info_player
        self.delete_player(player)
        self.add_new_player(player, new_tribe)

    def option_mi(self):  # ai = modify info
        player = raw_input("\n\nwhich player you wanna modify some info?  ").decode(sys.stdin.encoding)
        player_tribe = self.find_tribe(player)
        if player_tribe or player_tribe == "":
            print "current info of player {}: {}".format(
                player, self.all_info["tribes"][player_tribe][player])
            player_info = raw_input("\n\nwhich info you wanna modify?  ").decode(sys.stdin.encoding)
            self.all_info["tribes"][player_tribe][player] = player_info
            self.save_file()
        else:
            print "player {} don't exists".format(player)
            time.sleep(2)

    def option_mq(self):
        self.print_menu()

    def option_m(self):
        self.print_menu(["tribe", "player", "change tribe", "info", "quit"], "m")

    def option_dt(self):  # dt = delete tribe
        tribe = raw_input("which tribe you wanna delete?  ")
        self.delete_tribe(tribe)

    def option_dp(self):  # dp = delete player
        player = raw_input("which player you wanna delete?  ")
        self.delete_player(player)

    def option_dq(self):  # dq = delete quit
        self.print_menu()

    def option_d(self):
        self.print_menu(["tribe", "player", "quit"], "d")

    def option_q(self):
        sys.exit(0)

    def print_menu(self, options=["see", "add", "modify", "delete", "quit"], first_option=""):
        while True:
            menu = "\n"
            for option in options:
                menu += "[{}]{} ".format(option[0], option[1::])
            print menu,
            choice = raw_input("  ").strip().lower()
            erro_msg = "\n\nI don't understand your answer, please select one of the below posiblilities"
            if len(choice) != 1 and choice not in options:
                print erro_msg
                continue
            try:
                getattr(self, "option_{}{}".format(first_option, choice[0]))()
            except AttributeError:
                print erro_msg
                continue
            break

    def run(self):
        while True:
            self.clear_screen()
            self.print_menu()

            self.save_file()
            self.f.close()
        # self.run()

if __name__ == '__main__':
    Run()

print_menu()
exit(0)
f = open(file_name, "w")
json.dump(d, f)

f = open(file_name, "r")
a = json.load(f)


print a
