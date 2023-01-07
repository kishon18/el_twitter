from TwitterSystem import *


# check for empty input
def field_cant_be_blank(variable):
    while not variable:
        variable = input(Fore.RED + '== ATTENTION! == Field can not be blank. Enter something: ')
        return field_cant_be_blank(variable)
    return variable


def registration_nickname():
    if not Users_dict:
        first_name = field_cant_be_blank(input('Input your first name: '))
        second_name = field_cant_be_blank(input('Input your second name: '))

    elif Users_dict:
        while True:
            first_name = field_cant_be_blank(input('Input your first name: '))
            second_name = field_cant_be_blank(input('Input your second name: '))

            nickname = f'@{first_name.strip().capitalize()}{second_name.strip().capitalize()}'

            has_duplicate = False
            for inst in Users_dict.values():
                if nickname == inst.nickname:
                    print(Fore.RED + f'\n{system_info_header:=^25}')
                    print(f'| Your nickname will consist of First and Second names. But "{nickname}" '
                          f'already in use. Please change something in your data. For example, use underscore 😉.\n')
                    has_duplicate = True
                    break
            if not has_duplicate:
                break
    return first_name, second_name


def registration_email():
    if not Users_dict:
        email = field_cant_be_blank(input('Input your e-mail: '))

    elif Users_dict:
        while Users_dict:
            email = field_cant_be_blank(input('Input your e-mail: '))

            has_duplicate = False
            for inst in Users_dict.values():
                if email == inst._email:
                    print(Fore.RED + f'\n{system_info_header:=^25}')
                    print(f'This email already used. Try another one')
                    print()
                    has_duplicate = True
                    break
            if not has_duplicate:
                break
    return email


def registration_psw():
    psw = field_cant_be_blank(input('Create a password: '))
    return psw


def login_user():
    email = field_cant_be_blank(input('Input your e-mail: '))
    psw = field_cant_be_blank(input('Input your password: '))
    return email, psw


