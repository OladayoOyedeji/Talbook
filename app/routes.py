from app import app

password_valid = True

@app.route('/')
def homepage():
    return '''<html>
<h1>Talbok</h1>
    <a href="/register">
    <button>Register</button>
    </a>
</html>'''

def valid():
    Password = request.args.get('password', '[no password]')
    if Password is valid:
        return 'add_b'
    else:
        return 'register'

@app.route('/register')
def register():
    return """"<html>
<body>
<h1>Registration</h1>
<form action='%s' method='get'>
Lastname: <input type='text' name='lastname'/> 
Firstname: <input type='text' name='firstname'/> <br>
Password: <input type='text' name='password'/> <br>
   
Email: <input type='text' name='email'/> <br>
<input type='submit' value='Go'/>
</form>
</body>
</html>""" % valid()



def process_email(Email):
    


def add_db():
    lastname = request.args.get("lastname", "[No Name]")
    firstname = request.args.get("fullname", "[No Name]")
    Password = request.args.get('password', '[no password]')
    Email = request.args.get('email', 'no email')

    try:
        process_email(Email)
        Hash = hash_password(Password)
    except Exception as e:
        return False
    
    conn = pymsql.connect(user='root', passwrd='root', db='talbook')
    cursor = conn.cursor(pymysql.cursor.DictCursor)

    
    exe = 'insert into Person lastname=%(l)s, firstname=%(f)s, hash=%(h)s, email=%(e)s';
    cursor.execute(exe)
    
    cursor.commit()
    # try:
    #     table = cursor.fetchall()
    #     row = table[len(table)-1]
    #     person_id = row['person_id']

    #     #now i want to add the Email
    #     exe = 'insert into Pa lastname=%(l)s, firstname=%(f)s';

@app.route('/')
def
