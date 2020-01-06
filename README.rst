***********
sceance
***********

Installation
############

To start running sceance, install the project and enable the Google calendar API.

Dependencies
============
- A Letterboxd account: sceance currently provides a way of downloading your watchlist from letterboxd provided you store your letterboxd credentials in a .envrc file. This is done by the `update_watchlist.py` file.

- A Google Account: for sceance to create and suggest events to your calendar.

- Firefox: to run the selenium headless browser to find film showings

Download the app
================
Currently film-to-cal is not available on pip, but you can clone it directly from this repository.

.. code-block:: console
   git clone git@github.com:sjmignot/film-to-cal.git

Then, install the dependencies by running the following line:


Enable the Google calendar API
==============================

To enable the Google calendar API, you need to download a credentials file from the following link and place it in the `film_to_cal/film_to_calc/data` subfolder. This file can be downloaded from:

`https://developers.google.com/calendar/quickstart/python?hl=en#step_1_turn_on_the`

How it works
############
