import csv
from istorage import IStorage


class StorageCsv(IStorage):
    """class for dealing with csv-file movie storages"""

    def __init__(self, storage):
        """Instance initialization"""
        self._storage = storage

    def list_movies(self):
        """Reads database file, converts csv data into movies dictionary
         returns dictionary
         :return: dict"""
        with open(self._storage, 'r') as handle:
            handle.readline()
            reader = csv.reader(handle)
            movies = {}
            for line in reader:
                title, year, rating, poster = tuple(line)
                year = int(year)
                rating = float(rating)
                movies[title] = {"year": year,
                                 "rating": rating,
                                 "poster": poster}
        return movies

    def update_database(self, database):
        """Writes given database in a csv file
        :param database: dictionary of movies
        :return: None
        """
        with open(self._storage, 'w') as handle:
            handle.write('"title","year","rating","poster"')
            for title, info in database.items():
                handle.write(f'\n"{title}",{info["year"]},{info["rating"]},"{info["poster"]}"')

    def add_movie(self, title, year, rating, poster):
        """Reads movies database, adds one movie, saves new database to a csv file
        :param title: str, movie title
        :param year: int, movie release year
        :param rating: float, movie rating
        :param poster: str, URL for movie poster
        :return: None
        """
        movies = self.list_movies()
        movies[title] = {"year": year,
                         "rating": rating,
                         "poster": poster}
        self.update_database(movies)
        print(f'Movie "{title}" was added to the movies database.')

    def delete_movie(self, title):
        """Removes a movie from a database based on a given movie title"""
        movies = self.list_movies()
        del movies[title]
        self.update_database(movies)

    def update_movie(self, title, rating):
        """Updates movie's rating"""
        movies = self.list_movies()
        movies[title]['rating'] = rating
        self.update_database(movies)
