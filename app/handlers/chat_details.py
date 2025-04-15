# File: chat_details.py
from flask import request, jsonify, render_template, session, redirect, url_for

from app.utils import mysql_util
from app.utils import photo

def handle_chat_details(chat_id: int):
    print("handle_chat_details(chat_id: %s)" % chat_id) 
    
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    if request.method == "POST":
        message_content = request.form.get('message')
        print("recieved inputed message:", message_content)
        if message_content:
            # process message and save it to database
            sql = '''
            INSERT INTO Message (chat_id, sender_id, content)
            VALUES
            (%s, %s, %s);
            '''
            mysql_util.execute_sql(sql, (chat_id, user_id, message_content))

        return redirect(url_for("chat/%s" % chat_id))
    
    elif request.method == "GET":
        # --- all user chats (all are displayed on sidebar) ---
        sidebarsql = """
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
            FROM Message m
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
        ORDER BY lm.created_at DESC;
        """

        chats = mysql_util.execute_sql(
            sidebarsql,
            params=(user_id, user_id, user_id),
            fetchdict=True
        )

        print("chats:", chats)

        # --- details of the currently selected chat ---
        current_chat_sql = """
        SELECT
            m.content,
            m.created_at AS time,
            m.sender_id = %s AS is_sender,
            u.username AS sender_username -- Alias the sender's username
        FROM Message m
        JOIN User u ON m.sender_id = u.id
        WHERE m.chat_id = %s
        ORDER BY m.created_at ASC;
        """

        current_chat_messages = mysql_util.execute_sql(
            current_chat_sql,
            params=(user_id, chat_id),
            fetchdict=True
        )

        # --- other user in the current chat ---
        other_user_info_sql = """
        SELECT
            CASE
                WHEN c.buyer_id = %s THEN seller.username
                ELSE buyer.username
            END AS other_username,
            i.item_name
        FROM Chat c
        JOIN User buyer ON c.buyer_id = buyer.id
        JOIN User seller ON c.seller_id = seller.id
        JOIN Item i ON c.item_id = i.id
        WHERE c.id = %s;
        """

        other_user_info = mysql_util.execute_sql(
            other_user_info_sql,
            params=(user_id, chat_id),
            fetchdict=True,
            fetchone=True
        )

        current_chat_data = {}
        if other_user_info:
            current_chat_data['other'] = other_user_info['other_username']
            current_chat_data['item_name'] = other_user_info['item_name']
            current_chat_data['messages'] = current_chat_messages

        return render_template(
            "chat_details.html",
            chats=chats,
            current_chat=current_chat_data,
            current_chat_id=chat_id
        )

