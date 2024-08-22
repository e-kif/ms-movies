import json

DATA_FILE = 'data.json'  # dictionary of manually entered movies
# DATA_FILE = "data2.json"  # parcing result of imdb top 250 movies

def list_movies():
    """Returns a dictionary of dictionaries that
    contains the movies information in the database.
    The function loads the information from the JSON
    file and returns the data.
    :return: dictionary
    """
    with open(DATA_FILE, "r") as database_file:
        return json.loads(database_file.read())


def update_database(database):
    """Function rewrites database JSON file
    :param database: dictionary
    :return: None
    """
    with open(DATA_FILE, "w") as database_file:
        database_file.write(json.dumps(database))


def add_movie(title, year, rating):
    """Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it.
    """
    database = list_movies()
    database[title] = {'year': year,
                       'rating': rating}
    update_database(database)


def delete_movie(title):
    """Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it.
    """
    database = list_movies()
    del database[title]
    update_database(database)


def update_movie(title, rating):
    """Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it.
    """
    database = list_movies()
    database[title]['rating'] = rating
    update_database(database)
