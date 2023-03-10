from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, login_manager
from models.user import User,db, setup_db, db_drop_and_create_all, Sister
from forms import RegistrationForm, LoginForm, RecommendSisterForm
from sqlalchemy.exc import IntegrityError
import hashlib
from flaskext.mysql import MySQL
from dotenv import load_dotenv   #for python-dotenv method
load_dotenv()                    #for python-dotenv method
import os




app = Flask(__name__)
setup_db(app)

""" uncomment at the first time running the app. Then comment back so you do not erase db content over and over """
with app.app_context():
    db_drop_and_create_all()




login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('index.html')


@classmethod
def get_by_id(cls, user_id):
    return cls.query.filter_by(id=user_id).first()


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # Sanity check: if the user is already authenticated then go back to home page
    #if current_user.is_authenticated:
     #   return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(display_name=form.username.data).first()
        hashed_input_password = hashlib.md5(form.password.data.encode()).hexdigest()
        if user and user.password == hashed_input_password:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome back {form.username.data}!')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check user name and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(f'You have logged out!', 'success')
    return redirect(url_for('home'))

@app.route("/allSisters")
@login_required
def allSisters():
    sisters = Sister.query.all()
    return render_template('allSisters.html', sisters=sisters)

@app.route('/home', methods=['GET','POST'])
@login_required
def home():
    form = RecommendSisterForm()
    if form.validate_on_submit():
        sister = Sister(
            full_name=form.fullname.data,
            tag_name=form.tag.data,
            contact=form.contact.data,
            address=form.address.data)
        try:
            sister.insert()
            flash(f'we have added your recommendation, thank you!')
            return redirect(url_for('home'))
        # what is this?
        except IntegrityError as e:
            flash(f'Could not register! The entered username or email might be already taken', 'danger')
            print('IntegrityError when trying to store new user')
            # db.session.rollback()

    return render_template('home.html', form=form)



@app.route("/register", methods=['GET', 'POST'])
def register():
    # Sanity check: if the user is already authenticated then go back to home page
    #if current_user.is_authenticated:
     #   return redirect(url_for('home'))

    # Otherwise process the RegistrationForm from request (if it came)
    form = RegistrationForm()
    if form.validate_on_submit():
        # hash user password, create user and store it in database
        hashed_password = hashlib.md5(form.password.data.encode()).hexdigest()
        user = User(
            full_name=form.fullname.data,
            display_name=form.username.data,
            email=form.email.data,
            password=hashed_password)
        try:
            user.insert()
            flash(f'Account created for: {form.username.data}!', 'success')
            return redirect(url_for('home'))
        # what is this?
        except IntegrityError as e:
            flash(f'Could not register! The entered username or email might be already taken', 'danger')
            print('IntegrityError when trying to store new user')
            # db.session.rollback()

    return render_template('registration.html', form=form)

#if __name__ == "__main__":
#app.run(debug=True)
#app.app_context().push()





