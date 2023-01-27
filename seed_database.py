"""Script to seed database.""" 
# import os
# import json

# from datetime import datetime

# import crud
# import model
# import server

# model.connect_to_db(server.app)
# model.db.create_all()

# # Create a fake user for testing:
# email = "user@test.com"
# password = "test"

# user = crud.create_user(email, password)

# model.db.session.add(user)
# model.db.session.commit()



# # EXAMPLE from movie rating app --->
# os.system("dropdb ratings")

# # This will re-creating a database is run dropdb and createdb automatically
# os.system("createdb ratings")

# # This will connect to the database and call db.create_all
# model.connect_to_db(server.app)
# model.db.create_all()

# # This will load data from data/movies.json and save it to a variable
# with open('data/movies.json') as f:
#     movie_data = json.loads(f.read())
    
# # Create movies, store them in list so we can use them
# # to create fake ratings later
# movies_in_db = []
# for movie in movie_data:
#     # TODO: 
#     # Get the title, overview, and poster_path from the movie dictionary.
#     title, overview, poster_path = (movie["title"], movie["overview"], movie["poster_path"])
#     # Then, get the release_date and convert it to datetime object with datetime.strptime
#     release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")
    
#     # TODO: create a movie here and append it to movies_in_db
#     db_movie = crud.create_movie(title, overview, release_date, poster_path)
#     movies_in_db.append(db_movie)

# model.db.session.add_all(movies_in_db)
# model.db.session.commit()

# # <--- END of EXAMPLE