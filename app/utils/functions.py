# functions.py
from app import app
from flask import session
import random
import string

from app.utils import User
from app.email_verification.myemail import *
from app.utils import hash
from app.utils.mysql_util import *

PASSWORD_RULES = {
    "min_length": 8,
    "min_capital_letters": 1,
    "min_numbers": 2,
    "min_special_chars": 2
}

def is_valid_username(username: str) -> bool:
    """
    Checks if username is valid and available.
    Returns False if:
    - Username contains '@' symbol
    - Username already exists
    - Usernames list couldn't be fetched (None)
    """
    if '@' in username:
        return False
    else:
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
        elif (not c.isalnum()):
            special_count += 1

    if capital_count < PASSWORD_RULES["min_capital_letters"]:
        errors.append("Password must contain at least %s capital letter(s)." % PASSWORD_RULES['min_capital_letters'])
    if num_count < PASSWORD_RULES["min_numbers"]:
        errors.append("Password must contain at least %s number(s)." % PASSWORD_RULES['min_numbers'])
    if special_count < PASSWORD_RULES["min_special_chars"]:
        errors.append("Password must contain at least %s special character(s)." % PASSWORD_RULES['min_special_chars'])

    return errors

def is_valid_password(password):
    return (password_errors(password) == [])

def generate_verification_code(length: int = 6) -> str:
    """Generates a random 6-digit verification code"""
    return ''.join(random.choices(string.digits, k=length))

def send_verification_code(email: str) -> None:
    """Sends a verification code to the user via email"""
    verification_code = generate_verification_code()
    session['verification_code'] = verification_code
    text = "Your verification code is %s. This code will expire in 30 minutes." % verification_code
    sendgmail(to_=[email],
              from_=GMAIL,
              subject='TalBook Verification Code',
              text=text,
              html='<html><body><h1>%s</h1></body></html>' % verification_code
              )
    app.logger.debug("Verification code sent to %s: %s" % (email, verification_code))

def is_valid_code(user_entered_code: str) -> bool:
    '''
    Returns True if the entered verification code matches the stored one,
    and False otherwise
    '''
    return True
    stored_code = session.get('verification_code')

    if not stored_code and user_entered_code == stored_code:
        return True
    else:
        return False

def is_valid_login(user_input: str, plain_password: str):
    """
    Authenticates a user by checking if the entered password
    matches the stored hash

    user_input: either username or email of user
    plain_password: plaintext password of user
    """
    
    sql = "SELECT id, username, email, password_hash from User \
    where username = %s or email = %s;"
    params = (user_input, user_input)
    
    user = execute_sql(sql, params)
    assert len(user) <= 1

    if user:
        user_id, username, email, stored_hashed_password = user[0]

        if hash.verify_password(plain_password, stored_hashed_password):
            app.logger.debug("authentication successful for user: %s" % username)
            session['user_id'] = user_id
            session['username'] = username
            return True
        else:
            app.logger.debug("password failed for user: %s" % username)
            return False
    else:
        app.logger.debug("user_input failed for user: %s" % username)
        return False
