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
import file_helpers

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

GOOGLE_CSS_SELECTORS = {
    "see_more": "div.hide-focus-ring.iXqz2e.aI3msd.xpdarr.pSO8Ic.vk_arc",
    "address": "span.LrzXr",
    "show_days": "li.tb_l",
    "showings": "div.lr_c_fcb.lr-s-stor",
    "film_length": "div.wwUB2c.PZPZlf"
}

FILM_DETAIL_SEP = '‧'
DATA_PATH = 'data/'

# ------------------- #
# named_tuples        #
# ------------------- #

Theater = collections.namedtuple('Theater', ['name', 'address'])
Film = collections.namedtuple('Film', ['name','release', 'genre', 'length'])

# ----------------------- #
# selenium driver helpers #
# ----------------------- #

def start_brower(headless):
    '''starts and returns a selenium firefox brower. Takes a paremeter to determine headedness'''
    options = Options()
    options.headless = headless

    profile = webdriver.FirefoxProfile()
    profile.set_preference('intl.accept_languages', 'en_GB')

    driver = webdriver.Firefox(
        executable_path=GeckoDriverManager().install(),
        firefox_profile=profile,
        options=options,
        service_log_path=os.path.devnull
    )
    return driver


@contextmanager
def wait_for_new_window(driver, timeout=10):
    '''makes sure a new window has loaded before progressing'''
    handles_before = driver.window_handles
    yield
    WebDriverWait(driver, timeout).until(
        lambda driver: len(handles_before) != len(driver.window_handles))

# ----------------------- #
# extraction helpers      #
# ----------------------- #

def get_movie_lengths(film_links):
    '''Takes a dictionary of film links and gets movie lengths if they haven't already been saved.'''
    film_length_dict = {}

    driver = start_brower(True)

    if os.path.exists(f'{DATA_PATH}film_length.pickle'):
        with open(f'{DATA_PATH}film_length.pickle', 'rb') as flf:
            film_length_dict = pickle.load(flf)

    new_films = { k: v for k, v in film_links.items() if k not in film_length_dict.keys()}
    if(not new_films): return film_length_dict

    for k, url in new_films.items():
        driver.get(url)
        film_details = driver.find_element_by_css_selector(GOOGLE_CSS_SELECTORS['film_length']).text
        release_date, film_genre, film_length = film_details.split(FILM_DETAIL_SEP)
        cur_film  = Film(
            name = k.strip(),
            release = release_date.strip(),
            genre = film_genre.strip(),
            length = tuple(map(int, film_length[:-1].strip().split('h ')))
        )
        print(cur_film)
        film_length_dict[k] = cur_film

    with open(f'{DATA_PATH}film_length.pickle', 'wb') as flf:
        pickle.dump(film_length_dict, flf)

    return film_length_dict

def get_dates(datelist):
    '''Takes a string of concatenated standard dates and return a list of military time tuples.'''
    date_pattern = r"\d{1,2}\:\d{2}(?:am|pm)"
    matches = re.findall(date_pattern, datelist)
    tupled_matches = [list(map(int, match[:-2].split(":")))+[match[-2:]] for match in matches]
    military_time_tuples = [tuple([match[0]+12, match[1]]) if match[2] == 'pm'
                            else tuple(match[:2]) for match in tupled_matches]
    return military_time_tuples

def get_possible_showtimes(movie_showtimes, film_length_dict, watchlist):
    '''returns a Film object to datetime array dict with playtimes for all movies found in watchlist'''
    possible_showtimes = {}
    for movie_name, showtimes in movie_showtimes.items():
        if movie_name.lower() in watchlist:
            for showtime in showtimes:
                possible_showtimes.setdefault(film_length_dict[movie_name], []).append(showtime)
    return possible_showtimes

# ---------------------- #
# main function          #
# ---------------------- #

def get_watchlist_showings(headless=True, auto_filter_work=True):
    '''Do X and return a list.'''
    theater_search_placeholder = "https://www.google.com/search?q={theater_name}+showtimes"

    movie_showtimes = {}
    film_links = {}

    driver = start_brower(headless)

    watchlist = file_helpers.get_watchlist()
    theaters = file_helpers.get_theaters()

    for theater in theaters:
        url = theater_search_placeholder.format(theater_name=(theater[:-1].replace(" ", "+")))
        driver.get(url)
        address = driver.find_element_by_css_selector(GOOGLE_CSS_SELECTORS['address']).text
        movie_theater = Theater(name=theater[:-1], address=address)
        print(f"{movie_theater}\n")
        show_days = driver.find_elements_by_css_selector(GOOGLE_CSS_SELECTORS['show_days'])
        date_s = datetime.datetime.today()
        for i, day in enumerate(show_days):
            day.click()
            try:
                see_more_button = driver.find_element_by_css_selector(
                    GOOGLE_CSS_SELECTORS['see_more']
                )
                driver.execute_script("arguments[0].click();", see_more_button)
            except selenium.common.exceptions.NoSuchElementException:
                pass
            showings = driver.find_elements_by_css_selector(GOOGLE_CSS_SELECTORS['showings'])
            for showing in showings:
                if not len(showing.text.splitlines()) == 3:
                    continue

                name, datelist = showing.text.splitlines()[1:]
                a = showing.find_element_by_css_selector('a')
                film_links[name] = a.get_attribute('href')

                show_times = get_dates(datelist)
                for show_time in show_times:
                    possible_showtime = date_s.replace(hour=show_time[0], minute=show_time[1])
                    movie_showtimes.setdefault(name,[]).append((movie_theater, possible_showtime))
            date_s += datetime.timedelta(days=1)
    driver.quit()

    film_links = { k: v for k, v in film_links.items() if k.lower() in watchlist }
    film_length_dict = get_movie_lengths(film_links)

    possible_showtimes = get_possible_showtimes(movie_showtimes, film_length_dict, watchlist)
    return possible_showtimes

if __name__ == "__main__":
    get_watchlist_showings()
