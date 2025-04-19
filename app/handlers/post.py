import os
from flask import request, render_template, flash, redirect, url_for, session, current_app as app
from werkzeug.utils import secure_filename
import json
import uuid
from app.utils.functions import *
from app.utils.User import *
from app.utils.photo import *
from app.utils.video import *

def delete_post(post_id):
    sql = '''DELETE FROM Post WHERE id %s'''

    return execute_sql(sql, (post_id,), commit=True)

def handle_post(post_id):
    # get post informations
    list_of_photo = [ x + ('photo',) for x in get_photo_id(post_id)]
    list_of_video = [ x + ('video',) for x in get_video_id(post_id)]
    

    list_of_media = list_of_photo + list_of_video

    list_of_media.sort()

    post = get_post_data(post_id)[0]
    print(post)
    post['media'] = list_of_media
    post['comments'] = get_comments(post_id)
    
    if request.method == 'POST':
        new_comment = request.form.get('content')

        if new_comment:
            add_comment(session['user_id'], post_id, new_comment)
            post['comments'] = get_comments(post_id)
    print(post)
    return render_template('post.html', post=post)
    
def handle_add_post():
    # create_a_post_id
    if request.method=='POST':
        list_media = request.files.getlist('media')
        descrip = request.form.get('description')
        
        sql = '''INSERT INTO Post (user_id, descrip)
VALUES (%s, %s)'''
        print(sql % (session['user_id'],descrip))
        post_id = execute_sql(sql, (session['user_id'],descrip), commit=True, get_lastrowid=True)
        dir_path_photo = "app/static/images/uploads/"
        dir_path_video = "app/static/videos/uploads/"
        photo_names = []
        video_names = []
        
        photo_id, video_id = None, None


        print('\n', list_media)
        print(descrip)
        print(request.files)

        photo_sql = '''
        INSERT INTO Post_Photo (post_id, photo_id, display_order)
        VALUE '''

        video_sql = '''
        INSERT INTO Post_Video (post_id, video_id, display_order)
        VALUE '''
        photo_params = ()
        video_params = ()

        ordering = 0

        delim_photo, delim_video = '', ''
        for media in list_media:
            if photo_allowed_file(media.filename):
                filename = str(uuid.uuid4())
                filepath = dir_path_photo + filename
                media.save(filepath)
                print("saving %s to %s" % (media.filename, filename))

                photo_id = upload_image(filepath)

                photo_sql += delim_photo + "(%s, %s, %s)"
                photo_params += (post_id, photo_id, ordering)
                delim_photo = ',\n'
            elif video_allowed_file(media.filename):
                filename = str(uuid.uuid4())
                filepath = dir_path_video + filename
                media.save(filepath)
                print("saving %s to %s" % (media.filename, filename))

                video_id = upload_video(filepath)

                video_sql += delim_video + "(%s, %s, %s)"
                video_params += (post_id, video_id, ordering)
                delim_video = ',\n'
            else:
                print()
                flash('media not supported')
                ordering -= 1
            ordering += 1
        print(photo_sql, video_sql)
        execute_sql(photo_sql, photo_params, commit=True)
        execute_sql(video_sql, video_params, commit=True)
        return redirect(url_for('post', post_id=post_id))
         
    return render_template('add_post.html')
                
    # get_media
    # store_the_pictures_and_videos
    # display_it
