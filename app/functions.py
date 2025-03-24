import sys

PASSWORD_RULES = {
    "min_length": 8,
    "min_capital_letters": 1,
    "min_numbers": 2,
    "min_special_chars": 2
}

'''
# Validation.py
password_entered = False
password_valid = True
valid_length = 8
no_capital_letters = 1
no_integers = 2
no_special_char = 2
user = None
'''

def is_valid_username(username: str) -> bool:
    return True
    usernames = User.get_usernames()
    return (usernames == None or username not in usernames) 

def invalid_message_password():
    return'password has to be a minimum of %(i)s characters \
    containing %(j)s capital letters, %(k)s integers, %(l)s \
    special characters'\
    %{'i':PASSWORD_RULES['min_length'], 'j':PASSWORD_RULES['min_capital_letters'],
      'k':PASSWORD_RULES['min_numbers'], 'l':PASSWORD_RULES['min_special_chars']}


def password_errors(password: str) -> list:
    ''' 
    Returns a list of error messages if password does
    NOT meet complexity requirements.
    Returns an empty list if the password is valid.
    '''
    
    errors = []
    
    if len(password) < PASSWORD_RULES["min_length"]:
        errors.append("Password must be at least %s characters long." % PASSWORD_RULES['min_length'])

    capital_count = 0
    num_count = 0
    special_count = 0
    for c in password:
        if (c.isupper()):
            capital_count += 1
        elif (c.isdigit()):
            num_count += 1
        elif (c.isalnum()):
            special_count += 1
    print(capital_count, num_count, special_count)
    if capital_count < PASSWORD_RULES["min_capital_letters"]:
        errors.append("Password must contain at least %s capital letter(s)." % PASSWORD_RULES['min_capital_letters'])
    if num_count < PASSWORD_RULES["min_numbers"]:
        errors.append("Password must contain at least %s number(s)." % PASSWORD_RULES['min_numbers'])
    if special_count < PASSWORD_RULES["min_special_chars"]:
        errors.append("Password must contain at least %s special character(s)." % PASSWORD_RULES['min_special_chars'])

    return errors

def is_valid_password(password):
    # return True
    return (password_errors(password) == [])

# sends code to specified email. To validate the email,
# they must input the code
def is_valid_email(email):
    return True

def send_verification_code():
    return None

def is_valid_code():
    return False
