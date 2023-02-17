"""Script to seed database.""" 
import os
import json
from random import choice, randint
from datetime import datetime
import crud
import model
import server

os.system("dropdb eventsLocator")
os.system("createdb eventsLocator")
model.connect_to_db(server.app)
server.app.app_context().push()
model.db.create_all()


with open('data/events.json') as f:
    event_data = json.loads(f.read())
    
events_in_db = []
events = event_data["_embedded"]["events"]

for event in events:
    event_id = event["id"]
    event_title = event["name"]
    event_genre = event["classifications"][0]["genre"]["name"]
    event_date = datetime.strptime(event["dates"]["start"]["localDate"], "%Y-%m-%d")
    if "place" in event:
        event_zipcode = event['place']['postalCode']
    else:
        event_zipcode = event['_embedded']["venues"][0]["postalCode"]
    event_lat = float(event['_embedded']["venues"][0]["location"]["latitude"])
    event_lng = float(event['_embedded']["venues"][0]["location"]["longitude"])
    
    # Create a movie here and append it to movies_in_db
    db_event = crud.create_event(event_id, event_title, event_genre, event_date, event_zipcode, event_lat, event_lng)
    events_in_db.append(db_event)

model.db.session.add_all(events_in_db)
model.db.session.commit()



# Create 3 users and each user will make 5 reviews for testing:
for n in range(3):
    fname = "User"
    lname = f"{n}"
    email = f"user{n}@test.com"
    password = "test"
    address = f"123{n} Main Street"
    state = "MA"
    zipcode = "02116"
    
    # Create a user and add to User db
    user = crud.create_user(fname, lname, email, password, address, state, zipcode)    
    model.db.session.add(user)
    model.db.session.commit()
    
    # Create 5 reviews for the user
    for _ in range(5):
        random_event = choice(events_in_db)
        rating_score = randint(1, 5)
        review_title = f"Title by User{n}"
        review_description = f"Reviewed by User{n}"
        review_recommend = choice([True,False])
        review_date = "2023-02-28"

        review = crud.create_review(user.user_id, random_event.event_id, rating_score, review_title, review_description, review_recommend, review_date)
        model.db.session.add(review)

model.db.session.commit()

