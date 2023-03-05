class User:

    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.is_logged_in = False
        self.image = []

    def sign_up(self):
        pass
        # create database and add all info

    def log_in(self):
        pass
        # compare with db and see if log in is successfull, then is_logged in = True

    def recommend_user(self):
        pass
        # add a user

    def add_business(self):
        pass
        # add a business


# class Students(db.Model):
#    id = db.Column('student_id', db.Integer, primary_key = True)
#    name = db.Column(db.String(100))
#    city = db.Column(db.String(50))
#    addr = db.Column(db.String(200))
#    pin = db.Column(db.String(10))
#
#    def __init__(self, name, city, addr,pin):
#        self.name = name
#        self.city = city
#        self.addr = addr
#        self.pin = pin