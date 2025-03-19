# File: User.py
# Description: User class with database functions
'''
CREATE TABLE User
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    photo_id INT, -- profile picture
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    descrip TEXT,
    FOREIGN KEY (photo_id) REFERENCES Photo(id)
) ENGINE=InnoDB;
'''

from .mysql_util import execute_sql
import bcrypt
 
def get_usernames():
    sql = '''
    SELECT username from User
    '''
    return execute_sql(sql)

##==============================================================
## Password Hashing Functions
## https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/
##==============================================================
def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.
    
    password: The plaintext password to hash
    return: The hashed password as a string
    """
    # generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # convert bytes to string

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plaintext password against a hashed password.
    
    plain_password: The plaintext password to verify
    hashed_password: The hashed password to compare against
    return: True if the passwords match, False otherwise
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

##==============================================================
## User Registration and Login Functions
##==============================================================
def register_user(username: str, email: str, password: str, descrip: str = None, photo_id: int = None):
    """
    Registers a new user by hashing their password and storing their details in the database.

    username: The user's username
    email: The user's email
    password: The user's plaintext password
    descrip: Optional description of the user
    photo_id: Optional profile picture ID
    """

    # hash the password
    password_hash = hash_password(password)

    # insert the user into the database
    sql = '''
    INSERT INTO User (username, email, password_hash, descrip, photo_id)
    VALUES (%s, %s, %s, %s, %s)
    '''
    execute_sql(sql, (username, email, password_hash, descrip, photo_id))

##==============================================================
## Helper Functions
##==============================================================
def get_preference(user_id):
    sql = '''
    SELECT subcategory_id, weight FROM User_Preference
    WHERE user_id = %s
    '''
    return execute_sql(sql, (user_id,))

def get_transaction_history(user_id):
    sql = '''
    SELECT id FROM Purchase_History
    WHERE user_id = %s
    '''
    return execute_sql(sql, (user_id,))

def get_follower_list(user_id):
    sql = '''
    SELECT follower_id FROM Follow
    WHERE followed_id = %s
    '''
    return execute_sql(sql, (user_id,))

def get_followed_list(user_id):
    sql = '''
    SELECT followed_id FROM Follow
    WHERE followed_id = %s
    '''
    return execute_sql(sql, (user_id,))

def get_listed_items(user_id):
    sql = '''
    SELECT id FROM item
    WHERE seller_id = %s
    '''
    return execute_sql(sql, (user_id,))

##==============================================================
## User Class
##==============================================================
class User:
    def __init__(self, id):
        self.id = id
        self.preferences = get_preference(self.id)
        self.transaction_history = get_transaction_history(self.id)
        self.follower_list = get_follower_list(self.id)
        self.followed_list = get_followed_list(self.id)
        self.listed_items = get_listed_items(self.id)
