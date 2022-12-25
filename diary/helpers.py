
from flask import redirect, render_template, flash

def apology(message, code=400):
    # If possible change html template for in-page flash alerts
    # return flash(message=message+''+ str(code),category="error")
    return render_template("error.html", error=code, message=message)
