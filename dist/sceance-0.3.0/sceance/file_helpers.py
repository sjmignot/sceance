# -*- coding: utf-8 -*-

'''
set of functions that handle your watchlist and theaters files.
'''

import os.path

DATA_PATH = "data/"
WATCHLIST_FILE = "watchlist.txt"
THEATERS_FILE = "theaters.txt"
MY_PATH = os.path.abspath(os.path.dirname(__file__))


# --------------------- #
# watchlist helpers     #
# --------------------- #
def get_watchlist() -> set:
    '''Reads the watchlist file and returns a set of movies with titles lowercased.'''
    watchlist = os.path.join(MY_PATH, f"{DATA_PATH}{WATCHLIST_FILE}")
    assert os.path.exists(watchlist), f"{watchlist} file does not exist."
    with open(watchlist) as f:
        return frozenset((x[:-1]).lower() for x in f.readlines())

# --------------------- #
# theater helpers       #
# --------------------- #
def get_theaters() -> list:
    '''Reads the theaters file and returns a set of theaters.'''
    theaterlist = os.path.join(MY_PATH, f"{DATA_PATH}{THEATERS_FILE}")
    assert os.path.exists(theaterlist), f"{theaterlist} file does not exist."
    with open(theaterlist) as f:
        return f.readlines()

def add_theater(theater_name):
    '''Adds a theater to your favorite theater file'''
    theaterlist = os.path.join(MY_PATH, f"{DATA_PATH}{THEATERS_FILE}")
    assert os.path.exists(theaterlist), f"{theaterlist} file does not exist."
    with open(theaterlist) as f:
        f.write(theater_name)

def remove_theater(theater_name):
    '''Remove theater from you list of favorite theaters'''
    pass
