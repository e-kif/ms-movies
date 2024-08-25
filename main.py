from storage_json import StorageJson
from movie_app import MovieApp


def main():
    """Creates instances of class StorageJson and MovieApp, runs MovieApp"""
    storage = StorageJson('data.json')
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
