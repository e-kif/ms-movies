from storage_json import StorageJson
from storage_csv import StorageCsv
from movie_app import MovieApp


def main():
    """Creates instances of class StorageJson or Storage CSV and MovieApp, runs MovieApp"""
    storage = StorageJson('data2.json')
    # storage = StorageCsv('data.json')
    movie_app = MovieApp(storage)
    movie_app.run()
    # movie_app.update_movies_info()


if __name__ == "__main__":
    main()
