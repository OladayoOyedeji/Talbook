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
            mysql_util.execute_sql(sql, (chat_id, user_id, message_content), commit=True)

        return redirect("/chat/%s" % chat_id)
    
    elif request.method == "GET":
        # --- other user in the current chat ---
        other_user_info_sql = """
        SELECT
            CASE
                WHEN c.buyer_id = %s THEN seller.username
                ELSE buyer.username
            END AS other_username,
            CASE
                WHEN c.buyer_id = %s THEN c.seller_id
                ELSE c.buyer_id
            END AS other_user_id,
            i.item_name
        FROM Chat AS c
        JOIN User buyer ON c.buyer_id = buyer.id
        JOIN User seller ON c.seller_id = seller.id
        JOIN Item i ON c.item_id = i.id
        WHERE c.id = %s;
        """

        other_user_info = mysql_util.execute_sql(
            other_user_info_sql,
            params=(user_id, user_id, chat_id),
            fetchdict=True,
            fetchone=True
        )
        
        # mark messages as read
        updatesql = '''
        UPDATE Message SET is_read = True
        WHERE chat_id = %s AND sender_id = %s;
        '''
        mysql_util.execute_sql(updatesql,
                           (chat_id, other_user_info["other_user_id"]),
                            commit=True)
        
        # --- all user chats (all are displayed on sidebar) ---
        sidebarsql = '''
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
    ),
    unread_counts AS (
    SELECT
        chat_id,
        COUNT(*) AS unread_count
    FROM Message
    WHERE chat_id IN (SELECT id FROM user_chats)
      AND sender_id != %s
      AND is_read = False
    GROUP BY chat_id
    )
    SELECT
        c.id AS chat_id,
        u.username AS other,
        i.item_name AS item_name,
        lm.content AS preview,
        lm.created_at AS time,
        COALESCE(uc.unread_count, 0) AS unread_count
    FROM user_chats AS c
    JOIN other_users AS ou ON c.id = ou.chat_id
    JOIN User AS u ON u.id = ou.other_user_id
    JOIN Item AS i ON c.item_id = i.id
    JOIN latest_messages AS lm ON c.id = lm.chat_id
    LEFT JOIN unread_counts AS uc ON c.id = uc.chat_id
    ORDER BY lm.created_at DESC;
    '''
        
        chats = mysql_util.execute_sql(
            sidebarsql,
            params=(user_id, user_id, user_id, user_id),
            fetchdict=True
        )

        for chat in chats:
          chat['time'] = chat['time'].strftime('%I:%M %p')
          
        print("chats:", chats)

        # --- details of the currently selected chat ---
        current_chat_sql = """
        SELECT
            m.content,
            m.created_at AS time,
            m.sender_id AS sender_id,
            u.username AS sender_username
        FROM Message m
        JOIN User u ON m.sender_id = u.id
        WHERE m.chat_id = %s
        ORDER BY m.created_at ASC;
        """

        current_chat_messages = mysql_util.execute_sql(
            current_chat_sql,
            params=(chat_id),
            fetchdict=True
        )

        print("current_chat_messages:", current_chat_messages)

        current_chat_data = {}
        if other_user_info:
            current_chat_data['other'] = other_user_info['other_username']
            current_chat_data['item_name'] = other_user_info['item_name']
            current_chat_data['messages'] = current_chat_messages

        return render_template(
            "chat_details.html",
            chats=chats,
            current_chat=current_chat_data,
            current_chat_id=chat_id,
            user_id=user_id
        )

