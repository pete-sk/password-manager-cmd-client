from connect import post_user_data
from access_data import search_passwords, search_secure_notes, search_credit_cards
from generate_password import generate_password
from encryption import encrypt
from menu import menu


def manage_data(data, encryption_key, token):
    menu_dict = {'1': ['Add entry', add_data, (encryption_key, token)],
                 '2': ['Edit entry', edit_data, (data, encryption_key, token)],
                 '3': ['Delete entry', delete_data, (data, token)]}

    menu(menu_dict, heading='MANAGE DATA')


def add_data(encryption_key, token):
    menu_dict = {'1': ['Password', add_password, (encryption_key, token)],
                 '2': ['Secure Note', add_secure_note, (encryption_key, token)],
                 '3': ['Credit Card', add_credit_card, (encryption_key, token)]}

    menu(menu_dict, heading='ADD')


def edit_data(data, encryption_key, token):
    passwords = data['passwords']
    secure_notes = data['secure_notes']
    credit_cards = data['credit_cards']

    menu_dict = {'1': ['Password', edit_password, (passwords, encryption_key, token)],
                 '2': ['Secure Note', edit_secure_note, (secure_notes, encryption_key, token)],
                 '3': ['Credit Card', edit_credit_card, (credit_cards, encryption_key, token)]}

    menu(menu_dict, heading='EDIT')


def delete_data(data, token):
    passwords = data['passwords']
    secure_notes = data['secure_notes']
    credit_cards = data['credit_cards']

    menu_dict = {'1': ['Password', delete_password, (passwords, token)],
                 '2': ['Secure Note', delete_secure_note, (secure_notes, token)],
                 '3': ['Credit Card', delete_credit_card, (credit_cards, token)]}

    menu(menu_dict, heading='DELETE')


def add_password(encryption_key, token):
    print('NEW PASSWORD')
    entry = input_password()
    encrypted_entry = encrypt_password(encryption_key, entry)
    if not confirm_save():
        return
    data = {'action': 'add', 'data_type': 'password', 'data': encrypted_entry}
    response = post_user_data(token, data)
    print_save_response(response)


def add_secure_note(encryption_key, token):
    print('NEW SECURE NOTE')
    entry = input_secure_note()
    encrypted_entry = encrypt_secure_note(encryption_key, entry)
    if not confirm_save():
        return
    data = {'action': 'add', 'data_type': 'secure_note', 'data': encrypted_entry}
    response = post_user_data(token, data)
    print_save_response(response)


def add_credit_card(encryption_key, token):
    print('NEW CREDIT CARD')
    entry = input_credit_card()
    encrypted_entry = encrypt_credit_card(encryption_key, entry)
    if not confirm_save():
        return
    data = {'action': 'add', 'data_type': 'credit_card', 'data': encrypted_entry}
    response = post_user_data(token, data)
    print_save_response(response)


def edit_password(passwords, encryption_key, token):
    results = search_passwords(passwords, print_results_id=True)
    to_edit = ask_for_id(passwords, results)

    for password in passwords:
        if password.relative_id == to_edit:
            print(f'\nEDIT ENTRY #{to_edit}')
            entry = input_password()
            encrypted_entry = encrypt_password(encryption_key, entry)
            encrypted_entry_with_id = {password.id: encrypted_entry}
            if not confirm_save():
                return
            data = {'action': 'edit', 'data_type': 'password', 'data': encrypted_entry_with_id}
            response = post_user_data(token, data)
            print_save_response(response)


def edit_secure_note(secure_notes, encryption_key, token):
    results = search_secure_notes(secure_notes, print_results_id=True)
    to_edit = ask_for_id(secure_notes, results)

    for secure_note in secure_notes:
        if secure_note.relative_id == to_edit:
            print(f'\nEDIT ENTRY #{to_edit}')
            entry = input_secure_note()
            encrypted_entry = encrypt_secure_note(encryption_key, entry)
            encrypted_entry_with_id = {secure_note.id: encrypted_entry}
            if not confirm_save():
                return
            data = {'action': 'edit', 'data_type': 'secure_note', 'data': encrypted_entry_with_id}
            response = post_user_data(token, data)
            print_save_response(response)


def edit_credit_card(credit_cards, encryption_key, token):
    results = search_credit_cards(credit_cards, print_results_id=True)
    to_edit = ask_for_id(credit_cards, results)

    for credit_card in credit_cards:
        if credit_card.relative_id == to_edit:
            print(f'\nEDIT ENTRY #{to_edit}')
            entry = input_credit_card()
            encrypted_entry = encrypt_credit_card(encryption_key, entry)
            encrypted_entry_with_id = {credit_card.id: encrypted_entry}
            if not confirm_save():
                return
            data = {'action': 'edit', 'data_type': 'credit_card', 'data': encrypted_entry_with_id}
            response = post_user_data(token, data)
            print_save_response(response)


def delete_password(passwords, token):
    results = search_passwords(passwords, print_results_id=True)
    to_delete_relative_id = ask_for_id(passwords, results)
    if not confirm_delete(to_delete_relative_id):
        return
    for entry in passwords:
        if entry.relative_id == to_delete_relative_id:
            to_delete = entry.id
            data = {'action': 'delete', 'data_type': 'password', 'data': to_delete}
            response = post_user_data(token, data)
            print_delete_response(response)


def delete_secure_note(secure_notes, token):
    results = search_secure_notes(secure_notes, print_results_id=True)
    to_delete_relative_id = ask_for_id(secure_notes, results)
    if not confirm_delete(to_delete_relative_id):
        return
    for entry in secure_notes:
        if entry.relative_id == to_delete_relative_id:
            to_delete = entry.id
            data = {'action': 'delete', 'data_type': 'secure_note', 'data': to_delete}
            response = post_user_data(token, data)
            print_delete_response(response)


def delete_credit_card(credit_cards, token):
    results = search_credit_cards(credit_cards, print_results_id=True)
    to_delete_relative_id = ask_for_id(credit_cards, results)
    if not confirm_delete(to_delete_relative_id):
        return
    for entry in credit_cards:
        if entry.relative_id == to_delete_relative_id:
            to_delete = entry.id
            data = {'action': 'delete', 'data_type': 'credit_card', 'data': to_delete}
            response = post_user_data(token, data)
            print_delete_response(response)


def input_password():
    name = input('Name: ')
    site = input('Site: ')
    if not name and site:
        name = site
    elif not name and not site:
        name = '(unnamed)'
    username = input('Username: ')
    generate = input('Do you want to generate a password? Y/N: ').upper()
    if generate == 'Y':
        print()
        while True:
            password = generate_password()
            if password:
                break
    else:
        password = input('Password: ')
    entry = {'name': name, 'site': site, 'username': username, 'password': password}
    return entry


def input_secure_note():
    name = input('Name: ')
    if not name:
        name = '(unnamed)'
    content = input('Content: ')
    entry = {'name': name, 'content': content}
    return entry


def input_credit_card():
    name = input('Name: ')
    if not name:
        name = '(unnamed)'
    number = input('Number: ')
    expiration_date = input('Expiration date (MM/YY): ')
    cvv = input('CVV: ')
    cardholder_name = input('Cardholder name: ')
    entry = {'name': name, 'number': number, 'expiration_date': expiration_date, 'cvv': cvv,
             'cardholder_name': cardholder_name}
    return entry


def encrypt_password(encryption_key, entry):
    entry['name'] = encrypt(encryption_key, entry['name'])
    entry['site'] = encrypt(encryption_key, entry['site'])
    entry['username'] = encrypt(encryption_key, entry['username'])
    entry['password'] = encrypt(encryption_key, entry['password'])
    return entry


def encrypt_secure_note(encryption_key, entry):
    entry['name'] = encrypt(encryption_key, entry['name'])
    entry['content'] = encrypt(encryption_key, entry['content'])
    return entry


def encrypt_credit_card(encryption_key, entry):
    entry['name'] = encrypt(encryption_key, entry['name'])
    entry['number'] = encrypt(encryption_key, entry['number'])
    entry['expiration_date'] = encrypt(encryption_key, entry['expiration_date'])
    entry['cvv'] = encrypt(encryption_key, entry['cvv'])
    entry['cardholder_name'] = encrypt(encryption_key, entry['cardholder_name'])
    return entry


def ask_for_id(all_entries, results):
    while True:
        id_ = input('\nEnter id of the entry to select: ')
        if id_ not in [entry.relative_id for entry in all_entries]:
            print('Selected entry does not exist!')
        elif id_ not in [entry.relative_id for entry in results]:
            proceed = input('Selected entry not included in the search results! '
                            'Are you sure want to proceed? Y/N: ').upper()
            if proceed == 'Y':
                return id_
        else:
            return id_


def confirm_save():
    confirmation = input(f'\nSave entry? Y/N: ').upper()
    if confirmation == 'Y':
        return True
    else:
        print('\nCancelled.')
        return False


def confirm_delete(id_):
    confirmation = input(f'Are you sure want to delete entry #{id_} permanently? Y/N: ').upper()
    if confirmation == 'Y':
        return True
    else:
        print('\nCancelled.')
        return False


def print_save_response(response):
    if response.status_code == 200:
        print('\nEntry saved successfully.')
    elif response.status_code == 401:
        print('\nSession expired. Please log in and try again.')
        exit(0)
    else:
        print('\nCould not save the entry. Please try again.')


def print_delete_response(response):
    if response.status_code == 200:
        print('\nEntry deleted successfully.')
    elif response.status_code == 401:
        print('\nSession expired. Please log in and try again.')
        exit(0)
    else:
        print('\nCould not delete the entry. Please try again.')
