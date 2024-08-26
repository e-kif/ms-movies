import json
from istorage import IStorage


class StorageJson(IStorage):
    """Storage class for dealing with json files storage"""

    def __init__(self, filepath):
        """Instance initialization"""
        self._data_file = filepath

    def list_movies(self):
        """Returns a dictionary of dictionaries that
        contains the movies information in the database.
        The function loads the information from the JSON
        file and returns the data.
        :return: dictionary
        """
        with open(self._data_file, "r") as database_file:
            return json.loads(database_file.read())

    def update_database(self, database):
        """Rewrites database JSON file
        :param database: dictionary
        :return: None
        """
        with open(self._data_file, "w") as database_file:
            database_file.write(json.dumps(database))

    def add_movie(self, title, year, rating, poster):
        """Adds a movie to the movies' database.
        Loads the information from the JSON file, add the movie,
        and saves it.
        """
        database = self.list_movies()
        database[title] = {'year': year,
                           'rating': rating,
                           'poster': poster}
        self.update_database(database)

    def delete_movie(self, title):
        """Deletes a movie from the movies' database.
        Loads the information from the JSON file, deletes the movie,
        and saves it.
        """
        database = self.list_movies()
        del database[title]
        self.update_database(database)

    def update_movie(self, title, rating):
        """Updates a movie from the movies' database.
        Loads the information from the JSON file, updates the movie,
        and saves it.
        """
        database = self.list_movies()
        database[title]['rating'] = rating
        self.update_database(database)
