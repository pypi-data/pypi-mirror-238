import sys

import requests
import bs4

from .credentials import load_credentials, store_credentials, fallback


def login(user, pw, url, shib_url):
    s = requests.Session()
    s.get(url)  # Create a flow for this session

    r = s.get(shib_url)  # We will be redirected so save response

    # I have no idea what this does but without this first post we cant login
    payload = {
        'shib_idp_ls_exception.shib_idp_session_ss':'',
        'shib_idp_ls_success.shib_idp_session_ss': True,
        'shib_idp_ls_value.shib_idp_session_ss': '',
        'shib_idp_ls_exception.shib_idp_persistent_ss': '',
        'shib_idp_ls_success.shib_idp_persistent_ss': True,
        'shib_idp_ls_value.shib_idp_persistent_ss': '',
        'shib_idp_ls_supported': '',
        '_eventId_proceed': True
    }
    r = s.post(r.url, data=payload)

    payload = {
        'j_username': user,
        'j_password': pw,
        '_eventId_proceed': ''
    }

    r = s.post(r.url, data=payload)

    soup = bs4.BeautifulSoup(r.content, features="lxml")
    form = soup.find("form")
    saml_endpoint = form['action']

    payload =   {}
    for field in form.find_all("input"):
        try:
           payload[field['name']] = field['value']
        except KeyError:
            pass

    r = s.post(saml_endpoint, data=payload)

    for h in r.history:
        for c in h.cookies.keys():
            if '_shibsession_' in c:
                return s

    return None


def interactive_login(url: str, shib_url: str, user=None, pw=None, store_creds=False):
    credential = load_credentials(user)
    user = user or (credential.username if credential else None) or input('Username:')

    if not pw:
        credential = load_credentials(user)  # may have changed
        if credential:
            pw = credential.password
        else:
            pw = fallback()
            store_creds = store_creds or input('Save pw? [Y/n]:') in ['', 'Y', 'y']

    s = login(user, pw, url, shib_url)

    if s is None:
        print('Login failed!')
        sys.exit(1)

    if store_creds:
        store_credentials(user, pw)

    return user, pw, s
