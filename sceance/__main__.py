'''
run point of application. Calls films to cal module.
Will soon allow configuration and downloading of watchlist.
'''
import configparser
import argparse
import os
from film_to_cal import film_to_cal
from set_watchlist import set_watchlist
from set_theaters import set_theaters

# get default settings from settings.ini file
THIS_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
SETTINGS_FILE = "settings.ini"
CRED_FILE = "credentials.json"
config = configparser.ConfigParser()
config.read(f"{THIS_DIRECTORY}/data/{SETTINGS_FILE}")
settings = config['DEFAULT']

# TYPE VERIFICATION
def valid_timezone(timezone_input):
    '''checks whether input string is valid IANA timezone'''
    TIMEZONE_FILE = "timezones.txt"
    with open(f"{THIS_DIRECTORY}/data/{TIMEZONE_FILE}") as f:
        timezones = frozenset([line[:-1] for line in f.readlines()])
    if timezone_input not in timezones:
        msg = f"{timezone_input} is not a IANA timezone"
        raise argparse.ArgumentTypeError(msg)
    return timezone_input

def valid_workdays(workdays_input):
    '''checks whether string is valid workday'''
    msg = f"{workdays_input} is not a valid workdays input. Your input should be a subset of [0,1,2,3,4,5,6] presented as a comma seperated string. ex: 1,2,4."
    try:
        workdays = set(map(int, workdays_input.split(',')))
    except:
        raise argparse.ArgumentTypeError(msg)
    if workdays.issubset(set(range(6))):
        return workdays
    raise argparse.ArgumentTypeError(msg)

def valid_workhours(workhours_input):
    '''checks whether string is valid workhour'''
    msg = f"{workhours_input} is not a valid workhours input. Your input should be two comma-seperated integers between 0 and 23 inclusive. ex. (10,20). These designate the start of work hours and the end of work hours"
    try:
        work_start, work_end = map(int, workhours_input.split(","))
    except:
        raise argparse.ArgumentTypeError(msg)
    if 23>work_start>0 and 23>work_end>0:
        return ((work_start,0), (work_end,0))
    raise argparse.ArgumentTypeError(msg)

def check_for_google_credentials():
    if not os.path.exists(f"{THIS_DIRECTORY}/data/{CRED_FILE}"):
        print(f"WARNING: {THIS_DIRECTORY}/data/{CRED_FILE} does not exist. sceance will be unable to add events to your google calender. To fix this, check the instructions on enabling the google calendar API (https://github.com/sjmignot/sceance#enable-the-google-calendar-api).")

def set_up_argparse():
    '''SET UP ARGPARSE'''
    parser = argparse.ArgumentParser(description='Discover which movies in your watchlist are playing in your favorite theaters. You can change defaults by updating the data/settings.ini file.')

    parser.add_argument('-b', '--browser', default=settings['browser'], choices=['firefox', 'chrome'], help=f"use chrome or firefox headless browser (default: {settings['browser']}).")

    parser.add_argument('-a', '--all-films', action='store_true', help=f"suggest all films instead of filtering based on watchlist.txt.")

    parser.add_argument('-d', '--workdays', type=valid_workdays, default=settings['workdays'], help=f"which days do you work? A comma seperated list of numbers between 0 and 6 (0 is monday, 1 is tueday, ..., 6 is sunday). (default: {settings['workdays']}).")

    parser.add_argument('-w', '--workhours', type=valid_workhours, default=settings['workhours'], help=f"Which hours do you work? Hours are in 24 hour time and formatted: start_hour,end_hour. (default: {settings['workhours']}).")

    parser.add_argument('-t', '--timezone', type=valid_timezone, default=settings['timezone'], help=f"What timezone do you live in? Make sure you provide a valid IANA timezone. This is used by the google calendar api. (default: {settings['timezone']}).")

    parser.add_argument('-v', '--version', action='version', version='0.5.5')

    parser.add_argument('-s', '--set-watchlist', action='store_true', help=f"change the default watchlist from {settings['watchlist']}.")

    parser.add_argument('-c', '--set-theaters', action='store_true', help=f"change the default theaters file from {settings['theaters']}.")

    return vars(parser.parse_args())

def main():
    args = set_up_argparse()
    if args['set_watchlist']:
        watchlist = set_watchlist()
        if watchlist:
            config.set('DEFAULT', 'watchlist', watchlist)
            with open(f"{THIS_DIRECTORY}/data/{SETTINGS_FILE}", 'w') as configfile:
                config.write(configfile)
            print(f"watchlist set to {watchlist}")
        else:
            print(f"watchlist remains unchanged as {settings['watchlist']}")
        return
    if args['set_theaters']:
        theaters =  set_theaters()
        if theaters:
            config.set('DEFAULT', 'theaters', theaters)
            with open(f"{THIS_DIRECTORY}/data/{SETTINGS_FILE}", 'w') as configfile:
                config.write(configfile)
            print(f"theaters file set to {theaters}")
        else:
            print(f"theaters file remains unchanged as {settings['theaters']}")
        return
    args['watchlist'] = settings['watchlist']
    args['theaters'] = settings['theaters']
    check_for_google_credentials()
    film_to_cal(args)

# MAIN FUNCTION: CALLS FILM TO CAL
if __name__ == "__main__":
    main()
    '''
     TODO #
    - add favorite theater
    - update watchlist using letterboxd
    - set busy schedule
    - keep track of films already scheduled and do not prompt if sceance has passed
    '''
