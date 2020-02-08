# sceance
<p align="center">
  ![sceance logo](/sceance.svg)
</p>

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

To enable the Google calendar API, you need to download a credentials file from the following link and place it in the `sceance/sceance/data` subfolder. This file can be downloaded from the [calendar API documentation](https://developers.google.com/calendar/quickstart/python?hl=en#step_1_turn_on_the). Call the file `credentials.json`.

I'm in the process of implementing a cleaner authentication process.

### Customize theaters.txt

By default, the theaters.txt file contains a set of my favorite Parisian movie theaters. If you live somewhere else (or want to add your own set of favorite theaters), you have to customize the file: you can find it in the data subfolder of the sceance package.

### Customize watchlist.txt

By default, the watchlist.txt contains every film from the criterion collection. However, to get the most from sceance, you should use a personal watchlist.

If you have a letterboxd account, sceance provides a way to automatically download your watchlist. To do this, use the `update_watchlist.py` file (you will need to store your letterboxd credentials in environment variables).

Make sure your watchlist is in English (which is currently the only language that sceance supports). If you want to run sceance without providing a watchlist, you can use the `-a` flag, but this might provide you with a lot of movies.

You can find the `watchlist.txt` file in the data subfolder of the sceance package.

## How sceance works

Sceance uses selenium to gather showtime information for every theater in your theater.txt file, from Google. These films are then intersected with your watchlist. Details on the resulting films and their showtimes are then filtered out based on 9am-5pm monday-friday work hours (both workdays and hours are customizable).

For all the films that remain, you are prompted with a list of showtimes and can select one showtime per film.

This showtime is then automatically added to your calendar using the google calendar api. Note, for now this requires that you [enable the Google calendar API](#enable-the-google-calendar-api): doing this allows sceance to write to your calendar.

## Contribution Guidelines

No contribution guidelines yet.
