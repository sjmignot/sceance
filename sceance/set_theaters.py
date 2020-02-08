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
THEATERS_DIR = '/theaters'

ERROR_MESSAGE = {
    "theaters_select": "response must be an integer in the range 1-{max_show}",
    "yes_no": "response must be one of the following: 'yes', 'y', 'no', 'n'"
}

def get_theaters():
    mypath = THIS_DIRECTORY+DATA_DIR+THEATERS_DIR
    return [f for f in listdir(mypath) if isfile(join(mypath, f))]

def get_input(question, response_format, error_message):
    ''' loops until a response that is in response_format is met'''
    while True:
        res = input(question)
        if res in response_format:
            return res
        print(error_message)

def set_theaters():
    '''for each movie left filtering, asks the user if they want to watch it and provides showtimes to pick from'''
    theaters_files = get_theaters()
    for i, theater in enumerate(theaters_files, start=1):
        print(f"[{i}]: {theater}")
    res = get_input(
        f"select your theaters file [1-{len(theaters_files)} or n to cancel]: ",
        set(map(str, range(1, len(theaters_files)+1)))|{'n', 'no'},
        ERROR_MESSAGE['theaters_select'].format(max_show=str(len(theaters_files)))
    )
    print()
    if res == 'n':
        return None
    chosen_theaters_file = theaters_files[int(res)-1]
    return chosen_theaters_file

if __name__ == "__main__":
    set_theaters()
