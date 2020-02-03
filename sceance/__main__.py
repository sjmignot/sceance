'''
run point of application. Calls films to cal module.
Will soon allow configuration and downloading of watchlist.
'''
import configparser
import argparse
import os
from film_to_cal import film_to_cal

# get default settings from settings.ini file
THIS_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
SETTINGS_FILE = "settings.ini"
config = configparser.ConfigParser()
config.read(f"{THIS_DIRECTORY}/{SETTINGS_FILE}")
settings = config['DEFAULT']

# type verification
def valid_timezone(string):
    '''checks whether input string is valid IANA timezone'''
    TIMEZONE_FILE = "timezones.txt"
    with open(f"{THIS_DIRECTORY}/data/{TIMEZONE_FILE}") as f:
        timezones = frozenset([line[:-1] for line in f.readlines()])
    print(timezones)
    if string not in timezones:
        msg = f"{string} is not a IANA timezone"
        raise argparse.ArgumentTypeError(msg)
    return string

def valid_workdays(string):
    '''checks whether string is valid workday'''
    return string

def valid_workhours(string):
    '''checks whether string is valid workhour'''
    return string

# set up argparse
parser = argparse.ArgumentParser(description='Discover which movies in your watchlist are playing in your favorite theaters. You can change defaults by updating the settings.ini file.')

parser.add_argument('-b', '--browser', default=settings['browser'], choices=['firefox', 'chrome'],
        help=f"Whether you want to run a chrome (c) or firefox (f) headless browser (default: {settings['browser']})")

parser.add_argument('-t', '--timezone', type=valid_timezone, default=settings['timezone'],
        help=f"Make sure you provide a valid IANA timezone. (default: {settings['timezone']}).")

parser.add_argument('-d', '--workdays', type=valid_workdays, default=settings['workdays'],
        help=f"Which days you work. A comma seperated list of numbers between 0 and 6 (0 is monday, 1 is tueday, ..., 6 is sunday). (default: {settings['workdays']}).")

parser.add_argument('-w', '--workhours', type=valid_workhours, default=settings['workhours'],
                    help=f"Which hours do you work. Hours are in 24 hour time and formatted: start_hour,end_hour. (default: {settings['workhours']}).")

args = vars(parser.parse_args())

if __name__ == "__main__":
    # film_to_calc
    film_to_cal(args)

    # TODO #

    # add favorite theater

    # update watchlist using letterboxd

    # set busy schedule

    # keep track of films already scheduled and do not promptif sceance has passed
