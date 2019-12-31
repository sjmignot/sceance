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

def main(headless=True, auto_filter_work=True):
    showings = get_showings.get_watchlist_showings()
    print(showings)
    projection_list = filter_select_showings.filter_select_showings(showings)
    print(projection_list)
    showtimes_to_google_cal.create_projection_events(projection_list)

if __name__ == "__main__":
    main()
