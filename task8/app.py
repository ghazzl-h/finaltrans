import os
import uuid
from flask import Flask, render_template, request, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')  # Use environment variable for production

# Database connection setup
try:
    database_connection_session = psycopg2.connect(
        host="ep-silent-sound-a5udo5gz.us-east-2.aws.neon.tech",
        database="FinalTrans",
        user="FinalTrans_owner",
        password="efmUkJg41rxS",
        port=5432
    )
    print("Database connection established successfully!")
except Exception as e:
    print(f"Database connection failed: {e}")

# Routes
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = None
    baby_data = None  # Store baby information after signup

    if request.method == 'GET':
        return render_template('signup.html')

    elif request.method == 'POST':

            # Collect form data
            fname = request.form.get('firstname')
            lname = request.form.get('lastname')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            age = request.form.get('age')
            baby_gender = request.form.get('baby_gender')
            contact = request.form.get('contact')
            address = request.form.get('address')
            parent1 = request.form.get('parent1')
            parent2 = request.form.get('parent2')



            if password != confirm_password:
                message = 'Passwords do not match!'
                return render_template('signup.html', msg=message)



            # Perform database operations
            with database_connection_session.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                # Check if baby (user) exists
                cur.execute('SELECT * FROM baby WHERE email = %s', (email,))
                if cur.fetchone():
                    message = "User already exists!"
                else:
                    # Insert new baby into the database
                    cur.execute(
                        '''
                        INSERT INTO baby (fname, lname, email, password, age, baby_gender, contact, address, parent1, parent2)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                        ''',
                        (fname, lname, email, password, age, baby_gender, contact, address, parent1, parent2)
                    )
                    database_connection_session.commit()
                    new_baby_id = cur.fetchone()['id']

                    # Fetch the newly created baby's data
                    cur.execute(
                        '''
                        SELECT fname, lname, email, age, baby_gender, contact, address, parent1, parent2
                        FROM baby
                        WHERE id = %s
                        ''',
                        (new_baby_id,)
                    )
                    baby_data = cur.fetchone()
                    message = "Baby record created successfully!"



    return render_template('signup.html', msg=message, baby_data=baby_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Secure the query to avoid SQL injection
        with database_connection_session.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute('SELECT * FROM baby WHERE email=%s AND password=%s', (email, password))
            userdata = cur.fetchone()

            if userdata:
                # Save user data to the session
                session['user'] = dict(userdata)


                # Redirect to the patient dashboard or home
                return redirect('/index')
            else:
                # If user data is not found, the email or password is incorrect
                message = 'Invalid email or password'
                return render_template('login.html', message=message)

@app.route('/index')
def index():
    return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
