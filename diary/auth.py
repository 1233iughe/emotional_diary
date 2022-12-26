"""Based on the Flask tutorial https://flask.palletsprojects.com/en/2.2.x/tutorial/views/"""

from flask import Blueprint, render_template, request, redirect, session, url_for, g
from diary.helpers import apology, login_required
from diary.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)
gid = 0


@auth.route("/register", methods=['POST','GET'])
def register():
    """ This function allows users to resgister"""
    # If possible add min lenght restraints for passwords and phrase

    # Checking request method
    if request.method == "POST":
    
        # Cheking contents of the fields of the registration form 
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirm')
        phrase = request.form.get('security')

        # Checking for multiple errors
        if not username:
            return apology("Must input username")
        elif not password:
            return apology("Must input password")
        elif not confirmation:
            return apology("Must retype password")
        elif password != confirmation:
            return apology("Passwords must match")
        elif not phrase:
            return apology("Must select a security phrase")
        else:
            # Checking for duplicate users
            db = get_db()
            user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            if user:
                return apology("user already in existence")
            else:
                # Adding the new user to the data base
                hashp = generate_password_hash(password)
                hashf = generate_password_hash(phrase)
                db.execute("INSERT INTO users(username, hash, security_phrase) VALUES(?,?,?);", (username, hashp, hashf))
                db.commit()

                return redirect(url_for("auth.login"))
    else:
        return render_template("register.html")

@auth.route("/login", methods=['POST','GET'])
def login():
    if request.method == "POST":
        # Gettin username and password from request
        username = request.form.get('username')
        password = request.form.get('password')
        # Setting cursor to database
        db = get_db()

        # Checking the user inputted username and password
        if not username:
            return apology("Must input username")
        elif not request.form.get('password'):
            return apology("Must input password")

        # Looking in data base for the inputted user, if usuccesful it returns None
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        # Checking the user exists
        if user is None:
            return apology("Inexistent user")

        # checking for if the password provided is correct
        elif not check_password_hash(user["hash"], password):
            return apology("Incorrect password")
        
        # Adding the user to the active users dict aka Session
        else:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for("views.index"))
    else:
        return render_template("login.html")

# This route defines a function that checks if a user is log
# before each request and make the info available for other views
# using the g object
@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()


# This rtoute allows the user to recuperate their password if forgotten
# using their security phrase. It handles the identification part.
@auth.route("/recover", methods=['POST','GET'])
def recover():
    if request.method == "POST":
        # Gettin username and password from request
        username = request.form.get('username')
        phrase= request.form.get('phrase')

        # Setting cursor to database
        db = get_db()

         # Checking the user inputted username and password
        if not username:
            return apology("Must input username")
        elif not phrase:
            return apology("Must input phrase")

        # Looking in data base for the inputted user, if usuccesful it returns None
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        # Checking the user exists
        if user is None:
            return apology("Inexistent user")
        
        # checking for if the password provided is correct
        elif not check_password_hash(user["security_phrase"], phrase):
            return apology("Incorrect phrase")
        else:
            global gid
            gid = user["id"]
            return render_template("recover_2.html")    
        
    else:
        return render_template("recover.html")

# Second part of the recover process
@auth.route("/recover_2", methods=['POST','GET'])
def recover_2():
    if request.method == "POST":
        # Gettin username and password from request
        password = request.form.get('password')
        confirmation= request.form.get('confirmation')

        # Setting cursor to database
        db = get_db()

        # Checking the user inputted password and confirmation
        if not password:
            return apology("Must input password")
        elif not confirmation:
            return apology("Must input confirmation")
        else:
            # Updating the database with new password
            global gid
            db.execute("UPDATE users SET hash = ? WHERE id = ?;", (generate_password_hash(password), gid))
            db.commit()
            gid = 0
            return redirect(url_for("auth.login"))
        
    else:
        return render_template("recover.html")

@auth.route("/logout", methods=['POST','GET'])
@login_required
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


# This route allows the user to change their password after logging.
@auth.route("/change_password", methods=['POST','GET'])
@login_required
def change_password():
    if request.method == "POST":
        # Gettin username and password from request
        oldPassword = request.form.get('old_password')
        password = request.form.get('password')
        confirmation= request.form.get('confirmation')

        # Setting cursor to database
        db = get_db()

        # Checking the user inputted password and confirmation
        if not oldPassword:
            return apology("Must input password")
        elif not password:
            return apology("Must input new password")
        elif not confirmation:
            return apology("Must input confirmation")
        else:
            user_id = session.get("user_id")
            user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            if check_password_hash(user['hash'],oldPassword):
                # Updating the database with new password
                
                db.execute("UPDATE users SET hash = ? WHERE id = ?;", (generate_password_hash(password), user_id))
                db.commit()
                return redirect(url_for("views.index"))
            else:
                return apology("Incorrect password")
        
    else:
        return render_template("change_password.html")
    
