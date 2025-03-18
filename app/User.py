# File: User.py
# Description: User class with database functions

from mysql_util import execute_sql

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
