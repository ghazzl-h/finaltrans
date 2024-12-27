from flask import Flask, render_template,request,redirect,session
import psycopg2
from jinja2.compiler import find_undeclared
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = 'your_secret_key'

database_connection_session = (psycopg2.connect
    (
    host="ep-silent-sound-a5udo5gz.us-east-2.aws.neon.tech",
    database="FinalTrans",
    user="FinalTrans_owner",
    password="efmUkJg41rxS",
    port=5432
))



@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'\

@app.route('/handle_button_click',methods=['POST','GET'])
def handle_button_click():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        age=request.form.get('age')
        cur=database_connection_session.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM baby WHERE age=%s',(age,))
        bdata=cur.fetchone()

        cur.close()

        if bdata and bdata['age']== 'Newborn':
            return redirect('/0-3_months')
        elif bdata and bdata['age']=='infant':
            return redirect('/3-12_months')
        elif bdata and bdata['age']=='toddlers':
            return redirect('/1-3_years')
        else:
            return 'Age not found',404

@app.route('/0-3_months',methods=['POST','GET'])
def zero_to_three_months():
       return "you selected 0-3  months page"
@app.route('/3-12_months',methods=['POST','GET'])
def three_to_twelve_months_page():
       return "you selected 3-12 months page"
@app.route('/1-3_years',methods=['POST','GET'])
def one_to_three_years():
       return "you selected 1-3 years page"








@app.route('/index')
def index():
   return render_template('index.html')


if __name__ == '__main__':
    app.run()
