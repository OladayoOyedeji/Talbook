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
    return render_template('search.html', items=items, query=query)
