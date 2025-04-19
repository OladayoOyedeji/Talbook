from flask import request, render_template, flash, redirect, url_for, session, current_app as app
from app.utils.functions import *
from app.utils.User import *
from app.utils.photo import *

def handle_search():
    print(request.args)
    items = None
    query = None
    if request.method == 'POST':
        query = request.form.get('query', '')
        print(query)
        items = get_search_query(query)
        
        print(items)
        if not items:
            flash('no item found')
    return render_template('search.html', items=items, query=query, search_Item=True)

def handle_search_profile():
    print(request.args)
    user_profile = None
    query = None
    if request.method == 'POST':
        query = request.form.get('query', '')
        print(query)
        user_profile = get_search_query_user(query)
        
        print(user_profile)
        if not user_profile:
            flash('no item found')
    return render_template('search.html', user_profile=user_profile, query=query, search_Item=False)
