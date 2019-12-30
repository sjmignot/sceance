'''
Starts a Firfox headless brower to see if movies on your watchlist are playing
at any of your favorite theaters.

Favorite theaters are taken from a txt file (extracted from "theaters.txt").
These showtimes are compared to a watchlist (extracted from "watchlist.txt")

-samuel mignot-
'''

import datetime
import re
import collections
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import os

WATCHLIST_FILE = "watchlist.txt"
THEATERS_FILE = "theaters.txt"
GOOGLE_CSS_SELECTORS = {
    "see_more": "div.hide-focus-ring.iXqz2e.aI3msd.xpdarr.pSO8Ic.vk_arc",
    "address": "span.LrzXr",
    "show_days": "li.tb_l",
    "showings": "div.lr_c_fcb.lr-s-stor"
}

Theater = collections.namedtuple('Theater', ['name', 'address'])

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
    with open(WATCHLIST_FILE) as f:
        return frozenset((x[:-1]).lower() for x in f.readlines())

def get_theaters():
    """Reads the theaters file and returns a set of theaters."""
    with open(THEATERS_FILE) as f:
        return f.readlines()

def main(headless=True):
    '''Do X and return a list.'''
    movie_showtimes = {}
    theater_search = "https://www.google.com/search?q={theater_name}+showtimes"

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

    watchlist = get_watchlist()
    theaters = get_theaters()
    for theater in theaters:
        url = theater_search.format(theater_name=(theater[:-1].replace(" ", "+")))
        driver.get(url)
        address = driver.find_element_by_css_selector(GOOGLE_CSS_SELECTORS['address']).text
        movie_theater = Theater(name=theater[:-1], address=address)
        print(f"{movie_theater}\n")
        show_days = driver.find_elements_by_css_selector(GOOGLE_CSS_SELECTORS['show_days'])
        date_s = datetime.datetime.today()
        for i, day in enumerate(show_days):
            try:
                see_more_button = driver.find_element_by_css_selector(
                    GOOGLE_CSS_SELECTORS['see_more']
                )
                driver.execute_script("arguments[0].click();", see_more_button)
                # see_more_button.click()
            except selenium.common.exceptions.NoSuchElementException:
                pass
            day.click()
            showings = driver.find_elements_by_css_selector(GOOGLE_CSS_SELECTORS['showings'])
            for showing in showings:
                if not len(showing.text.splitlines()) == 3:
                    continue
                name, datelist = showing.text.splitlines()[1:]
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
    for key, value in movie_showtimes.items():
        print(key)
        if key.lower() in watchlist:
            print(f"You can watch {key} at:")
            for i in value:
                print(f"- {i[0].name} at {i[1]}")

if __name__ == "__main__":
    main()
