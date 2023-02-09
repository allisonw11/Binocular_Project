"""Server for event look-up app"""
from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db
from pprint import pformat
from jinja2 import StrictUndefined
import requests
import crud
import os
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
TICKETMASTER_KEY = os.environ["TICKETMASTER_KEY"]
API_KEY = os.environ["GMAP_KEY"]

@app.route("/")
def homepage():
    """View Homepage."""
    
    return render_template("homepage.html")



@app.route("/", methods=["POST"])
def log_in():
    """Log-in a user."""
    # Handle POST form submission of the login at homepage
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.login_user(email, password)
    print(user)
    if user:
        session["user"] = user
        flash("You are successfully logged in.")
    else:
        flash("Error! Please create a new account.")
    return redirect("/")



@app.route("/logout", methods=["POST"])
def log_out():
    """Log-out a user."""
    session.clear()
    return redirect("/")
    

    
@app.route("/new_account")
def create_account():
    """View create account page."""

    return render_template("new_account.html")



@app.route("/new_account", methods=["POST"])
def creat_new_user():
    """Create a new user."""
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")
    address = request.form.get("address")
    state = request.form.get("states")
    zipcode = request.form.get("zipcode")
    
    # Add conditionals here when want flashing msg display at top of new_account.html page
    if len(email)<6:
        # Make sure each email is unique with NO DUPLICATION!!!
        flash("Email is not a valid address.")
        
    elif len(fname)<2:
        pass
    else:
        # add user.crud...
        # add db.session.add(user here!)
        # add db.session.commit()
        # flash msg "create new account"
        pass
        
    user = crud.create_user(fname,lname,email,password,address,state,zipcode)
    
    db.session.add(user)
    db.session.commit()
    
    if user:
        flash("You have created a new account.")
        return redirect("/user_profile", user=user)
    else:
        flash("Something is missing. Try again!")
        # flash msg should based on the missing info/conditionals from above
        return render_template("new_account.html")



@app.route("/user_profile")
def user_profile():
    """View indivdual user's profile."""
    
    user = crud.get_user_by_id(session["user"])
    
    if "user" in session:
        flash("Loggin Successfully")
        return render_template("user_profile.html", user=user)
    else:
        return redirect("/")



@app.route("/search")
def all_events_result():
    """Find all events using Ticketmaster."""

    keyword = request.args.get("keyword", "")
    postalCode = request.args.get("zipcode", "")
    radius = request.args.get("radius", "")
    sort = request.args.get("sort", "")
    page = request.args.get("page",0)

    # Url limited to USA only
    url = "https://app.ticketmaster.com/discovery/v2/events.json?countryCode=US"
    payload = {
        "apikey": TICKETMASTER_KEY,
        "keyword": keyword,
        "postalCode": postalCode,
        "radius": radius,
        "unit": "miles",
        "sort": sort,
        "page": page
        }
    # add if statement here using radius must add in zipcode too, flash msg to redirect


    res = requests.get(url, params=payload)
    data = res.json()
    # out_file = open("events.json", "w")
    # import json
    # json.dump(data, out_file)
    # out_file.close()
    
    if "_embedded" in data:
        events = data["_embedded"]["events"]
        return render_template("search_results.html",
                           pformat=pformat,
                           data=data,
                           results=events)
    else:
        flash("need msg")
        return redirect("/")


    
@app.route("/event/<id>")
def show_event(id):
    """View the details on a specific event."""

    url = f"https://app.ticketmaster.com/discovery/v2/events/{id}"
    id_payload = {
        "apikey" : TICKETMASTER_KEY,
    }
    res = requests.get(url, params=id_payload)
    data = res.json()
    
    if "_embedded" in data:
        event = data["_embedded"]["venues"]
        
    else:
        event = []
    
    evt_in_db = crud.get_event_by_id(id)
    if not evt_in_db:
        new_event = crud.create_event(id, 
                                    data["name"], 
                                    data["classifications"][0]["genre"]["name"],
                                    data["dates"]["start"]["localDate"],
                                    event[0]["postalCode"],
                                    event[0]["location"]["latitude"],
                                    event[0]["location"]["longitude"])
        db.session.add(new_event)
        db.session.commit()
    # write another crud fxn to get all reviews under this event or will be empty (conditionals if needed)
    # pass it thru jinja templete
    # should populate the reviews when refresh
    return render_template("event_details.html",
                           event_id=id, 
                           pformat=pformat,
                           data=data, 
                           event=event)



@app.route("/event/<id>/review", methods=["POST"])
def add_review(id):
    """Add review within an event page."""
    
    event_id = request.form.get("event-id")
    print(event_id)
    rating_score = request.form.get("rating", "")
    print(rating_score)
    review_title = request.form.get("title", "")
    print(review_title)
    review_description = request.form.get("review", "")
    print(review_description)
    review_recommend = request.form.get("recommendation", "")
    
    if review_recommend == "yes":
        review_recommend = True
    else:
        review_recommend = False
    print(review_recommend)
    current_date = datetime.now()
    review_date = current_date.strftime("%m/%d/%Y %H:%M")
    # check if event_id in db, session.add if is not

    
    review = crud.create_review(session["user"],
                                event_id, 
                                rating_score, 
                                review_title, 
                                review_description, 
                                review_recommend, 
                                review_date)
    db.session.add(review)
    db.session.commit()
    flash("Successfully added a review.")
    
    return redirect(f"/event/{event_id}")
                    # event_id=event_id, 
                    # rating_score=rating_score, 
                    # review_title=review_title, 
                    # review_description=review_description,
                    # review_recommend=review_recommend,
                    # review_date=review_date
                    



# @app.route("/edit_review")
# def edit_review():
#     """Edit a previously written review."""
#     user_id = request.args.get("user_id")
#     event_id = request.args.get("event_id")
#     rating_score = request.args.get("rating_score", "")
#     review_title = request.args.get("review_title", "")
#     review_description = request.args.get("review_description", "")
#     review_recommend = request.args.get("review_recommend", "")
#     review_date = request.args.get("review_date", "")
#     edit_review_date = datetime.now()
#     # Need the edit_review_date? Create new table in model.py?
#     updated_review = crud.create_review(user_id, 
#                                         rating_score, 
#                                         review_title, 
#                                         review_description, 
#                                         review_recommend, 
#                                         review_date, 
#                                         edit_review_date)
    
#     db.session.add(updated_review)
#     db.session.commit()
#     flash("Successfully edited a review.")
#     return redirect("/event/<id>",
#                     user_id=user_id,
#                     event_id=event_id, 
#                     rating_score=rating_score, 
#                     review_title=review_title, 
#                     review_description=review_description,
#                     review_recommend=review_recommend,
#                     review_date=review_date,
#                     edit_review_date=edit_review_date)
# When editing a review, do I need too session add all data that are already exist?
# Should it redirect to /event/<id> OR /event/<id>/review?



@app.route("/view_user_reviews")
def view_review():
    """View all review(s) written by the login user."""

    user = crud.get_user_by_id(session["user"])
    reviews = crud.get_review_by_userid(user.user_id)

    return render_template("user_reviews.html", user=user, reviews=reviews)



@app.route("/delete_review")
def delete_review():
    """Delete a review submitted by user previously."""
    # Need more work, button is clickable but is not removing the review
    review = crud.get_review_by_reviewid(review.review_id)
    if review:
        db.session.delete(review)
        db.session.commit()
    return render_template("user_reviews.html", review=review)




if __name__ == "__main__":
    connect_to_db(app)
    app.app_context().push()
    app.run(host="0.0.0.0", debug=True)