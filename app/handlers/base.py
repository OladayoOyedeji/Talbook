# File: base.py
from flask import request, render_template, flash, redirect, url_for, session, current_app as app

def handle_base():
    return '''
<h1>Talbook</h1>
    <a href="/signup">
    <button>Signup</button>
    </a>
    <a href="/login">
    <button>Login</button>
    </a>
</html>'''
