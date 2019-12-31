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

# external
import os
import datetime
import re
import collections
import time
import pickle
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from contextlib import contextmanager

# ------------------- #
# constants           #
# ------------------- #

def main(headless=True, auto_filter_work=True):
    showings = get_showings.main()
    print(showings)

if __name__ == "__main__":
    main()
