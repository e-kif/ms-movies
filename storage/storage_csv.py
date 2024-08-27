import csv
from storage.istorage import IStorage


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
                if len(line) == 4:
                    line += [""]
                title, year, rating, poster, notes = tuple(line)
                year = int(year)
                rating = float(rating)
                movies[title] = {"year": year,
                                 "rating": rating,
                                 "poster": poster,
                                 "notes": notes}
        return movies

    def update_database(self, database):
        """Writes given database in a csv file
        :param database: dictionary of movies
        :return: None
        """
        with open(self._storage, 'w') as handle:
            handle.write('"title","year","rating","poster","notes"')
            for title, info in database.items():
                handle.write(f'\n"{title}",'
                             f'{info["year"]},'
                             f'{info["rating"]},'
                             f'"{info["poster"]}",'
                             f'"{info.get("notes", "")}"')
