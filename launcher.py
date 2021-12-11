#!/usr/bin/python

import getopt
import sys
import os
import json


def add_game():
    home = os.getenv("HOME")

    print("game name (no spaces): ")
    game_name = input()
    print("absolute path to the wine binary (filename too, spaces must be escaped): ")
    wine_bin = input()
    print("absolute path to the game binary (filename too, spaces must be escaped): ")
    game_bin = input()
    print("environment variables: ")
    env_vars = input()

    game = {
        "wine_bin": wine_bin,
        "game_bin": game_bin,
        "env_vars": env_vars
    }

    with open(f"{home}/.local/share/pyGameLauncher/{game_name}.json", "w+") as file:
        json.dump(game, file)


def print_games():
    home = os.getenv("HOME")

    for filename in os.listdir(f"{home}/.local/share/pyGameLauncher"):
        print(filename[:len(filename) - 5])


def launch_game(game_name):
    home = os.getenv("HOME")

    with open(f"{home}/.local/share/pyGameLauncher/{game_name}.json", "r") as file:
        json_object = json.load(file)

    env_vars = json_object["env_vars"]
    wine_bin = json_object["wine_bin"]
    game_bin = json_object["game_bin"]

    os.system(f"{env_vars} {wine_bin} {game_bin}")


def remove_game(game_name):
    home = os.getenv("HOME")

    os.remove(f"{home}/.local/share/pyGameLauncher/{game_name}.json")


def print_help():
    print("./launcher.py -h/--help\t\t\tShow this help info")
    print("./launcher.py -l <name>/--launch=<name>\tLaunch the game with the specified name")
    print("./launcher.py -p/--print\t\tPrint a list of games")
    print("./launcher.py -a/--add\t\t\tAdd a new game")
    print("./launcher.py -r <name>/--remove=<name>\tRemove the specified game")


def parse_cmd_args():
    opts, args = getopt.getopt(sys.argv[1:], "hl:apr:", ["help", "launch=", "add", "print", "remove="])

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


def setup_env():
    home = os.getenv("HOME")
    if not os.path.exists(f"{home}/.local/share/pyGameLauncher"):
        os.makedirs(f"{home}/.local/share/pyGameLauncher")


if __name__ == '__main__':
    setup_env()
    parse_cmd_args()
