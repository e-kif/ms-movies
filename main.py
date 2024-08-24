from storage_json import StorageJson


def main():
    storage = StorageJson('data.json')
    print(storage.list_movies())
    storage.add_movie('Nobody', 2021, 7.4, "https://m.media-amazon.com/images/M/MV5BMjM5YTRlZmUtZGVmYi00ZjE2LWIyNzAtOWVhMDk1MDdkYzhjXkEyXkFqcGdeQXVyMjMxOTE0ODA@._V1_FMjpg_UY5000_.jpg")
    print(storage.list_movies())

if __name__ == "__main__":
    main()
