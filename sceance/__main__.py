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
config.read(f"{THIS_DIRECTORY}/data/{SETTINGS_FILE}")
settings = config['DEFAULT']

# TYPE VERIFICATION
def valid_timezone(timezone_input):
    '''checks whether input string is valid IANA timezone'''
    TIMEZONE_FILE = "timezones.txt"
    with open(f"{THIS_DIRECTORY}/data/{TIMEZONE_FILE}") as f:
        timezones = frozenset([line[:-1] for line in f.readlines()])
    if timezone_input not in timezones:
        msg = f"{string} is not a IANA timezone"
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

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def set_up_argparse():
    '''SET UP ARGPARSE'''
    parser = argparse.ArgumentParser(description='Discover which movies in your watchlist are playing in your favorite theaters. You can change defaults by updating the data/settings.ini file.')

    parser.add_argument('-b', '--browser', default=settings['browser'], choices=['firefox', 'chrome'], help=f"Whether you want to run a chrome or firefox headless browser (default: {settings['browser']}).")

    parser.add_argument('-a', '--all-films', action='store_true', help=f"If you want all films instead of filtering based on your watchlist.txt file. (default: False).")

    parser.add_argument('-d', '--workdays', type=valid_workdays, default=settings['workdays'], help=f"Which days you work. A comma seperated list of numbers between 0 and 6 (0 is monday, 1 is tueday, ..., 6 is sunday). (default: {settings['workdays']}).")

    parser.add_argument('-w', '--workhours', type=valid_workhours, default=settings['workhours'], help=f"Which hours do you work. Hours are in 24 hour time and formatted: start_hour,end_hour. (default: {settings['workhours']}).")

    parser.add_argument('-t', '--timezone', type=valid_timezone, default=settings['timezone'], help=f"Make sure you provide a valid IANA timezone. Used by the google calendar api. (default: {settings['timezone']}).")

    parser.add_argument('-v', '--version', action='version', version='0.3.1')

    return vars(parser.parse_args())

def main():
    args = set_up_argparse()
    print(args)
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
