from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#from models.user import User
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime



login_manager = LoginManager()


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SECRET_KEY'] = "DxoTNR5WqA4MmgYk"

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)  # i.e Hanna Barbera
    display_name = db.Column(db.String(20), unique=True, nullable=False)  # i.e hanna_25
    email = db.Column(db.String(120), unique=True, nullable=False)  # i.e hanna@hanna-barbera.com
    password = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_authenticated = db.Column(db.Boolean, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    is_anonymus = db.Column(db.Boolean, nullable=False)



    @classmethod
    def get_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    def __repr__(self):
        return f"User({self.id}, '{self.display_name}', '{self.email}')"

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()




@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)



# @app.route('/add', methods=['GET', 'POST'])
# def add_student():
#     if request.method == 'POST':
#         student = Students(request.form['name'], request.form['city'], request.form['addr'], request.form['pin'])
#         # Inserts records into a mapping table
#         db.session.add(student)
#         db.session.commit()
#     return render_template('new.html')
#
#
#
# @app.route('/showStudents/<city>')
# @app.route('/showStudents/')
# def show_students(city=None):
#     if city:
#         students_list = Students.query.filter_by(city=city).all()
#     else:
#         students_list = Students.query.all()
#     return render_template('show_all.html', students=students_list)



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
    db.create_all()


