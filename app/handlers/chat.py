# File: chat.py
from flask import request, jsonify, render_template, session, redirect, url_for

from app.utils import mysql_util
from app.utils import photo

def handle_chat():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    sql = '''
    WITH user_chats AS (
        SELECT * FROM Chat
        WHERE buyer_id = %s OR seller_id = %s
    ),
    other_users AS (
        SELECT
            c.id AS chat_id,
            CASE
                WHEN c.buyer_id = %s THEN c.seller_id
                ELSE c.buyer_id
            END AS other_user_id
        FROM user_chats c
    ),
    latest_messages AS (
        SELECT m.chat_id, m.content, m.created_at
        FROM Message AS m
        JOIN (
            SELECT chat_id, MAX(created_at) AS max_time
            FROM Message
            GROUP BY chat_id
        ) AS latest ON m.chat_id = latest.chat_id AND m.created_at = latest.max_time
    GROUP BY chat_id
    )
    SELECT
        c.id AS chat_id,
        u.username AS other,
        i.item_name AS item_name,
        lm.content AS preview,
        lm.created_at AS time
    FROM user_chats AS c
    JOIN other_users AS ou ON c.id = ou.chat_id
    JOIN User AS u ON u.id = ou.other_user_id
    JOIN Item AS i ON c.item_id = i.id
    JOIN latest_messages AS lm ON c.id = lm.chat_id
    ORDER BY lm.created_at ASC;
    '''
    
    chats = mysql_util.execute_sql(
        sql, 
        params=(user_id, user_id, user_id),
        fetchdict=True
    )
    if not chats:
        chats = []

    for chat in chats:
        chat['time'] = chat['time'].strftime('%I:%M %p')
        
    print("chats:", chats)
    
    return render_template("chat.html", chats=chats)
