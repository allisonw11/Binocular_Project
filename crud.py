"""CRUD operations."""
# import db and connet class tables here from model.py

from model import db, User, Event, Review, connect_to_db
from werkzeug.security import generate_password_hash, check_password_hash

# This connects to the database when run curd.py interactively 
def create_user(fname, lname, email, password, address, state, zipcode):
    """Create and return a new user."""

    user = User(fname=fname,
                lname=lname,
                email=email, 
                password=generate_password_hash(password, method="sha256"), 
                address=address, 
                state=state, 
                zipcode=zipcode)
    return user


def login_user(email, password):
    """Return user ID if email and password exists."""
    
    current_id = User.query.filter(User.email == email).first()
    
    # Check if password is correct for current_id after verify email is correct
    if current_id:
        if check_password_hash(current_id.password, password):
        # if current_id.password == password:
            return current_id.user_id    
    return False


def get_user_by_id(user_id):
    """Access user's info using it's id."""
    
    return User.query.get(user_id)


def create_event(event_id, event_title, event_genre, event_date, event_zipcode, event_lat, event_lng):
    """Create and return an event."""
    event = Event(event_id=event_id,
                  event_title=event_title,
                  event_genre=event_genre, 
                  event_date=event_date, 
                  event_zipcode=event_zipcode,
                  event_lat=event_lat,
                  event_lng=event_lng)
    return event


def get_event_by_id(event_id):
    """Return event_id from event."""
    return Event.query.get(event_id)


def create_review(user_id, event_id, rating_score, review_title, review_description,review_recommend, review_date):
    """Create and return a new review."""
    review = Review(user_id=user_id,
                    event_id=event_id,
                    rating_score=rating_score, 
                    review_title=review_title, 
                    review_description=review_description,
                    review_recommend=review_recommend, 
                    review_date=review_date)
    return review


def updated_review(user_id, event_id, rating_score, review_title, review_description,review_recommend):
    """Update an existed review."""
    updated_review = Review.query.filter(Review.event_id==event_id, Review.user_id==user_id).first()
    updated_review.rating_score=rating_score
    updated_review.review_title=review_title
    updated_review.review_description=review_description
    updated_review.review_recommend=review_recommend
    return updated_review
    
    
def get_review_by_userid(user_id):
    """Access all reviews created by user using it's user_id.""" 

    return Review.query.filter(Review.user_id==user_id).all()


def get_review_by_eventid(event_id):
    """Access all reviews under an event id."""
    
    return Review.query.filter(Review.event_id==event_id).all()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    app.app_context().push()