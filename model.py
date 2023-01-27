"""Models for events locating app."""
"""All data tables located + import into crud.py"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    
    # create relationship here, if any--->


    # function that auto return needed info when called
    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"
        
# # ENTER MORE CLASS HERE ----->

def connect_to_db(flask_app, db_uri="postgresql:///eventsLocator", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = False
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)
    
    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    app.app_context().push()
