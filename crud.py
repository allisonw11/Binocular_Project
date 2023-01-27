"""CRUD operations."""
# import db and connet class tables here from model.py
# UPDATE class tables HERE --->

from model import db, User, connect_to_db


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
    
    # If current_id
    # Check if password is correct for current_id
            # Return user_id
    if current_id:
        if current_id.password == password:
            return current_id.user_id    
    return False


def get_user_by_id(user_id):
    """Access user's info using it's id."""
    
    return User.query.get(user_id)

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    app.app_context().push()