from storage_json import StorageJson
from movie_app import MovieApp


def main():
    storage = StorageJson('data.json')
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
