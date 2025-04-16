# File: start_chat.py
from flask import request, jsonify, render_template, session, redirect, url_for

from app.utils import mysql_util

def handle_start_chat(seller_id: int, item_id: int):
    buyer_id = session['user_id']
    
    # prevent users from messaging themselves
    if buyer_id == seller_id:
        return "You cannot message yourself."

    # check if a chat already exists between these two users
    existing_chat_sql = '''
    SELECT id FROM Chat
    WHERE buyer_id = %s AND seller_id = %s AND item_id = %s;
    '''
    existing_chat = mysql_util.execute_sql(existing_chat_sql, (buyer_id, seller_id, item_id),
                                       fetchone=True, fetchdict=True)
    
    if existing_chat:
        print("chat already exists. redirecting")
        chat_id = existing_chat['id']
        return redirect("/chat/%s" % chat_id)
    else:
        # create a new chat in the database
        insert_chat_sql = '''
        INSERT INTO Chat (buyer_id, seller_id, item_id)
        VALUES (%s, %s, %s);
        '''
        chat_id = mysql_util.execute_sql(insert_chat_sql, (buyer_id, seller_id, item_id), commit=True, get_lastrowid=True)
        print("chat created for id", chat_id)
        return redirect("/chat/%s" % chat_id)
