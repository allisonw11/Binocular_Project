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
    zipcode = db.Column(db.String, nullable=False)
    
    
    reviews = db.relationship("Review", back_populates="user")

    # function that auto return needed info when called
    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"
        
        
        
class Event(db.Model):
    """An event."""
    __tablename__ = "events"
    
    event_id = db.Column(db.String, primary_key=True)
    event_title = db.Column(db.String, nullable=False)
    event_genre = db.Column(db.String, nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    event_zipcode = db.Column(db.Integer, nullable=False)
    event_lat = db.Column(db.Float, nullable=False)
    event_lng = db.Column(db.Float, nullable=False)
    
    reviews = db.relationship("Review", back_populates="event")
    
    def __repr__(self):
        return f"<User event_id={self.event_id}>"
    
    
    
class Review(db.Model):
    """An review."""
    __tablename__ = "reviews"
    
    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rating_score = db.Column(db.Integer, nullable=False)
    review_title = db.Column(db.String(50), nullable=False)
    review_description = db.Column(db.Text, nullable=False)
    review_recommend = db.Column(db.Boolean, nullable=False)
    review_date = db.Column(db.DateTime, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    event_id = db.Column(db.String, db.ForeignKey("events.event_id"), nullable=False)
    
    user = db.relationship("User", back_populates="reviews")
    event = db.relationship("Event", back_populates="reviews") 

    def __repr__(self):
        return f"<Review review_id={self.review_id} rating={self.rating_score}>"



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
