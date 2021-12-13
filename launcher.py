#!/usr/bin/python

import getopt
import sys
import os
import json
import re

home = os.getenv("HOME")


def add_game():
    print("game name (no spaces): ")
    game_name = input()
    print("absolute path to the wine binary (filename too, spaces must be escaped): ")
    wine_bin = input()
    print("absolute path to the game binary (filename too, spaces must be escaped): ")
    game_bin = input()
    print("environment variables: ")
    env_vars = input()
    print("launch options to be passed to the game binary: ")
    game_opts = input()

    game = {
        "wine_bin": wine_bin,
        "game_bin": game_bin,
        "env_vars": env_vars,
        "game_opts": game_opts
    }

    with open(f"{home}/.local/share/pyGameLauncher/{game_name}.json", "w+") as file:
        json.dump(game, file)


def print_games():
    for filename in os.listdir(f"{home}/.local/share/pyGameLauncher"):
        print(filename[:len(filename) - 5])


def launch_game(game_name):
    with open(f"{home}/.local/share/pyGameLauncher/{game_name}.json", "r") as file:
        json_object = json.load(file)

    env_vars = json_object["env_vars"]
    wine_bin = json_object["wine_bin"]
    game_bin = json_object["game_bin"]
    game_opts = json_object["game_opts"]

    os.system(f"{env_vars} {wine_bin} {game_bin} {game_opts}")


def remove_game(game_name):
    os.remove(f"{home}/.local/share/pyGameLauncher/{game_name}.json")


def new_wine_pfx():
    print("absolute path to new prefix (spaces must be escaped): ")
    pfx_path = input()

    os.system(f"WINEPREFIX={pfx_path} winecfg")


def winetricks(game_name):
    with open(f"{home}/.local/share/pyGameLauncher/{game_name}.json", "r") as file:
        json_object = json.load(file)

    env_vars = json_object["env_vars"]

    prefix = re.search(r"(?<=WINEPREFIX=)[^ ]*", env_vars).group(0)

    os.system(f"WINEPREFIX={prefix} winetricks --gui")


def edit_game(game_name):
    editor = os.getenv("EDITOR")

    os.system(f"{editor} {home}/.local/share/pyGameLauncher/{game_name}.json")


def print_help():
    print("./launcher.py -h/--help\t\t\tShow this help info")
    print("./launcher.py -l <name>/--launch=<name>\tLaunch the game with the specified name")
    print("./launcher.py -p/--print\t\tPrint a list of games")
    print("./launcher.py -a/--add\t\t\tAdd a new game")
    print("./launcher.py -r <name>/--remove=<name>\tRemove the specified game")
    print("./launcher.py -n/--new\t\t\tCreate a new empty wine prefix")
    print("./launcher.py -t <name>/--tricks=<name>\tRun winetricks for the game with the specified name")
    print("./launcher.py -e <name>/--edit=<name>\tEdit the config for the game with the specified name")


def parse_cmd_args():
    opts, args = getopt.getopt(sys.argv[1:], "hl:apr:nt:e:", ["help", "launch=", "add", "print",
                                                              "remove=", "new", "tricks=", "edit="])

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
            exit(0)
        elif opt in ("-l", "--launch"):
            launch_game(arg)
            exit(0)
        elif opt in ("-p", "--print"):
            print_games()
            exit(0)
        elif opt in ("-a", "--add"):
            add_game()
            exit(0)
        elif opt in ("-r", "--remove"):
            remove_game(arg)
            exit(0)
        elif opt in ("-n", "--new"):
            new_wine_pfx()
            exit(0)
        elif opt in ("-t", "--tricks"):
            winetricks(arg)
            exit(0)
        elif opt in ("-e", "--edit"):
            edit_game(arg)
            exit(0)


def setup_env():
    if not os.path.exists(f"{home}/.local/share/pyGameLauncher"):
        os.makedirs(f"{home}/.local/share/pyGameLauncher")


if __name__ == '__main__':
    setup_env()
    parse_cmd_args()
