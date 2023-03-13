from flask import Flask, render_template, redirect, url_for, request, flash, abort, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, login_manager
from flask_cors import CORS
import traceback
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
CORS(app)



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
#
# @app.route("/allSisters")
# @login_required
# def allSisters():
#     sisters = Sister.query.all()
#     return render_template('allSisters.html', sisters=sisters)

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

# @app.route('/home/findASister', methods=['GET'])
# @login_required()
# def findASister():
#     return render_template(
#         'map.html',
#         map_key='AAPK7d6d9e7a9b0f49fa8359acf88e28abb9xTZSEGYp1_BO4piSTbtYVRCJ8w-LLbKXrBndhNhJZWpzoBEK6O9RqV4Tmk65yBtZ'
#     )


# @app.route('/detail', methods=['GET'])
# def detail():
#     location_id = float(request.args.get('id'))
#     item = SampleLocation.query.get(location_id)
#     return render_template(
#         'detail.html',
#         item=item,
#         map_key='AAPK7d6d9e7a9b0f49fa8359acf88e28abb9xTZSEGYp1_BO4piSTbtYVRCJ8w-LLbKXrBndhNhJZWpzoBEK6O9RqV4Tmk65yBtZ'
#     )


# @app.route("/home/recommendASister", methods=['GET', 'POST'])
# @login_required()
# def new_location():
#     form = NewLocationForm()
#
#     if form.validate_on_submit():
#         latitude = float(form.coord_latitude.data)
#         longitude = float(form.coord_longitude.data)
#         description = form.description.data
#
#         location = SampleLocation(
#             description=description,
#             geom=SampleLocation.point_representation(latitude=latitude, longitude=longitude)
#         )
#         location.insert()
#
#         flash(f'New location created!', 'success')
#         return redirect(url_for('home'))
#
#     return render_template(
#         'new-location.html',
#         form=form,
#         map_key=os.getenv('MAPS_API_KEY', 'MAPS_API_KEY_WAS_NOT_SET?!')
#     )
#
#
# @app.route("/api/store_item")
# def store_item():
#     try:
#         latitude = float(request.args.get('lat'))
#         longitude = float(request.args.get('lng'))
#         description = request.args.get('description')
#
#         location = SampleLocation(
#             description=description,
#             geom=SampleLocation.point_representation(latitude=latitude, longitude=longitude)
#         )
#         location.insert()
#
#         return jsonify(
#             {
#                 "success": True,
#                 "location": location.to_dict()
#             }
#         ), 200
#     except:
#         exc_type, exc_value, exc_traceback = sys.exc_info()
#         app.logger.error(traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2))
#         abort(500)
#
#
# @app.route("/api/get_items_in_radius")
# def get_items_in_radius():
#     try:
#         latitude = float(request.args.get('lat'))
#         longitude = float(request.args.get('lng'))
#         radius = int(request.args.get('radius'))
#
#         locations = SampleLocation.get_items_within_radius(latitude, longitude, radius)
#         return jsonify(
#             {
#                 "success": True,
#                 "results": locations
#             }
#         ), 200
#     except:
#         exc_type, exc_value, exc_traceback = sys.exc_info()
#         app.logger.error(traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2))
#         abort(500)
#
#
# @app.errorhandler(500)
# def server_error(error):
#     return jsonify({
#         "success": False,
#         "error": 500,
#         "message": "server error"
#     }), 500
#
# #return app


#if __name__ == "__main__":
#app.run(debug=True)
#app.app_context().push()





