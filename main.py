from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import urllib
import datetime
import re
import collections

WATCHLIST_FILE = "watchlist.txt"
THEATERS_FILE = "theaters.txt"

Theater = collections.namedtuple('Theater', ['name', 'address'])

movie_showtimes = {}

theater_search = "https://www.google.com/search?q={theater_name}+showtimes"

def get_dates(datelist):
    date_pattern = r"\d{1,2}\:\d{2}(?:am|pm)"
    matches = re.findall(date_pattern, datelist)
    tupled_matches = [list(map(int, match[:-2].split(":")))+[match[-2:]] for match in matches]
    print(tupled_matches)
    tupled_matches = [tuple([match[0]+12, match[1]]) if match[2]=='pm' else tuple(match[:2]) for match in tupled_matches]
    print(tupled_matches)
    return tupled_matches

def get_watchlist():
    with open(WATCHLIST_FILE) as f:
        return set([(x[:-1]).lower() for x in f.readlines()])

options = Options()
options.headless = True

profile = webdriver.FirefoxProfile()
profile.set_preference('intl.accept_languages', 'en_GB')

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), firefox_profile=profile, options=options)

def get_theaters():
    with open(THEATERS_FILE) as f:
        return f.readlines()

watchlist = get_watchlist()
theaters = get_theaters()
for theater in theaters:
    url = theater_search.format(theater_name=(theater[:-1].replace(" ", "+")))
    print(url)
    driver.get(url)
    address = driver.find_element_by_css_selector("span.LrzXr").text
    movie_theater = Theater(name=theater[:-1], address=address)
    print(movie_theater)
    print("")
    show_days = driver.find_elements_by_css_selector("li.tb_l")
    date_s = datetime.datetime.today()
    for i, day in enumerate(show_days):
        try:
            x = driver.find_element_by_css_selector("div.hide-focus-ring.iXqz2e.aI3msd.xpdarr.pSO8Ic.vk_arc")
            x.click()
        except:
            pass
        date_s += datetime.timedelta(days=1)
        print(date_s)
        day.click()
        showings = driver.find_elements_by_css_selector("div.lr_c_fcb.lr-s-stor")
        for showing in showings:
            if(not len(showing.text.splitlines())==3): continue
            name, datelist = showing.text.splitlines()[1:]
            print(name)
            print(datelist)
            show_times = get_dates(datelist)
            for show_time in show_times:
                if name in movie_showtimes.keys():
                    movie_showtimes[name].append((movie_theater, date_s.replace(hour=show_time[0], minute=show_time[1])))
                else:
                    movie_showtimes[name] = [(movie_theater, date_s.replace(hour=show_time[0], minute=show_time[1]))]

print(movie_showtimes)
print(watchlist)
for key,value in movie_showtimes.items():
    print(key)
    if key.lower() in watchlist:
        print(f"You can watch {key} at:")
        for i in value:
            print(f"- {i[0].name} at {i[1]}")

driver.quit()
