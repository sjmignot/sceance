# -*- coding: utf-8 -*-

DATA_PATH = "data/"
WATCHLIST_FILE = "watchlist.txt"
THEATERS_FILE = "theaters.txt"

# --------------------- #
# watchlist helpers     #
# --------------------- #
def get_watchlist():
    '''Reads the watchlist file and returns a set of movies with titles lowercased.'''
    with open(DATA_PATH+WATCHLIST_FILE) as f:
        return frozenset((x[:-1]).lower() for x in f.readlines())

def update_watchlist():
    pass

# --------------------- #
# theater helpers       #
# --------------------- #
def get_theaters():
    '''Reads the theaters file and returns a set of theaters.'''
    with open(DATA_PATH+THEATERS_FILE) as f:
        return f.readlines()

def add_theater(theater_name):
    pass

def remove_theater(theater_name):
    pass
