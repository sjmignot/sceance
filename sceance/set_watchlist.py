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
OSCARS_WATCHLIST = 'oscar-winners-watchlist.txt'

ERROR_MESSAGE = {
    "watchlist_select": "response must be an integer in the range 1-{max_show}",
        "yes_no": "response must be one of the following: 'yes', 'y', 'no', 'n'"

}

def robert_easter_eggers(original_choice):
    res = get_input(
        f"Are you sure you want to set your default watchlist to...the oscars..?  [y/n]: ",
        {'y', 'yes', 'no', 'n'},
        ERROR_MESSAGE['yes_no']
    )
    if res in {'y', 'yes'}:
        res = get_input(
            f"The awards that gave Best Picture to Forrest Gump over Pulp fiction..? [y/n]: ",
            {'y', 'yes', 'no', 'n'},
            ERROR_MESSAGE['yes_no']
        )
        if res in {'y', 'yes'}:
            print('... Aight...')
            return original_choice
    if res in {'n', 'no'}:
        return set_watchlist(no_oscars=True)

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

def set_watchlist(no_oscars=False):
    '''for each movie left filtering, asks the user if they want to watch it and provides showtimes to pick from'''
    watchlist_files = get_watchlists()
    print(watchlist_files)
    if(no_oscars): watchlist_files = list(filter(lambda x: x!=OSCARS_WATCHLIST, watchlist_files))
    for i, watchlist in enumerate(watchlist_files, start=1):
        print(f"[{i}]: {watchlist}")
    res = get_input(
        f"select your watchlist [1-{len(watchlist_files)} or n to cancel]: ",
        set(map(str, range(1, len(watchlist_files)+1)))|{'n', 'no'},
        ERROR_MESSAGE['watchlist_select'].format(max_show=str(len(watchlist_files)))
    )
    print()
    if res in {'n', 'no'}:
        return None
    chosen_watchlist = watchlist_files[int(res)-1]
    if(not no_oscars):
        if chosen_watchlist == OSCARS_WATCHLIST:
            chosen_watchlist = robert_easter_eggers(chosen_watchlist)
    return chosen_watchlist

if __name__ == "__main__":
    set_watchlist()
