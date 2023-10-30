import getpass
import logging

import keyring
import keyring.errors

SERVICE_NAME = "tubtools"


def fallback():
    pw = getpass.getpass('Password:')
    return pw


def load_credentials(username):
    log = logging.getLogger(__name__)

    try:
        return keyring.get_credential(SERVICE_NAME, username)
    except keyring.errors.KeyringError:
        log.error('Could not get credentials from keyring!')


def store_credentials(username, pw):
    keyring.set_password(SERVICE_NAME, username, pw)


def clear_credentials(username):
    try:
        keyring.delete_password(SERVICE_NAME, username)
    except keyring.errors.PasswordDeleteError:
        pass  # Fail silently
