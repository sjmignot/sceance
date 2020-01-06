import requests
import os

SIGN_IN_PAGE = "https://letterboxd.com/user/login.do"
EXPORT_PAGE = "https://letterboxd.com/data/export"
REFERER = "https://letterboxd.com/activity/"

SIGN_IN_ID_EL = "username"
SIGN_IN_PW_EL = "password"
COOKIE_NAME = "com.xk72.webparts.csrf"

payload = {
    SIGN_IN_ID_EL: os.environ['LBXD_USERNAME'],
    SIGN_IN_PW_EL: os.environ['LBXD_PASSWORD']
}

def update_watchlist():
    with requests.Session() as s:
        s.get(SIGN_IN_PAGE)
        if COOKIE_NAME in s.cookies:
            payload['__csrf'] = s.cookies[COOKIE_NAME]

        p = s.post(SIGN_IN_PAGE, data=payload, headers={'referer': REFERER})
        r = s.get(EXPORT_PAGE)

        print(r.content)

        with open('data/lbdata.zip', 'wb') as f:
            f.write(r.content)

if __name__ == "__main__":
    update_watchlist()
