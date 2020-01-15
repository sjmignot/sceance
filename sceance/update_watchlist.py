'''
update your watchlist by signing into your letterboxd account and exporting your content from the site to a local watchlist.txt file.
'''

#IMPORTS

import os
import os.path

import zipfile
import requests
import pandas as pd

# CONTSTANTS

# letterboxd urls

SIGN_IN_PAGE = "https://letterboxd.com/user/login.do"
EXPORT_PAGE = "https://letterboxd.com/data/export"
REFERER = "https://letterboxd.com/activity/"

# other constants

SIGN_IN_ID_EL = "username"
SIGN_IN_PW_EL = "password"
COOKIE_NAME = "com.xk72.webparts.csrf"
ZIP_FILE = 'data/lb_data.zip'
WATCHLIST_CSV = 'watchlist.csv'
DATA = 'data/'
WATCHLIST_TXT = 'data/watchlist.txt'

MY_PATH = os.path.abspath(os.path.dirname(__file__))

def extract_watchlist():
    '''extracts the watchlist from  the downloaded letterboxd content'''
    zip_file = os.path.join(MY_PATH, ZIP_FILE)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extract(WATCHLIST_CSV, path=os.path.join(MY_PATH, DATA))
    os.remove(zip_file)

    watchlist_csv = os.path.join(MY_PATH, f"{DATA}{WATCHLIST_CSV}")
    watchlist = list(pd.read_csv(watchlist_csv)['Name'])
    watchlist_txt = os.path.join(MY_PATH, WATCHLIST_TXT)
    with open(watchlist_txt, 'w') as f:
        f.write("\n".join(watchlist))
    os.remove(watchlist_csv)

def download_letterboxd_content():
    '''signs you into letterboxd and then downloads the content'''
    login_payload = {
        SIGN_IN_ID_EL: os.environ['LBXD_USERNAME'],
        SIGN_IN_PW_EL: os.environ['LBXD_PASSWORD']
    }

    with requests.Session() as session:
        session.get(SIGN_IN_PAGE)
        if COOKIE_NAME in session.cookies:
            login_payload['__csrf'] = session.cookies[COOKIE_NAME]

        # sign in
        session.post(SIGN_IN_PAGE, data=login_payload, headers={'referer': REFERER})
        letterboxd_content = session.get(EXPORT_PAGE)

        with open(ZIP_FILE, 'wb') as f:
            f.write(letterboxd_content.content)

def update_watchlist():
    '''updates your watchlist by downloading letterboxd content and then extracting it'''
    download_letterboxd_content()
    extract_watchlist()

if __name__ == "__main__":
    update_watchlist()
