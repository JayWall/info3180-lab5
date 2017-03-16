"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm
from werkzeug.utils import secure_filename
from models import UserProfileNew, UserProfile
import os
import datetime


###
# Routing for your application.
###


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    # If the user is already logged in then it will just return them to the 
    # secure page instead of logging them in again
    if (current_user.is_authenticated):
        return redirect(url_for('secure_page'))
    
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        # change this to actually validate the entire form submission
        # and not just one field
        if form.username.data and form.password.data:
            # Get the username and password values from the form.
            username = form.username.data
            password = form.password.data
            # using your model, query database for a user based on the username
            # and password submitted
            # store the result of that query to a `user` variable so it can be
            # passed to the login_user() method.
            user = UserProfile.query.filter_by(username=username, password=password).first()
            # get user id, load into session
            if user is not None:
                login_user(user)
                flash('Successful login :)', 'success')
                next = request.args.get('next')
                return redirect(url_for('secure_page'))
            else:
                flash('Login information correct. Check again :(', 'danger')
                
    return render_template("login.html", form=form)

@app.route("/secure-page")
@login_required
def secure_page():
    return render_template('securepage.html', uploads=get_uploads())
    
@app.route('/profile', methods=["POST"])
def newfile():
    thefilefolder = app.config['UPLOAD_FOLDER']
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(thefilefolder, filename))
    
    NewProfile = UserProfileNew(request.form['fName'], request.form['lName'],
                                request.form['userName'],request.form['age'], 
                                request.form['bio'], filename, request.form['gender'])
                                
    db.session.add(NewProfile)
    db.session.commit()
    
    User = UserProfileNew.query.filter_by(username=request.form['userName']).first
    
    flash('Profile saved :)')
    return redirect(url_for('profile',userid=User.id))

@app.route('/profile', methods=["GET"])
def profile():
    return render_template('signup.html')
    
@app.route('/profiles', methods=["GET"])
def profiles():
    profiles = UserProfileNew.query.filter_by().all()
    return render_template('profiles.html', profiles=profiles)
    
@app.route('/profile/<userid>', methods=['GET'])
def idprofile(userid):
    User = UserProfileNew.query.filter_by(id=userid).first
    return render_template('profile.html', profile=User)


    
#@app.route('/postdata', methods=['GET', 'POST'])
#def postdata():
#    if request.method == "POST":
#        theuserform()
#    return render_template('profile.html')
    
#def theuserform():
    firstname= '' 
    lastname=''
    username=firstname+ '_' +lastname
    age= 0
    bio=''
    file=''
    gender=''
    firstname=request.form['FirstName']
    lastname=request.form['LastName']
    username=request.form['UserName']
    age=request.form['Age']
    bio=request.form['Bio']
    file=request.form['file']
    gender=request.form['gender']
    return (firstname, lastname, username, age, bio, file, gender)    
        

@app.route('/profiles', methods=['POST'])
def profilesJSON():
    profile_list = []    
    profiles = UserProfileNew.query.filter_by().all()

    for profile in profiles:
        profile_list +=[{'username':profile.username, 'userID':profile.id}]
    return jsonify(users=profile_list)

@app.route('/profile/<userid>', methods=['POST'])
def profileIDJSON(userid):
    profile = UserProfileNew.query.filter_by(id=userid).first()
    if profile is not None:
        profile_list ={'userid':profile.id, 'username':profile.username, 
                        'image':profile.image, 'gender':profile.gender, 
                        'age':profile.age, 'profile_created_on':profile.datecreated
                        }
    else:
        profile_list = {}
    return jsonify(profile_list)    

def get_uploads():
    uploads = []
    for subdir, dirs, files in os.walk(app.config['UPLOAD_FOLDER']):
        for file in files:
            if not file.startswith('.'): #ignores hidden files on linux
                uploads.append(file)
    return uploads

@app.route('/filelisting', methods=['POST', 'GET'])
def test():
    if not session.get('logged_in'):
        abort(401)
        
    return render_template('uploads.html', uploads=get_uploads())

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%d %b %Y'):
    return value.strftime(format)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
    


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")