# -*- coding: utf-8 -*-
'''
Starts a Firfox headless brower to see if movies on your watchlist are playing
at any of your favorite theaters.

Favorite theaters are taken from a txt file (extracted from "theaters.txt").
These showtimes are compared to a watchlist (extracted from "watchlist.txt")

-samuel mignot-
'''

# ------------------- #
# imports             #
# ------------------- #

import configparser
import os
from os import listdir
from os.path import isfile, join

# internal
import file_helpers

# ------------------- #
# constants           #
# ------------------- #

THIS_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = '/data'
WATCHLIST_DIR = '/watchlists'

ERROR_MESSAGE = {
    "watchlist_select": "response must be an integer in the range 1-{max_show}"
}

def robert_easter_eggers(res):
    print("really....the oscars watchlist...that's the kinda decision you make?")
    return res

def get_watchlists():
    mypath = THIS_DIRECTORY+DATA_DIR+WATCHLIST_DIR
    return [f for f in listdir(mypath) if isfile(join(mypath, f))]

def get_input(question, response_format, error_message):
    ''' loops until a response that is in response_format is met'''
    while True:
        res = input(question)
        if res in response_format:
            return res
        print(error_message)

def set_watchlist():
    '''for each movie left filtering, asks the user if they want to watch it and provides showtimes to pick from'''
    watchlist_files = get_watchlists()
    for i, watchlist in enumerate(watchlist_files, start=1):
        print(f"[{i}]: {watchlist}")
    res = get_input(
        f"select your watchlist [1-{len(watchlist_files)} or n to cancel]: ",
        set(map(str, range(1, len(watchlist_files)+1)))|{'n', 'no'},
        ERROR_MESSAGE['watchlist_select'].format(max_show=str(len(watchlist_files)))
    )
    print()
    if res == 'n':
        return None
    if res == 'oscar_watchlist.txt':
        res = robert_easter_eggers(res)
    return watchlist_files[int(res)-1]

if __name__ == "__main__":
    set_watchlist()
