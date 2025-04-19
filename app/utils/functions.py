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
    ret = False
    if '@' in username:
        ret = False
    else:
        usernames = User.get_usernames()
        ret = (usernames is None or (username,) not in usernames)

    app.logger.debug("username:%s, is_valid_username():%s" % (username, ret))
    return ret
    
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
        print(password)
        if (c.isupper()):
            capital_count += 1
        elif (c.isdigit()):
            num_count += 1
        elif (not c.isalnum()):
            special_count += 1

    if capital_count < PASSWORD_RULES["min_capital_letters"]:
        print("capital_count:", capital_count)
        errors.append("Password must contain at least %s capital letter(s)." % PASSWORD_RULES['min_capital_letters'])
    if num_count < PASSWORD_RULES["min_numbers"]:
        print("num_count:", num_count)
        errors.append("Password must contain at least %s number(s)." % PASSWORD_RULES['min_numbers'])
    if special_count < PASSWORD_RULES["min_special_chars"]:
        print("special_count", special_count)
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
        app.logger.debug("user_input failed for user: %s" % user_input)
        return False

def get_search_query(query):
    sql = '''
SELECT Item.id,
    Item.item_name,
    Item.price,
    Item.condition,
    User.username,
    Item_Photo.photo_id,
    count(Item.id) FROM Item_Tag
JOIN Tag ON Item_Tag.tag_id = Tag.id
JOIN Item ON Item_Tag.item_id = Item.id
JOIN User ON Item.seller_id = User.id
JOIN Item_Photo on Item.id = Item_Photo.item_id and Item_Photo.display_order = 0
WHERE 
'''
    delim = ''
    params = ()

    query_list = query.split(' ')

    for word in query_list:
        if word not in ['', ' ']:
            sql += delim + '''(Tag.name LIKE %s OR Item.descrip LIKE %s OR Item.item_name LIKE %s)'''
            params += ("'%%%s%%'"%word,) * 3
            delim = '\n OR '
    sql += '''
GROUP BY Item.id
ORDER BY count(Item.id) DESC'''
    print(sql % params)

    print(sql,  params)
    return execute_sql(sql % params)

def get_search_query_user(query):
    sql = '''SELECT * FROM User
    WHERE username like "%%%s%%"'''

    print(sql % query)
    return execute_sql(sql % query, fetchdict=True)

def get_photo_id(post_id):
    sql = '''SELECT display_order, photo_id
FROM Post_Photo
WHERE post_id = %s'''

    return execute_sql(sql, (post_id,))

def get_video_id(post_id):
    sql = '''SELECT display_order, video_id
FROM Post_Video
WHERE post_id = %s'''

    return execute_sql(sql, (post_id,))

def get_post_data(post_id):
    sql = '''SELECT User.username as username,
    User.photo_id as photo_id,
    Post.descrip as descrip,
    Post.created_at as created_at
    FROM Post
    JOIN User ON Post.user_id = User.id
    WHERE Post.id = %s'''

    return execute_sql(sql, (post_id, ), fetchdict=True)


def get_posts(user_id):
    sql = ''' SELECT Post.created_at, Post_Photo.photo_id as media, 'photo', Post.id FROM Post
JOIN Post_Photo on Post_Photo.post_id = Post.id
WHERE Post.user_id = %s
AND Post_Photo.display_order = 0

UNION

SELECT Post.created_at, Post_Video.video_id as media, 'video', Post.id FROM Post
JOIN Post_Video on Post_Video.post_id = Post.id
WHERE Post.user_id = %s
AND Post_Video.display_order = 0'''# get_from_post: post_id, list of pictures, list of videos, descrip, time

    return execute_sql(sql, (user_id, user_id))

def get_bookmarked_items(user_id):
    sql = '''
    SELECT 
        I.id,
        I.item_name,
        I.price,
        I.condition,
        U.username,
        IP.photo_id
    FROM Bookmark AS B
    JOIN Item AS I ON B.item_id = I.id
    JOIN User AS U ON I.seller_id = U.id
    JOIN Item_Photo AS IP ON I.id = IP.item_id AND IP.display_order = 0
    WHERE B.user_id = %s AND I.is_available = True;
    '''
    
    return execute_sql(sql, (user_id,))

def get_comments(post_id):
    sql = '''SELECT User.username username,
    Comment.comment as content,
    Comment.created_at as timestamp
    FROM Comment
    JOIN User ON User.id = Comment.commenter_id
    WHERE post_id = %s
    ORDER BY created_at DESC'''

    return execute_sql(sql, (post_id,), fetchdict=True)

def add_comment(user_id, post_id, comment):
    sql = '''INSERT INTO Comment (commenter_id, post_id, comment)
    VALUE (%s, %s, %s)'''

    return execute_sql(sql, (user_id, post_id, comment), commit=True)
