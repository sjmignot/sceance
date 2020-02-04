# sceance

Sceance is an application for moviegoers. If you provide it with a list of your favorite cinemas and your movie watchlist, it suggests showtimes, letting you watch your favorite movies in theaters.

It was designed with Paris, a city full of small and independent cinemas, in mind.

## Installation

To start running sceance, install the project and enable the Google calendar API.

### Dependencies

Most dependencies are optional:

- **A Google Account**: for sceance to create and suggest events to your calendar.

- **Firefox or Chrome**: to run the selenium headless browser to find film showings.

- **A Letterboxd account**: sceance currently provides a way of downloading your watchlist from letterboxd provided you store your letterboxd credentials in a .envrc file. This is done with the `update_watchlist.py` file. Otherwise you can manually create a watchlist as a list of newline seperated film titles.

### Download the app

You can install sceance with pip.
```sh
pip install sceance
```

To run sceance, simply call:
```sh
sceance
```

To get information on parameters run:
```sh
sceance -h
```

At this point, sceance can suggest films, but is unable to automatically add events to your google calendar.

If you want scence to add films to your calendar, you need to [enable the google calendar API](#enable-the-google-calendar-api).

### Enable the Google calendar API

To enable the Google calendar API, you need to download a credentials file from the following link and place it in the `sceance/sceance/data` subfolder. This file can be downloaded from:

`https://developers.google.com/calendar/quickstart/python?hl=en#step_1_turn_on_the`

## How sceance works

Sceance uses selenium to gather showtime information for every theater in your theater.txt file, from Google. These films are then intersected with your watchlist. Details on the resulting films and their showtimes are then filtered out based on 9am-5pm monday-friday work hours.

For all the films that remain, you are prompted with a list of showtimes and can select one showtime per film.

This showtime is then automatically added to your calendar using the google calendar api. Note, for now this requires that you [enable the Google calendar API](#enable-the-google-calendar-api): doing this allows sceance to write to your calendar.

## Contribution Guidelines

No contribution guidelines yet.
