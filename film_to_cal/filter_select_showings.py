# -*- coding: utf-8 -*-

import datetime

WORK_START = (8,0)
WORK_END = (19,00)
WEEKDAYS = set(range(0,5))
DATE_INDEX = 1

def not_during_work(showing):
    date = showing[DATE_INDEX]
    if date.weekday() not in WEEKDAYS: return True

    now = (date.hour, date.minute)
    print(now)
    return now <= WORK_START or now >= WORK_END

def filter_showings(showings):
    filtered_showings_dict = {}
    for movie, showtimes in showings.items():
        filtered_showings = list(filter(not_during_work, showtimes))
        if len(filtered_showings) > 0:
            filtered_showings_dict[movie] = filtered_showings
    return filtered_showings_dict

def select_showings(filtered_showings_dict):
    selected_showings = {}
    for movie, showings in filtered_showings_dict.items():
        inp = input(f"Watch {movie.name}? [y/n] ")
        if(inp=='n'):
            continue
        for i, showing in enumerate(showings, start=1):
            print(f"[{i}]: {showing[1].strftime('%b %d %Y %H:%M')} at {showing[0].name}")
        inp = input(f"select your showing [1-{len(showings)} or n to cancel]: ")
        if(inp=='n'): continue
        selected_showings[movie] = showings[int(inp)-1]
    return selected_showings


def filter_select_showings(showings):
    filtered_showings_dict = filter_showings(showings)
    selected_showings_dict = select_showings(filtered_showings_dict)
    print(selected_showings_dict)
