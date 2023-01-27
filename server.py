"""Server for event look-up app"""
from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
from pprint import pformat
from jinja2 import StrictUndefined
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
    """View all events using Ticketmaster."""

    keyword = request.args.get('keyword', '')
    postalcode = request.args.get('zipcode', '')
    radius = request.args.get('radius', '')
    unit = request.args.get('unit', '')
    sort = request.args.get('sort', '')

    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {
        'apikey': TICKETMASTER_KEY,
        'keyword': keyword,
        'postalcode': postalcode,
        'radius': radius,
        'unit': unit,
        'sort': sort,
        }
    res = request.get(url, params=payload)
    data = res.json()
    events = data['_embedded']['events']
    
    return render_template('search_results.html',
                           pformat=pformat,
                           data=data,
                           results=events)
    
@app.route("/search/<event_id>")
def show_event(event_id):
    """Show details on a specific event."""
    
    event = crud.get_event_by_id(event_id)
    
    return render_template("event_details.html", event=event)


if __name__ == "__main__":
    connect_to_db(app)
    app.app_context().push()
    app.run(host="0.0.0.0", debug=True)