# -*- coding: utf-8 -*-
'''
Module takes a series of showimes and first filters them and then prompts the user to select times.

Currently the only filter is automatically applied and filters sceances during work hours.
Currently the program is not intelligent enough to optimize times or ensure that sceances do not overlap.
'''

DATE_INDEX = 1
ERROR_MESSAGE = {
    "yes_no": "response must be one of the following: 'yes', 'y', 'no', 'n'",
    "showtime_select": "response must be an integer in the range 1-{max_show}"
}

COLOR = {
    'purple': '\033[95m',
    'cyan': '\033[96m',
    'darkcyan': '\033[36m',
    'blue': '\033[94m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'bold': '\033[1m',
    'underline': '\033[4m',
    'end': '\033[0m',
}

def bold(word):
    return COLOR['bold']+word+COLOR['end']

def underline(word):
    return COLOR['underline']+word+COLOR['end']

def not_during_work(showing, workdays, workhours):
    '''takes a datetime and verifies whether it is during work hours or not (default work hours between 8am and 7pm).'''
    date = showing[DATE_INDEX]
    if date.weekday() not in workdays:
        return True
    work_start, work_end = workhours
    now = (date.hour, date.minute)
    return now <= work_start or now >= work_end

def filter_showings(showings, workdays, workhours):
    '''for each movie in your watchlist, filters out showtimes during work hours (currently this is the only filter).'''
    filtered_showings_dict = {}
    for movie, showtimes in showings.items():
        filtered_showings = list(filter(lambda x: not_during_work(x, workdays, workhours), showtimes))
        if filtered_showings:
            filtered_showings_dict[movie] = filtered_showings
    return filtered_showings_dict

def get_input(question, response_format, error_message):
    ''' loops until a response that is in response_format is met'''
    while True:
        res = input(question)
        if res in response_format:
            return res
        print(error_message)

def select_showings(filtered_showings_dict):
    '''for each movie left filtering, asks the user if they want to watch it and provides showtimes to pick from'''
    selected_showings = []
    for movie, showings in filtered_showings_dict.items():
        res = get_input(
            f"Watch '{underline(movie.name)}'?\n{bold('Director')}: {movie.director}\n{bold('Description')}: {movie.description}\n[y/n]: ",
            {'y', 'yes', 'no', 'n'},
            ERROR_MESSAGE['yes_no']
        )
        if(res in {'n', 'no'}):
            print()
            continue
        for i, showing in enumerate(showings, start=1):
            print(f"[{i}]: {showing[1].strftime('%b %d %Y %H:%M')} at {showing[0].name}")
        res = get_input(
            f"select your showing [1-{len(showings)} or n to cancel]: ",
            set(map(str, range(1, len(showings)+1)))|{'n', 'no'},
            ERROR_MESSAGE['showtime_select'].format(max_show=str(len(showings)))
        )
        print()
        if res == 'n':
            continue
        selected_showings.append([movie]+list(showings[int(res)-1]))
    return selected_showings

def filter_select_showings(showings, workdays, workhours):
    '''main function that calls first filter and then select functions'''
    showings = filter_showings(showings, workdays, workhours)
    selected_showings_dict = select_showings(showings)
    return selected_showings_dict
