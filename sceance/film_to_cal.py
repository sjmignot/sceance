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

def film_to_cal(args, headless: bool = True):
    '''main file for getting showings and savaing them to a google calendar'''
    showings = get_showings.get_watchlist_showings(args['browser'], args['all_films'], args['theaters'], args['watchlist'], headless)
    projection_list = filter_select_showings.filter_select_showings(showings, args['workdays'], args['workhours'])
    showtimes_to_google_cal.create_projection_events(projection_list, args['timezone'])

if __name__ == "__main__":
    film_to_cal(args)
