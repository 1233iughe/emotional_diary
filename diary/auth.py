"""Based on the Flask tutorial https://flask.palletsprojects.com/en/2.2.x/tutorial/views/"""

from flask import Blueprint, render_template, request, redirect, flash
from diary.helpers import apology
from diary.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

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
        if not username:
            return apology("Must input username", 400)
        elif not password:
            return apology("Must input password", 400)
        elif not confirmation:
            return apology("Must retype password", 400)
        elif password != confirmation:
            return apology("Passwords must match", 400)
        elif not phrase:
            return apology("Must select a security phrase", 400)
        else:
            db = get_db()
            if db.execute("SELECT username FROM users WHERE username = ?", (username,)):
                return apology("user already in existence", 400)
            else:
                hashp = generate_password_hash(password)
                hashf = generate_password_hash(phrase)
                db.execute("INSERT INTO users(username, hash, security_phrase) VALUES(?,?,?);", (username, hashp, hashf))
                db.commit()

                return redirect("/auth/login")
    else:
        return render_template("register.html")

@auth.route("/login", methods=['POST','GET'])
def login():
    return render_template("login.html")

@auth.route("/logout", methods=['POST','GET'])
def logout():
    return render_template("login.html")

@auth.route("/change_password", methods=['POST','GET'])
def change_password():
    return render_template("change_password.html")
