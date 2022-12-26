from flask import Flask
import os


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # Should be changed to random string when in production
        SECRET_KEY='dev',
        # Tells app were to check for database
        DATABASE=os.path.join(app.instance_path, 'diary.db'),
        TEMPLATES_AUTO_RELOAD=True
    )

    # Ensuring the existence of the instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    if os.path.isfile(os.path.join(app.instance_path, 'diary.sqlite')):
        with app.app_context():
            db.init_db()
    db.init_app(app)

    # Importing blueprints tells the app where to look up for the routes
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')

    return app