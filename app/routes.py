from app import app
from flask import request
# from constants import *

# Validation.py
password_entered = False
password_valid = True
valid_length = 8
no_capital_letters = 1
no_integers = 2
no_special_char = 2
user = None

def valid_check(Password):
    global password_valid
    global valid_length
    global no_capital_letters
    global no_integers
    global no_special_char
    global password_entered
    
    # print("password_entered", )
    if not password_entered:
        return False
    
    password_valid = False
    
    if len(Password) < valid_length:
        return False;
    count_cl = 0
    count_int = 0
    count_sp_c = 0
    for c in Password:
        if ord(c) >= ord('A') and ord(c) <= ord('Z'):
            count_cl += 1
        elif ord(c) >= ord('0') and ord(c) <= ord('9'):
            count_int += 1
        elif ord(c) < ord('a') or ord(c) > ord('z'):
            count_sp_c += 1
    valid = count_cl >= no_capital_letters and \
    count_int >= no_integers and count_sp_c >= no_special_char

    print("password_valid?:", valid)
    password_valid = valid
        
    return valid

def valid():
    global password_entered
    Password = request.args.get('password', '[no password]')
    if valid_check(Password):
        print("password valid go home")
        return 'home'
    else:
        print('true')
        password_entered = True
        return 'signin'

def ver_message():
    global password_valid
    global valid_length
    global no_capital_letters
    global no_integers
    global no_special_char
    if password_valid:
        return ''
    else:
        return '<span style = "color: red; font-size: 10px">\
        password has to be a minimum of %(i)s characters \
        containing %(j)s capital letters, %(k)s integers, %(l)s \
        special characters<br>\n <span style = "color: black">'\
        %{'i':valid_length, 'j':no_capital_letters,
                              'k':no_integers, 'l':no_special_char}

# end of validation


## ======================================================== ##
## = these are all the links that will be used in the app = ##
## = the list of all the links would be =================== ##
## ========= homepage ===================================== ##
## ========= sign in ====================================== ##
## ========= login ======================================== ##
## ========= profile ====================================== ##
## ========= explore ====================================== ##
## ========= inbox ======================================== ##
## ========= cart ========================================= ##
## ========= setting ====================================== ##
## ========= purchases ==================================== ##
## ========= saved ======================================== ##
## ========= sell an item ================================= ##
## ========= more links later ============================= ##
## ======================================================== ##

@app.route('/')
def base():
    return '''<html>
<h1>Talbook</h1>
    <a href="/signup">
    <button>Signup</button>
    </a>
    <a href="/login">
    <button>Login</button>
    </a>
</html>'''
    
@app.route('/signup')
def signup():
    is_valid = {'username': valid_username(),
                'password': valid_password()}

    invalid_message = {'username': 'username already used',
                       'password': inv_message_password()}
    
    return render_template('signup.html', is_valid=is_valid, invalid_message=invalid_message)
# is_valid_signup function checks if the password is valid and the username is valid and returns the destination
# is_Valid_password function checks the password if its valid return nothing but if not valid returns a message
# like wise for is_valid_username

@app.route('/email_verification')
def email_verification():
    return '''
<form action='%s' method='get'><br>
<input type='text' name='code'/>
    ''' % is_valid_code()
# is_valid_code function checks the code if its valid and returns the destination

@app.route('/login')
def login():
    is_valid_login = is_valid_login()
    return render_template('login.html', is_valid_login=is_valid_login)

@app.route('/home')
def home():
    global user
    if user==None:
        # get id from username and put it into the User object
        user = User(id)
    return render_template('homepage.html', user=user)

# @app.route('/')
# def homepage():
#     return '''<html>
# <h1>Talbook</h1>
#     <a href="/signup">
#     <button>Signup</button>
#     </a>
#     <a href="/login">
#     <button>Login</button>
#     </a>
# </html>'''
    
# @app.route('/signup')
# def register():
#     return """<html>
# <body>
# <h1>Registration</h1>
# <form action='%(action)s' method='get'><br>
# Username: <input type='text' name='username'/> <br>
# %(valid_username)s
# Password: <input type='text' name='password'/> <br>
# %(valid_password)s
# <h3>Email: <input type='text' name='email'/></h3> <br>
# <input type='submit' value='Go'/>
# </form>
# </body>
# </html>""" % {'action':is_valid_signup(), 'valid_password': is_valid_password(), 'valid_username':is_valid_username()}
# # is_valid_signup function checks if the password is valid and the username is valid and returns the destination
# # is_Valid_password function checks the password if its valid return nothing but if not valid returns a message
# # like wise for is_valid_username

# @app.route('/email_verification')
# def email_verification():
#     return '''
# <form action='%s' method='get'><br>
# <input type='text' name='code'/>
#     ''' % is_valid_code()
# # is_valid_code function checks the code if its valid and returns the destination

# @app.route('/login')
# def login():
#     return """<html>
# <body>
# <h1>Registration</h1>
# <form action='%(action)s' method='get'><br>
# Lastname: <input type='text' name='lastname'/> <br>
# Firstname: <input type='text' name='firstname'/> <br>
# Password: <input type='text' name='password'/> <br>
# %(verified_message)s
# <h3>Email: <input type='text' name='email'/></h3> <br>
# <input type='submit' value='Go'/>
# </form>
# </body>
# </html>""" % {'action':valid(), 'verified_message':ver_message()}


# @app.route('/home')
# def home():
#     global user
#     return """<html>
#     <h2>%s's homepage</h2>
# </html>""" % user.username

# def process_email(Email):
    


# def add_db():
#     lastname = request.args.get("lastname", "[No Name]")
#     firstname = request.args.get("fullname", "[No Name]")
#     Password = request.args.get('password', '[no password]')
#     Email = request.args.get('email', 'no email')

#     try:
#         process_email(Email)
#         Hash = hash_password(Password)
#     except Exception as e:
#         return False
    
#     conn = pymsql.connect(user='root', passwrd='root', db='talbook')
#     cursor = conn.cursor(pymysql.cursor.DictCursor)

    
#     exe = 'insert into Person lastname=%(l)s, firstname=%(f)s, hash=%(h)s, email=%(e)s';
#     cursor.execute(exe)
    
#     cursor.commit()
#     # try:
#     #     table = cursor.fetchall()
#     #     row = table[len(table)-1]
#     #     person_id = row['person_id']

#     #     #now i want to add the Email
#     #     exe = 'insert into Pa lastname=%(l)s, firstname=%(f)s';

# @app.route('/')
# def
