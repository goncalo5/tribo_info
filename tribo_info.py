#!/usr/bin/python
import os
import sys
import time
import json
import urllib
import re
# all_info = {"tribes": {"tribe1": {members_list: {"player1": {"id": 12345, "points": 123, "info": "msg"},
#                                                  "player2": {"id": 12346, "info": "msg"}},
#                                   {"id": 1234, "OD": 12000}
#                        "tribe2": {}}}
world = 57
print_order = "player, points, info"


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
        self.all_info["tribes"][new_tribe_name] = {"members_list": {}}
        print self.all_info

    def add_new_player(self, new_player_name, tribe):
        self.all_info["tribes"][tribe]["members_list"][new_player_name] = {"info": "", "id": "", "points": ""}

    def change_tribe_name(self, tribe, new_tribe_name):
        self.all_info["tribes"][new_tribe_name] = self.all_info["tribes"][tribe]
        del self.all_info["tribes"][tribe]

    def update_tribe(self, tribe):
        print "update_tribe(%s)" % tribe
        url = 'http://pt.twstats.com/index.php?page=search&name=%s&type=tribe' % tribe
        sock = urllib.urlopen(url)
        r = sock.read()
        sock.close()
        # print r
        pat = re.compile('id=([0-9]+)\"')
        id_tribe = pat.findall(r)
        print 1, id_tribe
        id_tribe = id_tribe[0]
        id_tribe = int(id_tribe)
        # print li
        # id_tribe = int(li[0])
        print id_tribe
        self.all_info["tribes"][tribe]["id"] = id_tribe

        url = 'http://pt.twstats.com/pt%s/index.php?page=tribe&id=%s' % (world, id_tribe)
        sock = urllib.urlopen(url)
        r = sock.read()
        sock.close()
        # print r
        pat = re.compile('([0-9,]+) score')
        ODS = pat.findall(r)
        print ODS
        OD, OD_ofensivo, OD_defensivo = int(ODS[0].replace(",", "")), int(ODS[1].replace(",", "")), int(ODS[2].replace(",", ""))
        OD_apoios = OD - OD_ofensivo - OD_defensivo
        self.all_info["tribes"][tribe]["OD"] = OD
        self.all_info["tribes"][tribe]["OD_ofensivo"] = OD_ofensivo
        self.all_info["tribes"][tribe]["OD_defensivo"] = OD_defensivo
        self.all_info["tribes"][tribe]["OD_apoios"] = OD_apoios
        pat = re.compile('>Pontos:</th><td>([0-9,]+)')
        points = int(pat.findall(r)[0].replace(",", ""))
        print points
        self.all_info["tribes"][tribe]["points"] = points

        url = 'http://pt.twstats.com/pt%s/index.php?page=tribe&mode=members&id=%s' % (world, id_tribe)
        sock = urllib.urlopen(url)
        r = sock.read()
        sock.close()
        # print r
        pat = re.compile('playerlink.*>(.+)</a>')
        members_list = pat.findall(r)
        return members_list

    def update_player_score(self, player_name, tribe):
        print "update_player_score(%s)" % player_name
        url = 'http://pt.twstats.com/index.php?page=search&name={}&type=player'.format(player_name)
        sock = urllib.urlopen(url)
        sock_readed = sock.read()
        sock.close()
        pat = '<td><span class="world">PT%s</span></td>\n<td>(.*)</td>\n.*id=(.*)".*\n<td>(.*)</td>\n<td>(.*)</td>.*' % world
        position, player_id, points, n_villages = re.search(pat, sock_readed).groups()
        self.all_info["tribes"][tribe]["members_list"][player_name]["position"] = position
        self.all_info["tribes"][tribe]["members_list"][player_name]["id"] = player_id
        self.all_info["tribes"][tribe]["members_list"][player_name]["points"] = int(points.replace(",", ""))
        print "ok1"
        # self.all_info["tribes"][tribe][player_name]["n_villages"] = n_villages
        # pat = 'xx-small">\((.*) score.*xx-small">\((.*) score.*.*xx-small">\((.*) score.*.*xx-small">\((.*) score.*'
        url = 'http://pt.twstats.com/pt{}/index.php?page=player&id={}'.format(world, player_id)
        sock = urllib.urlopen(url)
        sock_readed = sock.read()
        sock.close()
        pat = 'xx-small">\((.*) score.*xx-small">\((.*) score.*.*xx-small">\((.*) score'
        OD = re.search(pat, sock_readed).groups()
        print OD
        OD, OD_ofensivo, OD_defensivo = OD
        OD, OD_ofensivo, OD_defensivo = int(OD.replace(",", "")), int(OD_ofensivo.replace(",", "")), int(OD_defensivo.replace(",", ""))
        OD_apoios = OD - OD_ofensivo - OD_defensivo
        self.all_info["tribes"][tribe]["members_list"][player_name]["OD"] = OD
        self.all_info["tribes"][tribe]["members_list"][player_name]["OD_ofensivo"] = OD_ofensivo
        self.all_info["tribes"][tribe]["members_list"][player_name]["OD_defensivo"] = OD_defensivo
        self.all_info["tribes"][tribe]["members_list"][player_name]["OD_apoios"] = OD_apoios
        print "ok2"
        self.save_file()

    def update_all_scores(self):
        for tribe in self.all_info["tribes"]:
            print tribe
            if tribe == "":
                continue
            members_list = self.update_tribe(tribe)
            # exit(0)
            for player in members_list:
                print player
                try:
                    if player not in self.all_info["tribes"][tribe]["members_list"]:
                        self.add_new_player(player, tribe)
                    self.update_player_score(player, tribe)
                except Exception as e:
                    print e
                    exit(0)
                    continue
        self.save_file()
        # raw_input()

    def delete_tribe(self, tribe):
        del self.all_info["tribes"][tribe]

    def delete_player(self, player):
        tribe = self.find_tribe(player)
        try:
            self.all_info["tribes"][tribe]["members_list"].pop(player)
        except:
            print "\nthat player don't exist"
            time.sleep(3)

    def check_if_the_tribe_exist(self, tribe):
        if tribe in self.all_info["tribes"]:
            return True
        return False

    def find_tribe(self, player):
        for tribe in self.all_info["tribes"]:
            if player in self.all_info["tribes"][tribe]["members_list"]:
                return tribe
        return False

    def print_head(self):
        player = "%-18s" % "player"
        points = "%7s" % "points"
        OD = "%7s" % "OD"
        ODO = "%7s" % "OD_ofensivo"
        ODD = "%7s" % "OD_defensivo"
        ODA = "%7s" % "OD_apoios"
        info = "%7s" % "info"
        exec "print \t%s" % print_order

    def print_player_infos(self, player_name, player_dict):
        player = player_name
        points = player_dict["points"]
        OD = player_dict["OD"]
        OD_ofensivo = player_dict["OD_ofensivo"]
        OD_defensivo = player_dict["OD_defensivo"]
        OD_apoios = player_dict["OD_apoios"]
        info = player_dict["info"]

        player = "%-18s" % player
        points = "%7s" % points
        OD = "%7s" % OD
        ODO = "%7s" % OD_ofensivo
        ODD = "%7s" % OD_defensivo
        ODA = "%7s" % OD_apoios
        info = "%7s" % info
        exec "print \t%s" % print_order

    def option_sa(self):  # see alphabetical ordered
        # print self.all_info
        for tribe in self.all_info["tribes"]:
            print "\n{}:".format(tribe)
            self.print_head()
            for player in sorted(self.all_info["tribes"][tribe]["members_list"], key=lambda s: s.lower()):
                self.print_player_infos(player, self.all_info["tribes"][tribe]["members_list"][player])
        raw_input()

    def option_sp(self):  # see ordered by points
        for tribe in self.all_info["tribes"]:
            print "\n%s:" % tribe
            # print "\t%-18s%7s%7s%7s%7s%7s %s" % ("player", "points", "OD", "ODO", "ODD", "ODA", "info")
            self.print_head()
            # print sorted(self.all_info["tribes"][tribe].items(),key=lambda x:x[1]['points'])
            for player in reversed(sorted(self.all_info["tribes"][tribe]["members_list"].items(),key=lambda x:int(x[1]['points']))):
                # print player[1]
                # print "\t%-18s%7s%7s%7s%7s%7s %s" % (player[0], player[1]["points"], player[1]["OD"], player[1]["OD_ofensivo"], player[1]["OD_defensivo"], player[1]["OD_apoios"], player[1]["info"])
                self.print_player_infos(player[0], player[1])
        raw_input()

    def option_sf(self):
        # print self.all_info
        for tribe in self.all_info["tribes"]:
            print "\n[ally]{}[/ally]:".format(tribe)
            print "[table]"
            print "[**]%-40s[||]%7s[||]%7s[||]%7s[||]%7s[||]%7s[||]%s[/**]" % ("player", "points", "OD", "ODO", "ODD", "ODA", "info")
            for player in sorted(self.all_info["tribes"][tribe]["members_list"], key=lambda s: s.lower()):
                info = self.all_info["tribes"][tribe]["members_list"][player]["info"]
                points = self.all_info["tribes"][tribe]["members_list"][player]["points"]
                OD = self.all_info["tribes"][tribe]["members_list"][player]["OD"]
                ODO = self.all_info["tribes"][tribe]["members_list"][player]["OD_ofensivo"]
                ODD = self.all_info["tribes"][tribe]["members_list"][player]["OD_defensivo"]
                ODA = self.all_info["tribes"][tribe]["members_list"][player]["OD_apoios"]
                print "[*]%-40s[|]%7s[|]%7s[|]%7s[|]%7s[|]%7s[|]%s" % (" - [player]" + player + "[/player]:", points, OD, ODO, ODD, ODA, info)
            print "[/table]"
        raw_input()

    def option_sd(self):  # see all_info dictionary
        print self.all_info
        raw_input()

    def option_sq(self):  # see quit
        self.print_menu()

    def option_s(self):
        self.print_menu(["alphabetical", "points", "forum", "dictionary", "quit"], "s")

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
                self.add_new_player(player, tribe)
        # print self.all_info["tribes"]
        # exit(0)
        player_info = raw_input("\n\ninfo?  ").decode(sys.stdin.encoding)
        self.all_info["tribes"][tribe]["members_list"][player]["info"] = player_info
        player_id = raw_input("\n\nid?  ").decode(sys.stdin.encoding)
        self.all_info["tribes"][tribe]["members_list"][player]["id"] = player_id
        self.all_info["tribes"][tribe]["members_list"][player]["points"] = self.update_player_score(player_id)



    def option_ai(self):
        player = raw_input("\n\nwhat is the name of that player?  ").decode(sys.stdin.encoding)
        tribe = self.find_tribe(player)
        if tribe == False:
            print "that player don't exist"
            return
        player_id = raw_input("\n\nwhat is the id of that player?  ").decode(sys.stdin.encoding)
        try:
            player_id = int(player_id)
        except ValueError:
            print "please insert a number"
            return
        self.all_info["tribes"][tribe]["members_list"][player]["id"] = player_id

    def option_aq(self):
        self.print_menu()

    def option_a(self):
        self.print_menu(["tribe", "player", "id of the player", "quit"], "a")

    def option_ut(self):  # updates the tribe name
        tribe = raw_input("\n\nwhich tribe?  ").decode(sys.stdin.encoding)
        new_tribe_name = raw_input("new tribe name?  ").decode(sys.stdin.encoding)
        self.change_tribe_name(tribe=tribe, new_tribe_name=new_tribe_name)

    def option_uc(self):  # change player tribe
        player = raw_input("\n\nwhich player?  ").decode(sys.stdin.encoding)
        current_tribe = self.find_tribe(player)
        if not current_tribe:
            print "\nthe player {} don't exist".format(player)
            time.sleep(3)
            return
        new_tribe = raw_input("\n\nwhich new tribe?  ").decode(sys.stdin.encoding)
        if not self.check_if_the_tribe_exist(new_tribe):
            print "\nthe tribe {} don't exist".format(new_tribe)
            time.sleep(3)
            return
        save_info_player = self.all_info["tribes"][current_tribe][player]
        print save_info_player
        self.delete_player(player)
        self.add_new_player(player, new_tribe)

    def option_ui(self):  # ui = update info
        player = raw_input("\n\nwhich player you wanna modify some info?  ").decode(sys.stdin.encoding)
        player_tribe = self.find_tribe(player)
        if player_tribe or player_tribe == "":
            print "current info of player {}: {}".format(
                player, self.all_info["tribes"][player_tribe][player])
            player_info = raw_input("\n\nwhich info you wanna modify?  ").decode(sys.stdin.encoding)
            self.all_info["tribes"][player_tribe][player]["info"] = player_info
            self.save_file()
        else:
            print "player {} don't exists".format(player)
            time.sleep(2)

    def option_us(self):  # update score (points)
        self.update_all_scores()

    def option_uq(self):  # quit update menu
        self.print_menu()

    def option_u(self):
        self.print_menu(["tribe", "player", "change tribe", "info", "score", "quit"], "u")

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

    def print_menu(self, options=["see", "add", "update", "delete", "quit"], first_option=""):
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
