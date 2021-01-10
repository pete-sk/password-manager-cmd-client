from connect import get_user_data
from encryption import decrypt, get_key
from menu import menu


class Password:
    count = 1

    def __init__(self, relative_id, id_, name, site, username, password):
        self.relative_id = str(relative_id)
        self.id = id_
        self.name = name
        self.site = site
        self.username = username
        self.password = password


class SecureNote:
    count = 1

    def __init__(self, relative_id, id_, name, content):
        self.relative_id = str(relative_id)
        self.id = id_
        self.name = name
        self.content = content


class CreditCard:
    count = 1

    def __init__(self, relative_id, id_, name, number, expiration_date, cvv, cardholder_name):
        self.relative_id = str(relative_id)
        self.id = id_
        self.name = name
        self.number = number
        self.expiration_date = expiration_date
        self.cvv = cvv
        self.cardholder_name = cardholder_name


def download_and_decrypt_user_data(token, password):
    encrypted_data = get_user_data(token)
    encrypted_master_key = encrypted_data['master_key']
    master_key = decrypt(get_key(password), encrypted_master_key)
    encryption_key = get_key(master_key)

    passwords = []
    for entry_id in encrypted_data['passwords']:
        entry = encrypted_data['passwords'][entry_id]
        entry['name'] = decrypt(encryption_key, entry['name'])
        entry['site'] = decrypt(encryption_key, entry['site'])
        entry['username'] = decrypt(encryption_key, entry['username'])
        entry['password'] = decrypt(encryption_key, entry['password'])

        passwords.append(Password(relative_id=Password.count, id_=entry_id, name=entry['name'], site=entry['site'],
                                  username=entry['username'], password=entry['password']))
        Password.count += 1

    secure_notes = []
    for entry_id in encrypted_data['secure_notes']:
        entry = encrypted_data['secure_notes'][entry_id]
        entry['name'] = decrypt(encryption_key, entry['name'])
        entry['content'] = decrypt(encryption_key, entry['content'])

        secure_notes.append(SecureNote(relative_id=SecureNote.count, id_=entry_id, name=entry['name'],
                                       content=entry['content']))
        SecureNote.count += 1

    credit_cards = []
    for entry_id in encrypted_data['credit_cards']:
        entry = encrypted_data['credit_cards'][entry_id]
        entry['name'] = decrypt(encryption_key, entry['name'])
        entry['number'] = decrypt(encryption_key, entry['number'])
        entry['expiration_date'] = decrypt(encryption_key, entry['expiration_date'])
        entry['cvv'] = decrypt(encryption_key, entry['cvv'])
        entry['cardholder_name'] = decrypt(encryption_key, entry['cardholder_name'])

        credit_cards.append(CreditCard(relative_id=CreditCard.count, id_=entry_id, name=entry['name'],
                                       number=entry['number'], expiration_date=entry['expiration_date'],
                                       cvv=entry['cvv'], cardholder_name=entry['cardholder_name']))
        CreditCard.count += 1

    decrypted_data = {'passwords': passwords, 'secure_notes': secure_notes, 'credit_cards': credit_cards}

    return encryption_key, decrypted_data


def access_data(data):
    passwords = data['passwords']
    secure_notes = data['secure_notes']
    credit_cards = data['credit_cards']

    menu_dict = {'1': ['Passwords', search_passwords, (passwords,)],
                 '2': ['Secure Notes', search_secure_notes, (secure_notes,)],
                 '3': ['Credit Cards', search_credit_cards, (credit_cards,)]}

    menu(menu_dict, heading='ACCESS DATA')


def search_passwords(passwords, query=None, print_results_id=False):
    if not query:
        query = input('Search: ')
    query = query.lower()
    results = []
    if passwords:
        for entry in passwords:
            if query in entry.name.lower() or query in entry.site.lower() or query in entry.username.lower():
                results.append(entry)

    if print_results_id:
        print_passwords(results, print_id=True)
    else:
        print_passwords(results)
    return results


def search_secure_notes(secure_notes, query=None, print_results_id=False):
    if not query:
        query = input('Search: ')
    query = query.lower()
    results = []
    if secure_notes:
        for entry in secure_notes:
            if query in entry.name.lower() or query in entry.content.lower():
                results.append(entry)

    if print_results_id:
        print_secure_notes(results, print_id=True)
    else:
        print_secure_notes(results)
    return results


def search_credit_cards(credit_cards, query=None, print_results_id=False):
    if not query:
        query = input('Search: ')
    query = query.lower()
    results = []
    if credit_cards:
        for entry in credit_cards:
            if query in entry.name.lower() or query in entry.number.lower() \
                    or query in entry.cardholder_name.lower():
                results.append(entry)

    if print_results_id:
        print_credit_cards(results, print_id=True)
    else:
        print_credit_cards(results)
    return results


def print_num_of_entries(num_of_entries):
    if num_of_entries == 0:
        print('No results...')
    else:
        print('Found ' + str(num_of_entries) + ' matching entries.')


def print_passwords(passwords, print_id=False):
    print_num_of_entries(len(passwords))

    for password in passwords:
        print()
        if print_id:
            print('#' + password.relative_id)
        print('Name: ' + password.name)
        print('Site: ' + password.site)
        print('Username: ' + password.username)
        print('Password: ' + password.password)


def print_secure_notes(secure_notes, print_id=False):
    print_num_of_entries(len(secure_notes))

    for secure_note in secure_notes:
        print()
        if print_id:
            print('#' + secure_note.relative_id)
        print('Name: ' + secure_note.name)
        print('Content: ' + secure_note.content)


def print_credit_cards(credit_cards, print_id=False):
    print_num_of_entries(len(credit_cards))

    for credit_card in credit_cards:
        print()
        if print_id:
            print('#' + credit_card.relative_id)
        print('Name: ' + credit_card.name)
        print('Number: ' + credit_card.number)
        print('Expiration date: ' + credit_card.expiration_date)
        print('CVV: ' + credit_card.cvv)
        print('Cardholder name: ' + credit_card.cardholder_name)
