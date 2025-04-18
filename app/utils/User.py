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

import os
from app import app

from .mysql_util import execute_sql
from .hash import *
 
def get_usernames():
    sql = '''
    SELECT username from User
    '''
    ret = execute_sql(sql)
    app.logger.debug(ret)
    return ret

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
    INSERT INTO User (username, email, password_hash, descrip)
    VALUES (%s, %s, %s, %s)
    '''
    return execute_sql(sql, (username, email, password_hash, descrip), commit=True)

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

def follow(follower_id, followed_id):
    sql = '''
    INSERT INTO Follow (follower_id, followed_id)
    VALUE (%s, %s)'''

    return execute_sql(sql, (follower_id, followed_id), commit=True)
    
def unfollow(follower_id, followed_id):
    sql = '''
    DELETE FROM Follow 
    WHERE follower_id = %s AND followed_id = %s'''

    return execute_sql(sql, (follower_id, followed_id), commit=True)

def get_follower_list(user_id):
    sql = '''
    SELECT follower_id FROM Follow
    WHERE follower_id = %s
    '''
    return execute_sql(sql, (user_id,))

def get_followed_list(user_id):
    sql = '''
    SELECT followed_id FROM Follow
    WHERE followed_id = %s
    '''
    return execute_sql(sql, (user_id,))

def is_following(follower_id, followed_id):
    sql = '''
    SELECT * FROM Follow WHERE follower_id = %s AND followed_id = %s'''
    
    return execute_sql(sql, (follower_id, followed_id))

def get_listed_items(user_id):
    sql = '''
    SELECT id FROM item
    WHERE seller_id = %s
    '''
    return execute_sql(sql, (user_id,))

def get_user_id(username):
    sql = '''
    SELECT id FROM User
    WHERE username = %s
    '''
    return execute_sql(sql, (user_id,))

def get_image_link(username):
    sql = '''
    SELECT photo_id FROM User
    WHERE username = %s
    '''
    photo_id = execute_sql(sql, (username,))[0][0]

    print(type(photo_id), str(photo_id), os.path.join('/static/images','%s.jpg' % photo_id), '\n')
    return os.path.join('/static/images','%s.jpg' % photo_id)

def get_skills():
    sql = '''
    SELECT skills, id FROM Service
    '''
    return execute_sql(sql)

def get_services(user_id):
    sql = '''
    SELECT Service.skills FROM User_Service
    JOIN Service ON User_Service.service_id = Service.id
    WHERE User_Service.user_id = %s
    '''

    return execute_sql(sql, (user_id))

def get_listings(user_id):

    sql = '''
       SELECT 
            I.id,
            I.item_name,
            I.price,
            I.condition,
            U.username,
            IP.photo_id
        FROM Item as I
        JOIN User as U ON I.seller_id=U.id
        JOIN Item_Photo as IP ON I.id=IP.item_id and IP.display_order=0
        WHERE I.seller_id = %s AND is_available=True;
    '''

    return execute_sql(sql, (user_id))

def get_data(username):
    sql = '''
    SELECT * FROM User
    WHERE username = %s
    '''

    return execute_sql(sql, (username,), False, False, False, True)

def update_username(profile, username):
    if profile['username'] != username:
        sql = '''
        UPDATE User SET username = %s WHERE id=%s
        '''
        return execute_sql(sql, (username,profile['id']), True)

def update_email(profile, email):
    if profile['email'] != email:
        sql = '''
        UPDATE User SET email = %s WHERE id=%s
        '''
        return execute_sql(sql, (email,profile['id']), True)

def update_descrip(profile, descrip):
    if profile['descrip'] != descrip:
        sql = '''
        UPDATE User SET descrip = %s WHERE id=%s
        '''
        return execute_sql(sql, (descrip,profile['id']), True)

def update_services(profile, add_skills, delete_skills):
    print(add_skills)
    sql = ""
    if add_skills or delete_skills :
        delim = ""
        if add_skills:
            sql = '''
            INSERT INTO User_Service (user_id, service_id)
            VALUES '''
            
            delim = "("
            
            for skill in add_skills:
                sql += delim + str(profile['id']) + ',' + str(skill)
                delim = '),\n('
            sql += ');'
        if delete_skills:
            sql += '''
            DELETE FROM User_Service WHERE '''
            
            for skill in delete_skills:
                sql += delim + "service_id = %s" % skill
                delim = "\nOR "
                
        print(sql)
        
        return execute_sql(sql, (), commit=True)
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
