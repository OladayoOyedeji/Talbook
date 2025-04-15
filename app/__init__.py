#File: __init__.py
from flask import Flask
import os
from app.utils import mysql_util
import logging
from datetime import datetime

app = Flask(__name__, static_folder="static")
# the secret key shouldn't be hardcoded
app.secret_key = r'''
b'R}j\x8a\x94\x99V">TM\xf79\x18\x8bu\x80\xb9\xba\x07\x90\x87\xb7\x88\x8f\xcaj\xbc}\xbd\x07\xeb1/\x0fw_\xef\x1e\x93\xbd\xfc\xf0\xd3D\\\xd4\x11\xa6\xe1\xb2\n\x8d\x1f\x16\x92\x13\x8cl\x1a;\xfe\xd8\x18sF\xaaU\x8e\xb3\xa5p8\x88\xf1~+\r\xd8\xea\xe8\xde\xa5\x94O\xbc\x03\x03[\xfa\xf4\xf0\\U\x02>\x02\x91Xf\xd0aHYD\x80/\xf6\xe3\xf1E\xcd\xa9\x88\x9d\x194\xd4\x1fM\xa3\xe6\x7fc8\xad\xd3\xeaH2m\xd8\xa4\xdc\xbe\x1e\x06\x98\xe2\nl\xe1\xce\xab\xa3\xe6d\x97\xfb\xa6\xce\x0e\xc0\x84\x19q\xb3A9\\\xb7=\xf67\x93\x1a\th\xd6\xa7\x82d\x7fR\x9e7\x91\x14\xf4\x8dC\x94\xa3g\xce\xb8\x97\xfb:\xe98\xc3\x11\xaa9\xf3\xb8\xd0\xd9\x96\x10\xc7\xdb\xa6\x9e.K\x12\n1F;\x9b\x92_L\x8e$/S\x0b\xe7\r\x01\x9c\x06v\x0c\x86\xb7*\xd64\xf7n\xa6\xe6\xb3\x16V'
''' # os.urandom(240)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


# configure logging to show DEBUG messages
app.logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

# log to a file for debugging
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)

# ensure the database is set up
mysql_util.ensure_database()

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%B %d, %Y at %I:%M %p'):
    return datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S').strftime(format)

from app import routes
