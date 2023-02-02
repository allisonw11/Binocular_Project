"""Server for event look-up app"""
from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
from pprint import pformat
from jinja2 import StrictUndefined
import requests
import crud
import os

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
TICKETMASTER_KEY = os.environ["TICKETMASTER_KEY"]

@app.route("/")
def homepage():
    """View Homepage."""
    
    return render_template("homepage.html")



@app.route("/", methods=["POST"])
def log_in():
    """Log-in a user."""
    # Handle submission of the login form at homepage
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.login_user(email, password)
    
    if user:
        session["user"] = user
        flash("You are successfully logged in.")
    else:
        flash("Error! Please create a new account.")
    return redirect("/")



@app.route("/")
def log_out():
    """Log-out a user. 2.0 features"""
pass
    

    
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

    # This url is limited to USA events only
    url = "https://app.ticketmaster.com/discovery/v2/events.json?countryCode=US"
    payload = {
        "apikey": TICKETMASTER_KEY,
        "keyword": keyword,
        "postalCode": postalCode,
        "radius": radius,
        "unit": "miles",
        "sort": sort,
        }
    # add if statement here to make user who fill in radius must add in zipcode too, flash msg to redirect

    res = requests.get(url, params=payload)
    data = res.json()
    
    if "_embedded" in data:
        # print("yes _embedded in data")
        events = data["_embedded"]["events"]
        return render_template("search_results.html",
                           pformat=pformat,
                           data=data,
                           results=events)
    else:
        flash("need msg")
        return redirect("/")
    # create new page when there is ZERO result? instead of redirect?


@app.route("/search/next_page", methods=["POST"])
def next_page():
    url = request.json.get("url")
    payload = {"apikey": TICKETMASTER_KEY}
    next_page_url = requests.get("https://app.ticketmaster.com"+url,params=payload)
    data = next_page_url.json()
    return redirect("/search", data=data)


@app.route("/search/<page>")
def change_page(page):
    url = "https://app.ticketmaster.com/discovery/v2/events.json?countryCode=US"
    payload = {
        "apikey":TICKETMASTER_KEY,
        "keyword": keyword,
        "postalCode": postalCode,
        "radius": radius,
        "unit": "miles",
        "sort": sort,
        "page":page
        }
    

    
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

    return render_template("event_details.html", pformat=pformat, data=data, event=event)



if __name__ == "__main__":
    connect_to_db(app)
    app.app_context().push()
    app.run(host="0.0.0.0", debug=True)