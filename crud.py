"""CRUD operations."""
# import db and connet class tables here from model.py
# UPDATE class tables HERE --->

from model import db, User, Event, Review, connect_to_db


# This connects to the database when run curd.py interactively 
def create_user(fname, lname, email, password, address, state, zipcode):
    """Create and return a new user."""

    user = User(fname=fname,
                lname=lname,
                email=email, 
                password=password, 
                address=address, 
                state=state, 
                zipcode=zipcode)
    return user


def login_user(email, password):
    """Return user ID if email and password exists."""
    
    current_id = User.query.filter(User.email == email).first()
    
    # Check if password is correct for current_id
    if current_id:
        if current_id.password == password:
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


def get_review_by_userid(user_id):
    """Access all review created by user using it's user_id.""" 

    return Review.query.filter(Review.user_id==user_id).all()

def get_review_by_reviewid(review_id):
    """Access a review created by a user."""
    return Review.query.get(review_id)
# Do I need this function?


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    app.app_context().push()