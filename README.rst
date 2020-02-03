***********
sceance
***********

Sceance is an application for moviegoers. If you provide it with a list of your favorite cinemas and your movie watchlist, it suggests showtimes, letting you watch your favorite movies in theaters.

It was designed with Paris, or other cities full of independent and small cinemas, in mind.

Installation
############

To start running sceance, install the project and enable the Google calendar API.

Dependencies
============

Most dependencies are optional
- **A Letterboxd account**: sceance currently provides a way of downloading your watchlist from letterboxd provided you store your letterboxd credentials in a .envrc file. This is done with the `update_watchlist.py` file. Otherwise you can manually create a watchlist as a list of newline seperated film titles.

- **A Google Account**: for sceance to create and suggest events to your calendar.

- **Firefox**: to run the selenium headless browser to find film showings (with a little customization to `get_showings.py` you can use google chrome instead).

Download the app
================
Currently sceance is not available on pip, but you can clone it directly from this repository.

.. code-block:: console

   git clone git@github.com:sjmignot/film-to-cal.git

Then, install the dependencies by running the following line:

.. code-block:: console

   pip install -r requirements.txt

Enable the Google calendar API
==============================

To enable the Google calendar API, you need to download a credentials file from the following link and place it in the `film_to_cal/film_to_calc/data` subfolder. This file can be downloaded from:

`https://developers.google.com/calendar/quickstart/python?hl=en#step_1_turn_on_the`

How it works
############

Sceance uses selenium to gather showtime information for every theater in your theater.txt file, from Google. These films are then intersected with your watchlist. Details on the resulting films and their showtimes are then filtered out based on 9am-5pm work hours. For all the films that remain, you are prompted with a list of showtimes and can select one.

This showtime is then automatically added to your calendar using the google calendar api. Note, for now this requires that :ref:`you download a credentials.json file from g<Enable the Google calendar API>`: doing this allows sceance to write to your calendar.

Contribution Guidelines
#######################

