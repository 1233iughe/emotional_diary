# Allows to store views (routes) without needing to now the complete final scope of the app
from flask import Blueprint, render_template, request, session, url_for
from diary.db import get_db
from diary.helpers import apology, login_required

views = Blueprint('views', __name__)

@views.route("/", methods=['POST','GET'])
@login_required
def index():
    # TODO: show calendar and allow to the user to click on individual days
    return render_template("home.html")

@views.route("/manage_emotions", methods=['POST','GET'])
@login_required
def manage_emotions():
    # TODO: Allow user to create a list of emotion-color pairs
    # Initialize database connections and get user id
    db = get_db()
    user_id = session.get('user_id')

    # Check request method
    if request.method == "POST":
        # Get color and emotion
        color = request.form.get('emotion_color')
        emotion = request.form.get('emotion')

        #Avoid error in case of invalid input in to int(value,16)
        try:
            # Checking the user inputted a color 
            if not color:
                return apology("Must input a color")
            # Checking user inputted an emotion, all emotions are valid. We don't judge you.
            elif not emotion:
                return apology("Must input an emotion")
             # Checking the user inputted a valid color 
            elif color[0:2] != '0x' or len(color) < 3:
                return apology("COLOR MUST BE A HEX")
            elif int(color,16) > 0xffffff:
                return apology("Number must be less than 0xffffff")
            else:
                
                # Checking if user has already registere some emotions/colors
                settings = db.execute("SELECT * FROM settings WHERE user_id = ?",(user_id,)).fetchall()
                if not settings:
                    # Inserting values and updating table
                    db.execute("INSERT INTO settings(user_id, color, emotion) VALUES(?,?,?)", (user_id, color, emotion))
                    db.commit()
                    settings = db.execute("SELECT * FROM settings WHERE user_id = ?",(user_id,)).fetchall()
                    return render_template("manage_emotions.html", settings=settings)
                else:
                    # Inserting values and updating table
                    for dict in settings:
                        if dict["emotion"] == emotion:
                            db.execute("UPDATE settings SET color = ? WHERE user_id = ? AND emotion = ?", (color, user_id, emotion))
                            db.commit()
                            settings = db.execute("SELECT * FROM settings WHERE user_id = ?",(user_id,)).fetchall()
                            return render_template("manage_emotions.html", settings=settings)
                    
                    db.execute("INSERT INTO settings(user_id, color, emotion) VALUES(?,?,?)", (user_id, color, emotion))
                    db.commit()
                    settings = db.execute("SELECT * FROM settings WHERE user_id = ?",(user_id,)).fetchall()
                    return render_template("manage_emotions.html", settings=settings)

        except TypeError:
            return apology("COLOR MUST BE A HEX")

    else:
        settings = db.execute("SELECT * FROM settings WHERE user_id = ?",(user_id,)).fetchall()
        if not settings:
            return render_template("manage_emotions.html")
        else:
            return render_template("manage_emotions.html", settings=settings)


@views.route("/delete_emotion", methods=['POST'])
@login_required
def delete_emotion():
    emotion = request.form.get('emotion_button')
    user_id = session.get('user_id')
    db = get_db()
    db.execute("DELETE FROM settings WHERE user_id = ? AND emotion = ?", (user_id, emotion))
    db.commit()
    settings = db.execute("SELECT * FROM settings WHERE user_id = ?",(user_id,)).fetchall()
    if not settings:
        return render_template("manage_emotions.html")
    else:
        return render_template("manage_emotions.html", settings=settings)
        