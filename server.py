"""Server for event look-up app"""
from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
from pprint import pformat
from jinja2 import StrictUndefined
import requests
import crud
import os
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
TICKETMASTER_KEY = os.environ["TICKETMASTER_KEY"]

@app.route("/")
def homepage():
    """View Homepage."""
    
    user = crud.get_user_by_id(session.get("user"))
    
    if user:
        url = "https://app.ticketmaster.com/discovery/v2/events.json?countryCode=US"
        payload = {
            "apikey": TICKETMASTER_KEY,
            "postalCode": user.zipcode,
            "size": "50"
            }
        res = requests.get(url, params=payload)
        data = res.json()
        
        if "_embedded" in data:
            events = data["_embedded"]["events"]
            random_events = random.sample(events,k=5)

            return render_template("homepage.html",
                                    data=data,
                                    results=random_events)
    return render_template("homepage.html")



@app.route("/", methods=["POST"])
def log_in():
    """Log-in a user."""
    
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.login_user(email, password)
    
    if user:
        session["user"] = user
        flash("You are signed in.", category="success")
    else:
        flash("Incorrect email/password. Try again.", category="error")
    return redirect("/")



@app.route("/logout")
def log_out():
    """Log-out a user."""
    
    session.clear()
    return redirect("/")
    

    
@app.route("/new_account")
def create_account():
    """View create account page."""
    
    if "user" not in session:
        return render_template("new_account.html")
    else:
        flash("You are already login!", category="success")
        return redirect("/")


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
    
    # should we keep this or use regex from html?
    if len(fname)<2:
        flash("First name must be greater than 2 characters.", category="error")    
    elif len(lname)<=2:
        flash("Last name must be greater than 1 character.", category="error")
    elif "@" not in email and len(email)<5:
        flash("Not a valid email address.", category="error")
    elif len(password)<8:
        flash("Password must be at least 8 characters.", category="error")
    elif len(address)<5:
        flash("This is not a valid address.", category="error")
    elif len(zipcode)<5:
        flash("Zipcode must have 5 digits.", category="error")
    else:
        user = crud.create_user(fname,lname,email,password,address,state,zipcode)
        db.session.add(user)
        db.session.commit()
        flash("You have created a new account.", category="success")
        return redirect("/")
    return render_template("new_account.html")


@app.route("/user_profile")
def user_profile():
    """View indivdual user's profile."""
    
    user = crud.get_user_by_id(session["user"])
    
    if "user" in session:
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
    
    if "_embedded" in data:
        events = data["_embedded"]["events"]
        return render_template("search_results.html",
                            data=data,
                            results=events
                            )
    else:
        flash("No event match your search setting. Please try again.", category="error")
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
                                    event[0]["location"]["longitude"]
                                    )
        db.session.add(new_event)
        db.session.commit()

    reviews_in_event = crud.get_review_by_eventid(id)
    
    return render_template("event_details.html",
                           event_id=id, 
                           pformat=pformat,
                           data=data, 
                           event=event,
                           reviews_in_event=reviews_in_event
                           )



@app.route("/event/<id>/review", methods=["POST"])
def add_review(id):
    """Add review within an event page."""
    
    event_id = request.form.get("event-id")
    rating_score = request.form.get("rating", "")
    review_title = request.form.get("title", "")
    review_description = request.form.get("review", "")
    review_recommend = request.form.get("recommendation", "")
    
    if review_recommend == "yes":
        review_recommend = True
    else:
        review_recommend = False
    current_date = datetime.now()
    review_date = current_date.strftime("%m/%d/%Y")

    review = crud.create_review(session["user"],
                                event_id, 
                                rating_score, 
                                review_title, 
                                review_description, 
                                review_recommend, 
                                review_date
                                )
    db.session.add(review)
    db.session.commit()
    flash("You have added a review.", category="success")
    
    return redirect(f"/event/{event_id}")
                    


@app.route("/edit_review", methods=["POST"])
def edit_review():
    """Edit a previously written review by user."""
    
    event_id = request.json.get("event_id")
    rating_score = request.json.get("rating", "")
    review_title = request.json.get("title", "")
    review_description = request.json.get("review", "")
    review_recommend = request.json.get("recommendation", "")
    
    updated_review = crud.updated_review(session["user"],
                                         event_id,
                                         rating_score, 
                                         review_title, 
                                         review_description, 
                                         review_recommend, 
                                        )
    db.session.add(updated_review)
    db.session.commit()
    flash("You have updated your review.", category="success")
    return "Review has been updated."



@app.route("/view_user_reviews")
def view_review():
    """View all review(s) written by the login user."""

    user = crud.get_user_by_id(session["user"])
    reviews = crud.get_review_by_userid(user.user_id)
    
    return render_template("user_reviews.html", user=user, reviews=reviews)



@app.route("/help")
def help():
    """Help page to navigate the site."""
    
    return render_template("help.html")

if __name__ == "__main__":
    connect_to_db(app)
    app.app_context().push()
    app.run(host="0.0.0.0", debug=True)