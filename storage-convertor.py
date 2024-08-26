import json
import csv


class StorageConvertor:

    def __init__(self, datafile):
        with open(datafile, 'r') as handle:
            if datafile.endswith(".json"):
                self._storage = json.loads(handle.read())
            else:
                handle.readline()
                reader = csv.reader(handle)
                self._storage = {}
                for line in reader:
                    print(line)
                    title, year, rating, poster = tuple(line)
                    year = int(year)
                    rating = float(rating)
                    self._storage[title] = {"year": year,
                                            "rating": rating,
                                            "poster": poster}

    def save_database_as_csv(self, csv_file):
        with open(csv_file, 'w') as handle:
            handle.write('"title","year","rating","poster"')
            for title, info in self._storage.items():
                year = info['year']
                rating = info['rating']
                poster = info.get('poster', '')
                handle.write(f'\n"{title}",{year},{rating},"{poster}"')
        print(f'Movies database was save to file {csv_file} successfully.')

    def save_database_as_json(self, json_file):
        with open(json_file, 'w') as handle:
            handle.write(json.dumps(self._storage))
        print(f'Movies database was saved to file {json_file} successfully.')


sor = StorageConvertor('data.csv')
# sor.save_database_as_csv('data.csv')
sor.save_database_as_json('data2.json')