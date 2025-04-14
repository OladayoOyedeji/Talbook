# File: chat_details.py
from flask import request, jsonify, render_template, session, redirect, url_for

from app.utils import mysql_util
from app.utils import photo

def handle_chat_details(chat_id: int):
    # Sample data for all chats in sidebar
    chats = [
        {
            "chat_id": "1",
            "sender": "emutlu",
            "item_name": "Harp",
            "preview": "Hey, just wanted to check in and give a quick update on the project status...",
            "time": "10:42 AM"
        },
        {
            "chat_id": "2",
            "sender": "jane_doe",
            "item_name": "Guitar",
            "preview": "Thanks for the quick response! I'll get back to you...",
            "time": "Yesterday"
        },
        {
            "chat_id": "3",
            "sender": "mike_smith",
            "item_name": "Piano",
            "preview": "The meeting is scheduled for tomorrow at 2 PM",
            "time": "Mar 15"
        }
    ]
    
    # Sample message data for the currently selected chat
    current_chat = {
        "chat_id": str(chat_id),
        "sender": "emutlu",
        "item_name": "Harp",
        "messages": [
            {
                "content": "Hey there! How's the harp working for you? I love harps and I hope you do to. It was great to come to Columbia.",
                "time": "10:30 AM",
                "is_sender": False
            },
            {
                "content": "It's great! The sound quality is amazing.",
                "time": "10:35 AM",
                "is_sender": True
            },
            {
                "content": "That's awesome to hear! Let me know if you need any tips.",
                "time": "10:40 AM",
                "is_sender": False
            },
            {
                "content": "Will do, thanks for checking in!",
                "time": "10:42 AM",
                "is_sender": True
            },
            {
                "content": "Hey there! How's the harp working for you? I love harps and I hope you do to. It was great to come to Columbia.",
                "time": "10:30 AM",
                "is_sender": False
            },
            {
                "content": "It's great! The sound quality is amazing.",
                "time": "10:35 AM",
                "is_sender": True
            },
            {
                "content": "That's awesome to hear! Let me know if you need any tips.",
                "time": "10:40 AM",
                "is_sender": False
            },
            {
                "content": "Will do, thanks for checking in!",
                "time": "10:42 AM",
                "is_sender": True
            },
            {
                "content": "Hey there! How's the harp working for you? I love harps and I hope you do to. It was great to come to Columbia.",
                "time": "10:30 AM",
                "is_sender": False
            },
            {
                "content": "It's great! The sound quality is amazing.",
                "time": "10:35 AM",
                "is_sender": True
            },
            {
                "content": "That's awesome to hear! Let me know if you need any tips.",
                "time": "10:40 AM",
                "is_sender": False
            },
            {
                "content": "Will do, thanks for checking in!",
                "time": "10:42 AM",
                "is_sender": True
            }
        ]
    }
    
    # Find the current chat in the chats list to get the preview info
    for chat in chats:
        if chat['chat_id'] == str(chat_id):
            current_chat.update({
                "preview": chat["preview"],
                "time": chat["time"]
            })
            break
    
    return render_template(
        "chat_details.html",
        chats=chats,
        current_chat=current_chat,
        current_chat_id=str(chat_id)
    )
