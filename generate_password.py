from random import randint
import pyperclip


def generate_password(user_input=True, length=16, lower='Y', upper='Y', numbers='Y', special='Y'):

    if user_input:
        while True:
            length = input('Enter password length: ')
            try:
                length = int(length)
                if length > 0:
                    break
                else:
                    print('Password length must be greater than zero!')
            except ValueError:
                print('Please enter a positive integer!')
                continue

        lower = input('Include lowercase characters? Y/N: ').upper()
        upper = input('Include uppercase characters? Y/N: ').upper()
        numbers = input('Include numbers? Y/N: ').upper()
        special = input('Include special characters? Y/N: ').upper()

    lowchars = 'qwertyuiopasdfghjklzxcvbnm'
    upchars = lowchars.upper()
    nums = '1234567890'
    specialchars = '!@#$%^&*()'

    scope = ''

    if lower == 'Y':
        scope += lowchars

    if upper == 'Y':
        scope += upchars

    if numbers == 'Y':
        scope += nums

    if special == 'Y':
        scope += specialchars

    password = ''

    if scope:
        for i in range(length):
            password += scope[randint(0, len(scope)-1)]
    else:
        if user_input:
            print('\nYou must include at least one group of characters!')
        return

    if user_input:
        print('\nGenerated password: ' + password)
        if_copy = input('Copy to clipboard? Y/N: ').upper()
        if if_copy == 'Y':
            pyperclip.copy(password)
            print('\nPassword copied to clipboard.')

    return password
