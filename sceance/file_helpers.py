# -*- coding: utf-8 -*-

'''
set of functions that handle your watchlist and theaters files.
'''

import os.path

DATA_PATH = "data/"
WATCHLIST_FILE = "watchlist.txt"
THEATERS_FILE = "theaters.txt"

# --------------------- #
# watchlist helpers     #
# --------------------- #
def get_watchlist():
    '''Reads the watchlist file and returns a set of movies with titles lowercased.'''
    watchlist = DATA_PATH+WATCHLIST_FILE
    assert os.path.exists(watchlist), f"{watchlist} file does not exist."
    with open(DATA_PATH+WATCHLIST_FILE) as f:
        return frozenset((x[:-1]).lower() for x in f.readlines())

def update_watchlist():
    pass

# --------------------- #
# theater helpers       #
# --------------------- #
def get_theaters():
    '''Reads the theaters file and returns a set of theaters.'''
    theaterlist= DATA_PATH+THEATERS_FILE
    assert os.path.exists(theaterlist), f"{theaterlist} file does not exist."
    with open(DATA_PATH+THEATERS_FILE) as f:
        return f.readlines()

def add_theater(theater_name):
    pass

def remove_theater(theater_name):
    pass
