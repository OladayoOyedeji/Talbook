# File: routes.py
from app import app
from flask import request, render_template, flash, redirect, url_for
import string
from app.functions import *
from app.User import *

user = None

# PASSWORD_RULES = {
#     "min_length": 8,
#     "min_capital_letters": 1,
#     "min_numbers": 2,
#     "min_special_chars": 2
# }

# '''
# # Validation.py
# password_entered = False
# password_valid = True
# valid_length = 8
# no_capital_letters = 1
# no_integers = 2
# no_special_char = 2
# user = None
# '''

# def is_valid_username(username: str) -> bool:
#     usernames = User.get_usernames()
#     return (usernames == None or username not in usernames) 

# def password_errors(password: str) -> list:
#     '''
#     Returns a list of error messages if password does
#     NOT meet complexity requirements.
#     Returns an empty list if the password is valid.
#     '''
    
#     errors = []
    
#     if len(password) < PASSWORD_RULES["min_length"]:
#         errors.append("Password must be at least %s characters long." % PASSWORD_RULES['min_length'])

#     capital_count = 0
#     num_count = 0
#     special_count = 0
#     for c in password:
#         if (c.isupper()):
#             capital_count += 1
#         elif (c.isdigit()):
#             num_count += 1
#         elif (c.isalnum()):
#             special_count += 1

#     if capital_count < PASSWORD_RULES["min_capital_letters"]:
#         errors.append("Password must contain at least %s capital letter(s)." % PASSWORD_RULES['min_capital_letters'])
#     if num_count < PASSWORD_RULES["min_numbers"]:
#         errors.append("Password must contain at least %s number(s)." % PASSWORD_RULES['min_numbers'])
#     if special_count < PASSWORD_RULES["min_special_chars"]:
#         errors.append("Password must contain at least %s special character(s)." % PASSWORD_RULES['min_special_chars'])

#     return errors

# def is_valid_password(password):
#     # return True
#     return (password_errors(password) == [])

# # sends code to specified email. To validate the email,
# # they must input the code
# def is_valid_email(email):
#     return True

## ======================================================== ##
## = these are all the links that will be used in the app = ##
## = the list of all the links would be =================== ##
## ========= homepage ===================================== ##
## ========= signup ======================================= ##
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
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handles user signup."""
    is_valid = {'username': True, 'password': True}  # default values
    invalid_message = {'username': '', 'password': ''}
    
    if (request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        # check for invalid submissions
        # if (not username or not password or not email):
        #     return "ERROR: missing fields"
        # elif (not is_valid_username(username)):
        #     return "ERROR: invalid username"
        #  elif (not is_valid_password(password)):
        #     return "ERROR: password does not meet complexity requirements"
        # elif (not is_valid_email(email)):
        #     return "ERROR: invalid email format"

        # add user to database
        is_valid = {'username': is_valid_username(username),
                    'password': is_valid_password(password)}

        invalid_message = {'username': 'username already used',
                           'password': invalid_message_password()}
        # print(is_valid)
        # sends the verification code
        if is_valid['username'] and is_valid['password'] and email != None:
            send_verification_code()
            return redirect(url_for('email_verification'))
        
    else:
        # if it's a GET request, render the signup form
         return render_template('signup.html', is_valid=is_valid, invalid_message=invalid_message)
    
@app.route('/email_verification')
def email_verification():
    return render_template('email_verification.html', valid_code=is_valid_code)
# is_valid_code function checks the code if its valid and returns the destination

@app.route('/login')
def login():
    
    global user
    
    # is_valid_login = {'user':False, 'password':False}
    invalid_message = ''
    
    if request.method == 'POST':
        user_or_email = request.form.get('user_or_email')
        password = request.form.get('password')

        hash = hash_password(password)

        id = get_user_id(user_or_email)
        print(id)
        is_valid_login = {'user': id != None,
                          'password': valid_hash(id, hash)}
        invalid_message = 'invalid login'
        if valid_login['user'] and valid_login['password']:
            user = User(id)
            return redirect(url_for('home'))
    
    return render_template('login.html', invalid_message=invalid_message)

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
