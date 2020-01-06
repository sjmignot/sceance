'''
interact with your update_watchlist by downloading watchlist from letterboxd.
'''

import os
import requests
import zipfile
import pandas as pd

SIGN_IN_PAGE = "https://letterboxd.com/user/login.do"
EXPORT_PAGE = "https://letterboxd.com/data/export"
REFERER = "https://letterboxd.com/activity/"

SIGN_IN_ID_EL = "username"
SIGN_IN_PW_EL = "password"
COOKIE_NAME = "com.xk72.webparts.csrf"
ZIP_FILE = 'data/lb_data.zip'
WATCHLIST_CSV = 'watchlist.csv'
DATA = 'data/'
WATCHLIST_TXT = 'watchlist.txt'

payload = {
    SIGN_IN_ID_EL: os.environ['LBXD_USERNAME'],
    SIGN_IN_PW_EL: os.environ['LBXD_PASSWORD']
}


def extract_watchlist():
    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        zip_ref.extract(WATCHLIST_CSV, path=DATA)
    os.remove(ZIP_FILE)
    watchlist = list(pd.read_csv(f'data/{WATCHLIST_CSV}')['Name'])
    with open(f"{DATA}{WATCHLIST_TXT}", 'w') as f:
        f.write("\n".join(watchlist))
    os.remove(f"{DATA}{WATCHLIST_CSV}")

def download_watchlist():
    '''update watchlist by '''
    with requests.Session() as session:
        session.get(SIGN_IN_PAGE)
        if COOKIE_NAME in session.cookies:
            payload['__csrf'] = session.cookies[COOKIE_NAME]

        # sign in
        session.post(SIGN_IN_PAGE, data=payload, headers={'referer': REFERER})
        letterboxd_content = session.get(EXPORT_PAGE)

        with open(ZIP_FILE, 'wb') as f:
            f.write(letterboxd_content.content)

def update_watchlist():
    download_watchlist()
    extract_watchlist()

    pass

if __name__ == "__main__":
    update_watchlist()
