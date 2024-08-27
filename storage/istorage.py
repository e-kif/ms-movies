from abc import ABC, abstractmethod


class IStorage(ABC):

    @abstractmethod
    def list_movies(self):
        pass

    def add_movie(self, title, year, rating, poster):
        """Reads movies database, adds one movie, saves new database to a csv file"""
        movies = self.list_movies()
        movies[title] = {"year": year,
                         "rating": rating,
                         "poster": poster}
        self.update_database(movies)
        print(f'Movie "{title}" was added successfully')

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

    @abstractmethod
    def update_database(self, database):
        pass
