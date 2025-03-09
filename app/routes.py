from app import app
from flask import request

password_entered = False
password_valid = True
valid_length = 8
no_capital_letters = 1
no_integers = 2
no_special_char = 2

## ======================================================== ##
## = functions used for the class ========================= ##
## ======================================================== ##
def get_shopping_cart():
    '''
    
    '''

## ======================================================== ##
## = Created a User class to make it easier to navigate and ##
## = use the database ===================================== ##
## ======================================================== ##
class User:
    def __init__(self, id):
        self.id = id
        self.listing = get_listing(self.id)
        self.preferences = get_preferences(self.id)
        self.transaction_history = get_transaction_history(self.id)
        self.friends_list = get_friends_list(self.id)
        self.photo_directory = get_photo_directory(self.id)

    def add_user_db():
        k
    def 

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
                                                   '''
                                                   the comments might be awful
                                                   '''
@app.route('/')
def homepage():
    return '''<html>
<h1>Talbok</h1>
    <a href="/signin">
    <button>Signin</button>
    </a>
    <a href="/login">
    <button>Loginr</button>
    </a>
</html>'''
    
@app.route('/signin')
def register():
    return """<html>
<body>
<h1>Registration</h1>
<form action='%(action)s' method='get'><br>
Lastname: <input type='text' name='lastname'/> <br>
Firstname: <input type='text' name='firstname'/> <br>
Password: <input type='text' name='password'/> <br>
%(verified_message)s
<h3>Email: <input type='text' name='email'/></h3> <br>
<input type='submit' value='Go'/>
</form>
</body>
</html>""" % {'action':valid(), 'verified_message':ver_message()}

@app.route('/home')
def home():
    return """<html>
    <h2>you have made it to the homepage<\h2>
</html>"""

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
