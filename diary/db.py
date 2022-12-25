"""Taken from flask tutorial https://flask.palletsprojects.com/en/2.2.x/tutorial/database/ 
comments by the author"""
import sqlite3

import click
from flask import current_app, g

# Creates a connection with the database and sets that each row is returned as a dict
# so columns can be access by name.
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


# Closing the conection with the data base
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Construction of the database
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def init_app(app):
    app.teardown_appcontext(close_db)
    