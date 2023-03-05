from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
login_manager = LoginManager()



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)






@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student = Students(request.form['name'], request.form['city'], request.form['addr'], request.form['pin'])
        # Inserts records into a mapping table
        db.session.add(student)
        db.session.commit()
    return render_template('new.html')



@app.route('/showStudents/<city>')
@app.route('/showStudents/')
def show_students(city=None):
    if city:
        students_list = Students.query.filter_by(city=city).all()
    else:
        students_list = Students.query.all()
    return render_template('show_all.html', students=students_list)



@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('index.html', error=error)

@app.route('/home', methods=['GET','POST'])
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.app_context().push()
    db.reflect()
    db.drop_all()


