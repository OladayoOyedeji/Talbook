# File: search_messages.py
from flask import request, jsonify, session

from app.utils import mysql_util

def handle_search_messages():
    try:
        query = request.args.get('query', '').strip()
        if not query:
            return jsonify([])

        user_id = session["user_id"]
        words = query.split()
        where_clauses = []
        params = [user_id, user_id]

        for word in words:
            where_clauses.append("M.content REGEXP %s")
            params.append(f"\\b{word}\\b")

        where_sql = " OR ".join(where_clauses)

        sql = f'''
        SELECT M.id, M.content, M.chat_id
        FROM Message AS M
        JOIN Chat AS C ON C.id = M.chat_id
        WHERE (C.buyer_id = %s OR C.seller_id = %s)
          AND ({where_sql})
        ORDER BY M.id ASC
        LIMIT 4;
        '''

        results = mysql_util.execute_sql(sql, params=params, fetchdict=True)
        return jsonify(results)

    except Exception as e:
        print("Search error:", e)
        return jsonify({'error': 'Internal server error'})
