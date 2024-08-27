import argparse
import os
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv
from movie_app import MovieApp


def main():
    """Reads passed commandline argument, create instance of class StorageJson or StorageCsv,
    MovieApp and runs MovieApp
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('echo')
    filename_from_argument = parser.parse_args().echo
    if filename_from_argument.endswith('.csv'):
        storage = StorageCsv(filename_from_argument)
    elif filename_from_argument.endswith('.json'):
        storage = StorageJson(filename_from_argument)
    else:
        filename = os.path.join("data", "data.csv")
        print(f'No valid filename is provided. Proceeding with default database "{filename}"')
        storage = StorageCsv(filename)

    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
