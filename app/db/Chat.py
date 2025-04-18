# File: Chat.py
from app.utils import mysql_util

def get_user_id(username: str) -> int:
    result = mysql_util.execute_sql("SELECT id FROM User WHERE username=%s", (username,))
    if not result:
        raise ValueError(f"User '{username}' not found")
    print("%s id: %s" % (username, result[0][0]))
    return result[0][0]

def get_item_id(item_name: str) -> int:
    result = mysql_util.execute_sql("SELECT id FROM Item WHERE item_name=%s", (item_name,))
    if not result:
        raise ValueError(f"Item '{item_name}' not found")
    print("%s id: %s" % (item_name, result[0][0]))
    return result[0][0]

def insert_chat(buyer_id: int, seller_id: int, item_id: int) -> int:
    chat_sql = '''
    INSERT INTO Chat (buyer_id, seller_id, item_id)
    VALUES (%s, %s, %s)
    '''
    chat_id = mysql_util.execute_sql(chat_sql, (buyer_id, seller_id, item_id), commit=True, get_lastrowid=True)
    return chat_id

def insert_message(chat_id: int, sender_id: int, content: str, created_at: str = None, is_read: bool = False):
    message_sql = '''
    INSERT INTO Message (chat_id, sender_id, content, created_at, is_read)
    VALUES (%s, %s, %s, %s, %s)
    '''
    mysql_util.execute_sql(message_sql, (chat_id, sender_id, content, created_at, is_read), commit=True)

def insert():
    bigbrovc_id = get_user_id("bigbrovc")
    elif_cato_id = get_user_id("elif_cato")

    harp_id = get_item_id("Roosebeck 22-String Heather Harp w/ Full Chelby Levers")

    time1_str = '2025-04-17 10:00:00'
    time2_str = '2025-04-17 10:05:00'
    time3_str = '2025-04-17 10:10:00'

    # chat 1: bigbrovc <-> elif_cato about the harp
    chat1 = insert_chat(bigbrovc_id, elif_cato_id, harp_id)
    insert_message(chat1, elif_cato_id, "Hi, I love the harp! Is it still available?", created_at=time1_str, is_read=True)
    insert_message(chat1, bigbrovc_id, "Yes! Still available. Do you have any questions?", created_at=time2_str, is_read=True)
    insert_message(chat1, elif_cato_id, "Would you take $150 for it?", created_at=time3_str, is_read=False)

if __name__ == '__main__':
    insert()
