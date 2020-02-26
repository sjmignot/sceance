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

# internal
import get_showings
from get_showings import Film, Theater
import showtimes_to_google_cal
import filter_select_showings

# ------------------- #
# constants           #
# ------------------- #

COLOR = {
    'purple': '\033[95m',
    'cyan': '\033[96m',
    'darkcyan': '\033[36m',
    'blue': '\033[94m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'bold': '\033[1m',
    'underline': '\033[4m',
    'end': '\033[0m',
}

def bold(word):
    return COLOR['bold']+word+COLOR['end']

def underline(word):
    return COLOR['underline']+word+COLOR['end']

def film_to_cal(args, headless: bool = True):
    '''main file for getting showings and savaing them to a google calendar'''
    print("")
    print(f"running sceance with:")
    print(f"{bold('watchlist')}: {args['watchlist']}")
    print(f"{bold('theaters')}: {args['theaters']}")

    showings = get_showings.get_watchlist_showings(args['browser'], args['all_films'], args['theaters'], args['watchlist'], headless)
    projection_list = filter_select_showings.filter_select_showings(showings, args['workdays'], args['workhours'])
    if(len(projection_list)>0):
        showtimes_to_google_cal.create_projection_events(projection_list, args['timezone'])
    print("No showtimes selected")
if __name__ == "__main__":
    film_to_cal(args)
