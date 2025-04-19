# File: home.py
from flask import session, redirect, url_for, render_template, flash
from app.utils import mysql_util
from app.utils.functions import *

def handle_home():
    username = session.get('username')
    if username:
        sql = '''
       SELECT 
            I.id,
            I.item_name,
            I.price,
            I.condition,
            U.username,
            IP.photo_id
        FROM Item as I
        JOIN User as U ON I.seller_id=U.id
        JOIN Item_Photo as IP ON I.id=IP.item_id and IP.display_order=0
        WHERE is_available=True;
        '''
        items = mysql_util.execute_sql(sql)

        sql = '''
        SELECT User.username as username,
        User.photo_id as photo_id,
        Post.descrip as descrip,
        Post.id as post_id,
        Post.created_at as created_at
        FROM Post
        JOIN Follow ON Follow.followed_id = Post.user_id
        JOIN User ON Post.user_id = User.id
        WHERE Follow.follower_id = %s'''

        Posts = mysql_util.execute_sql(sql, (session['user_id'],), fetchdict=True)

        for i in range(len(Posts)):
            post_id = Posts[i]['post_id']
            list_of_photo = [ x + ('photo',) for x in get_photo_id(post_id)]
            list_of_video = [ x + ('video',) for x in get_video_id(post_id)]
            

            list_of_media = list_of_photo + list_of_video

            list_of_media.sort()
        
            Posts[i]['media'] = list_of_media
            Posts[i]['comments'] = get_comments(post_id)
    
        print(Posts)
    
        return render_template("homepage.html", items=items, Posts=Posts, user={'username': username})
    else:
        flash("You must log in to view this page.")
        return redirect(url_for('login'))
