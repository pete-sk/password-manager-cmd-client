import webbrowser

from set_domain import domain
from connect import get_token
from access_data import download_and_decrypt_user_data, access_data
from manage_data import manage_data
from generate_password import generate_password
from menu import menu


def login():
    print('\nLOGIN')
    email = input('Email: ')
    pswrd = input('Password: ')
    token = get_token(email, pswrd)
    if token == 'enter_security_code':
        security_code = input('Security Code: ')
        token = get_token(email, pswrd, security_code)
    print()
    return pswrd, token


def launch_account_settings(url=f'https://{domain}/account/settings'):
    webbrowser.open(url)
    print('Settings page opened in the default browser.')
    exit()


def main():
    password, token = login()

    if token is False:
        print('Connection failed.')
    elif token == 'invalid_credentials':
        print('Invalid credentials.')
    else:
        encryption_key, decrypted_data = download_and_decrypt_user_data(token, password)

        menu_dict = {'1': ['Access data', access_data, (decrypted_data,)],
                     '2': ['Manage data', manage_data, (decrypted_data, encryption_key, token)],
                     '3': ['Generate password', generate_password, ()],
                     '4': ['Account settings', launch_account_settings, ()]}

        menu(menu_dict, heading='*PASSWORD MANAGER*')


if __name__ == '__main__':
    main()
    input('\nPress enter to exit...')
