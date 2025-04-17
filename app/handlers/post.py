import os
from flask import request, render_template, flash, redirect, url_for, session, current_app as app
from werkzeug.utils import secure_filename
import json
import uuid
from app.utils.functions import *
from app.utils.User import *
from app.utils import photo
from app.utils import video

def handle_post(post_id):
    # get post informations
    list_of_photo = get_photo_id(post_id)
    list_of_video = get_video_id(post_id)

    list_of_media = list_of_photo + list_of_video

    list_of_media.sort()

    post = get_post_data(post_id)
    post['media'] = list_of_media

    return render_template('post.html', post=post)

    
def handle_add_post():
    # create_a_post_id
    if request.method=='POST':
        list_media = request.files.getlist('media')
        descrip = request.form.get('descrip')

        sql = '''INSERT INTO Post (descrip)
VALUE ('%s')'''

        post_id = execute_sql(sql, (descrip), commit=True, get_lastrowid=True)
        dir_path_photo = "app/static/images/uploads/"
        dir_path_video = "app/static/videos/uploads/"
        photo_names = []
        video_names = []
        
        photo_id, video_id = None, None


        print('\n', list_media)
        print(request.files)

        photo_sql = '''
        INSERT INTO Post_Photo (post_id, photo_id, ordering_order)
        VALUE '''

        video_sql = '''
        INSERT INTO Post_Photo (post_id, photo_id, ordering_order)
        VALUE '''
        photo_params = ()
        video_params = ()

        ordering = 0
        
        for media in list_media:
            if photo.allowed_file(media.filename):
                filename = str(uuid.uuid4())
                filepath = dir_path_photo + filename
                media.save(filepath)
                print("saving %s to %s" % (media.filename, filename))

                photo_id = photo.upload_video(filepath)

                photo_sql += "(%s, %s, %s)"
                photo_params += (post_id, photo_id, ordering)
                
            elif video.allowed_file(media.filename):
                filename = str(uuid.uuid4())
                filepath = dir_path_video + filename
                media.save(filepath)
                print("saving %s to %s" % (media.filename, filename))

                video_id = video.upload_video(filepath)

                video_sql += "(%s, %s, %s)"
                video_params += (post_id, video_id, ordering)

            else:
                print()
                flash('media not supported')
            ordering += 1
        execute_sql(photo_sql, photo_params, commit=True)
        execute_sql(video_sql, video_params, commit=True)
        # return redirect(url_for('post', post_id=post_id))
         
    return render_template('add_post.html')
                
    # get_media
    # store_the_pictures_and_videos
    # display_it
