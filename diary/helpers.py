
from flask import redirect, render_template, flash, g, url_for 
import functools

# Renders and apology with a especified message and code
def apology(message, code=400):
    # If possible change html template for in-page flash alerts
    # return flash(message=message+''+ str(code),category="error")
    return render_template("error.html", error=code, message=message)

# Decorator that ensures the user is logged
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view