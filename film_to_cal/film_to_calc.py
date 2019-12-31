'''
Starts a Firfox headless brower to see if movies on your watchlist are playing
at any of your favorite theaters.

Favorite theaters are taken from a txt file (extracted from "theaters.txt").
These showtimes are compared to a watchlist (extracted from "watchlist.txt")

-samuel mignot-
'''

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

WATCHLIST_FILE = "watchlist.txt"
THEATERS_FILE = "theaters.txt"
GOOGLE_CSS_SELECTORS = {
    "see_more": "div.hide-focus-ring.iXqz2e.aI3msd.xpdarr.pSO8Ic.vk_arc",
    "address": "span.LrzXr",
    "show_days": "li.tb_l",
    "showings": "div.lr_c_fcb.lr-s-stor",
    "film_length": "div.wwUB2c.PZPZlf"
}

FILM_DETAIL_SEP = '‧'
DATA_PATH = 'data/'

Theater = collections.namedtuple('Theater', ['name', 'address'])
Film = collections.namedtuple('Film', ['name','release', 'genre', 'length'])

def get_dates(datelist):
    '''Takes a string of concatenated standard dates and return a list of military time tuples.'''
    date_pattern = r"\d{1,2}\:\d{2}(?:am|pm)"
    matches = re.findall(date_pattern, datelist)
    tupled_matches = [list(map(int, match[:-2].split(":")))+[match[-2:]] for match in matches]
    military_time_tuples = [tuple([match[0]+12, match[1]]) if match[2] == 'pm'
                            else tuple(match[:2]) for match in tupled_matches]
    return military_time_tuples

def get_watchlist():
    '''Reads the watchlist file and returns a set of movies with titles lowercased.'''
    with open(DATA_PATH+WATCHLIST_FILE) as f:
        return frozenset((x[:-1]).lower() for x in f.readlines())

def get_theaters():
    '''Reads the theaters file and returns a set of theaters.'''
    with open(DATA_PATH+THEATERS_FILE) as f:
        return f.readlines()

@contextmanager
def wait_for_new_window(driver, timeout=10):
    handles_before = driver.window_handles
    yield
    WebDriverWait(driver, timeout).until(
        lambda driver: len(handles_before) != len(driver.window_handles))


def get_movie_lengths(film_links):
    '''Takes a dictionary of film links and gets movie lengths if they haven't already been saved.'''
    film_length_dict = {}
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
            length = tuple(film_length[:-1].strip().split('h '))
        )
        print(cur_film)
        film_length_dict[k] = cur_film

    with open(f'{DATA_PATH}film_length.pickle', 'wb') as flf:
        pickle.dump(film_length_dict, flf)

    return film_length_dict

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

def main(headless=True, auto_filter_work=True):
    '''Do X and return a list.'''
    theater_search_placeholder = "https://www.google.com/search?q={theater_name}+showtimes"

    movie_showtimes = {}
    film_links = {}

    driver = start_brower(headless)

    watchlist = get_watchlist()
    theaters = get_theaters()

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
                    if name in movie_showtimes.keys():
                        movie_showtimes[name].append((movie_theater, possible_showtime))
                    else:
                        movie_showtimes[name] = [(movie_theater, possible_showtime)]
            date_s += datetime.timedelta(days=1)
    driver.quit()

    print(movie_showtimes)
    possible_showtimes = {}
    for key, value in movie_showtimes.items():
        print(key)
        if key.lower() in watchlist:
            print(f"You can watch {key} at:")
            for i in value:
                print(f"- {i[0].name} at {i[1]}")
    film_links = { k: v for k, v in film_links.items() if k.lower() in watchlist }
    film_length_dict = get_movie_lengths(film_links)
    print(film_length_dict)

if __name__ == "__main__":
    main()