from . import db
from datetime import datetime

def timeinfo():
    return datetime.today().strftime("%a %d %b %Y") # date and time representation

# Holdover from lab 5 for the login system
# Not really needed for this project but kept
# just for feature completeness
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)



# Project1 DB Model 
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    username = db.Column(db.String(80))
    age = db.Column(db.Integer)
    bio = db.Column(db.String(140))
    image = db.Column(db.String(255))
    datecreated = db.Column(db.DateTime)
    gender = db.Column(db.String(10))
    

    def __init__(self, fName, lName, username, age, bio, image, gender):
        self.fname = fName
        self.lname = lName
        self.username = username
        self.age = age
        self.bio = bio
        self.image = image
        self.gender = gender
        self.datecreated = timeinfo()