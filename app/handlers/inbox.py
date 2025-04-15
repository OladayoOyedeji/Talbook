# File: inbox.py
from flask import request, jsonify, render_template, session, redirect, url_for

from app.utils import mysql_util
from app.utils import photo

def handle_inbox():
    chats = [
        {
            "chat_id": "1",
            "sender": "emutlu",
            "item_name": "Harp",
            "preview": "Hey, just wanted to check in and give a quick update on the project status...",
            "time": "10:42 AM"
        }
    ]
    
    return render_template("inbox.html", chats=chats)
