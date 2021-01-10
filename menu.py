"""
MENU DICTIONARY TEMPLATE
menu_dict = {'1': ['Option', function, (arg1, arg2 ...)],
             '2': ['Option', function, (arg,)]}  # tuple of single arg MUST be a tuple
"""


def menu(menu_dict, heading=None):

    # prints menu
    menu_str = ''
    for k, v in menu_dict.items():
        menu_str += f'{str(k)}. {str(v[0])}    '
    if heading:
        print(heading.center(len(menu_str)))
    print(menu_str)

    # asks user which function to run
    while True:
        mode_sel = input('Enter number: ')
        if mode_sel in menu_dict.keys():
            break
    print()

    # calls the selected function
    func = menu_dict[mode_sel][1]
    args = menu_dict[mode_sel][2]
    func(*args)
