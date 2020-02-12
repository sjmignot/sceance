# -*- coding: utf-8 -*-
'''
Starts a Firfox headless browser to see if movies on your watchlist are playing
at any of your favorite theaters.

Favorite theaters are taken from a txt file (extracted from "theaters.txt").
These showtimes are compared to a watchlist (extracted from "watchlist.txt")

-samuel mignot-
'''

# ------------------- #
# imports             #
# ------------------- #

# external
import os
import datetime
import re
import collections
import pickle

from typing import List, Dict, Tuple
from typing import NewType

from distutils.util import strtobool
from contextlib import contextmanager

import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

from progress.bar import FillingSquaresBar

# internal
import file_helpers

# ------------------- #
# constants           #
# ------------------- #

GOOGLE_CSS_SELECTORS = {
    "see_more": "div[class^='hide-focus-ring']",
    "address": "span.LrzXr",
    "show_days": "li.tb_l",
    "showings": "div.lr_c_fcb.lr-s-stor",
    "film_details": "div.wwUB2c.PZPZlf",
    "film_description": "div.SALvLe.farUxc.mJ2Mod",
    "english_lang": "div.std.stp.card-section",
}

FILM_DETAIL_SEP = '‧'
DATA_PATH = 'data/'
MY_PATH = os.path.abspath(os.path.dirname(__file__))
FILM_DETAIL_PATTERNS = {
    "description": r"Description\n(.*)\n",
    "director": r"Director: (.*)\n"
}

DEBUG = False


# ------------------- #
# named_tuples        #
# ------------------- #

Theater = collections.namedtuple('Theater', ['name', 'address'])
Film = collections.namedtuple('Film', ['name', 'release', 'genre', 'length', 'director', 'description'])
Showtime = NewType('Showtime', datetime.datetime)

# ----------------------- #
# selenium driver helpers #
# ----------------------- #

def get_element(driver, element_selector: str, element_name: str) -> WebElement:
    '''gets an element from the current page with the selector, or returns a default and prints an error message'''
    try:
        element = driver.find_element_by_css_selector(element_selector)
        return element
    except selenium.common.exceptions.NoSuchElementException:
        if DEBUG: print(f"could not find {element_name} on {driver.current_url} with selector {element_selector}.")
        return None

def get_elements(driver, element_selector) -> List[WebElement]:
    '''gets multiple elements from the current page with the selector, or returns a default and prints an error message.

    Note, if no elements are found, then the function returns an empty list.'''

    return driver.find_elements_by_css_selector(element_selector)

def get_element_text_or_default(element: WebElement, default: str) -> str:
    '''returns an elements text or a default string value if element is None.'''
    return element.text if element else default

def start_browser(browser, headless: bool = True):
    '''starts and returns a selenium firefox brower. Takes a paremeter to determine headedness'''
    if browser=='firefox':
        options = Options()
        options.headless = headless

        return webdriver.Firefox(
            executable_path=GeckoDriverManager().install(),
            options=options,
            service_log_path=os.path.devnull
        )
    else:
        options = webdriver.ChromeOptions()
        options.headless= headless
        return webdriver.Chrome(
            executable_path=ChromeDriverManager().install(),
            options=options,
            service_log_path=os.path.devnull
        )

@contextmanager
def wait_for_new_window(driver, timeout: int = 10):
    '''makes sure a new window has loaded before progressing'''
    handles_before = driver.window_handles
    yield
    WebDriverWait(driver, timeout).until(
        lambda driver: len(handles_before) != len(driver.window_handles))

def get_director(detail_text):
    '''uses a regex to extract director from film_details'''
    director = re.findall(FILM_DETAIL_PATTERNS['director'], detail_text)
    return str(director[0]) if director else 'no director found'

def get_description(detail_text):
    '''uses a regex to extract director from film_details'''
    description = re.findall(FILM_DETAIL_PATTERNS['description'], detail_text)
    return str(description[0]) if description else 'no description found'
#
# ----------------------- #
# extraction helpers      #
# ----------------------- #

def get_movie_details(film_links, browser):
    '''Takes a dictionary of film links and gets movie lengths if they haven't already been saved.'''
    film_details_dict = {}
    driver = start_browser(browser)
    with FillingSquaresBar('Gathering Film Details', max=len(film_links), suffix="%(index)d/%(max)d") as bar:
        for k, url in film_links.items():
            driver.get(url)
            film_detail_default = FILM_DETAIL_SEP.join(["not specified", "not specified", "1h 50m"])
            film_details = get_element_text_or_default(
                get_element(driver, GOOGLE_CSS_SELECTORS['film_details'], "film details"),
                film_detail_default
            )

            release_date, film_genre, film_length = film_details.split(FILM_DETAIL_SEP) if len(film_details.split(FILM_DETAIL_SEP))==3 else film_detail_default.split(FILM_DETAIL_SEP)
            try:
                tuple_film_length = tuple(map(int, film_length[:-1].strip().split('h ')))
            except:
                tuple_film_length = (1,50)

            detail_text = get_element_text_or_default(
                get_element(driver, GOOGLE_CSS_SELECTORS['film_description'], "film description"),
                film_detail_default
            )
            cur_film = Film(name=k.strip(), release=release_date.strip(), genre=film_genre.strip(), length=tuple_film_length, description=get_description(detail_text), director=get_director(detail_text))
            film_details_dict[k] = cur_film
            bar.next()
    print("")
    return film_details_dict

def extract_showtimes(showtimes_string: str) -> List[Tuple]:
    '''Takes a string of concatenated standard dates and return a list of military time tuples.'''
    time_pattern = r"\d{1,2}\:\d{2}(?:am|pm)"
    matches = re.findall(time_pattern, showtimes_string)
    tupled_matches = [list(map(int, match[:-2].split(":")))+[match[-2:]] for match in matches]
    military_time_tuples = [tuple([match[0]+12, match[1]]) if match[2] == 'pm' and match[0] != 12
                            else tuple(match[:2]) for match in tupled_matches]
    return military_time_tuples

def get_watchlist_movie_showtimes(movie_showtimes, film_details_dict, watchlist, all_films) -> Dict[Film, List[Showtime]]:
    '''returns a Film object to datetime list dictionary storing all the playtimes for movies found in your watchlist'''
    possible_showtimes = {}
    for movie_name, showtimes in movie_showtimes.items():
        if movie_name.lower() in watchlist or all_films:
            for showtime in showtimes:
                possible_showtimes.setdefault(film_details_dict[movie_name], []).append(showtime)
    return possible_showtimes

def get_address(driver) -> str:
    '''returns the address of a theater or no address if it can't be found'''
    default_address = 'no address found'
    address = get_element_text_or_default(
        get_element(driver, GOOGLE_CSS_SELECTORS['address'], "address"),
        default_address
    )
    return address

def get_showings(driver, theaters):
    '''Function blindly collects showtimes from all favorite theaters.'''
    theater_search_placeholder = "https://www.google.com/search?q={theater_name}+showtimes&lr=lang_en&hl=en"
    movie_showtimes = {}
    film_links = {}
    with FillingSquaresBar('Processing Theaters', max=len(theaters), suffix="%(index)d/%(max)d") as bar:
        for theater in theaters:
            url = theater_search_placeholder.format(theater_name=(theater[:-1].replace(" ", "+")))
            driver.get(url)
            movie_theater = Theater(name=theater[:-1], address=get_address(driver))
            date_s = datetime.datetime.today()
            for day in get_elements(driver, GOOGLE_CSS_SELECTORS['show_days']):
                day.click()
                see_more_button = get_element(driver, GOOGLE_CSS_SELECTORS['see_more'], "see more")
                if see_more_button:
                    if not strtobool(see_more_button.get_attribute('aria-expanded')):
                        driver.execute_script("arguments[0].click();", see_more_button)

                for showing in get_elements(driver, GOOGLE_CSS_SELECTORS['showings']):
                    if not len(showing.text.splitlines()) == 3:
                        continue

                    name, showtimes_string = showing.text.splitlines()[1:]
                    film_links[name] = showing.find_element_by_css_selector('a').get_attribute('href')

                    for showtime in extract_showtimes(showtimes_string):
                        formatted_showtime = date_s.replace(hour=showtime[0], minute=showtime[1])
                        movie_showtimes.setdefault(name, []).append((movie_theater, formatted_showtime))
                date_s += datetime.timedelta(days=1)
            bar.next()
    driver.quit()
    print("Theaters processed...")
    print(f"Number of films found: {len(film_links)}")
    return movie_showtimes, film_links

def get_watchlist_showings(browser, all_films, theaters_name, watchlist_name, headless: bool = True) -> Dict[Film, List[Tuple[Theater, Showtime]]]:
    '''Main function: starts headless browser, gets showtimes, filmlengths and possible showtimes.'''
    driver = start_browser(browser, headless)
    theaters = file_helpers.get_theaters(theaters_name)
    movie_showtimes, film_links = get_showings(driver, theaters)

    watchlist = file_helpers.get_watchlist(watchlist_name)

    if not all_films:
        film_links = {k: v for k, v in film_links.items() if k.lower() in watchlist}
        print(f"Number of films found and in your watchlist: {len(film_links)}")
    film_length_dict = get_movie_details(film_links, browser)
    possible_showtimes = get_watchlist_movie_showtimes(movie_showtimes, film_length_dict, watchlist, all_films)
    return possible_showtimes

if __name__ == "__main__":
    get_watchlist_showings(browser)
