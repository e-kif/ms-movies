import json
import statistics
import datetime
import random
import requests
import dotenv
import pycountry


class MovieApp:
    """Main MovieApp clas responsible for user interaction"""

    api_key = dotenv.get_key('.env', 'API_KEY')
    function_list = {}
    min_rating = 0
    max_rating = 10

    def __init__(self, storage):
        """Instance initialization"""
        self._storage = storage

    def _command_list_movies(self):
        """Prints all movies from instance storage"""
        movies = self._storage.list_movies()
        try:
            print(f'{len(movies)} movies in total: {self._movie_string(self._storage.list_movies().keys())}')
        except json.decoder.JSONDecodeError:
            print('Movies database is empty!')

    def _movie_string(self, title):
        """Takes a movie title and returns a string with info
        about movie or a multistring with info about movies
        :param title: movie title as a string,
        list of movie titles or a dictionary key with movie titles
        :return: string or multistring
        """
        movies = self._storage.list_movies()
        if type(title) is type(movies.keys()):
            title = list(title)
        if isinstance(title, list):
            if len(title) > 1:
                return_string = ""
                for movie in title:
                    year = movies[movie]['year']
                    rating = movies[movie]['rating']
                    return_string += f'\n\t{movie} ({year}): {rating}'
                return return_string
            title = title[0]
        year = movies[title]['year']
        rating = movies[title]['rating']
        return f'{title} ({year}): {rating}'

    @staticmethod
    def get_title(custom_string=""):
        """Gets movie title from user input
        :param custom_string: additional string for user input
        :return: string
        """
        if custom_string:
            custom_string = " " + custom_string
        while True:
            user_input = input(f'Enter the name of a movie{custom_string}: ').strip()
            if not user_input:
                print('Movie title can not be empty')
                continue
            return user_input

    @staticmethod
    def get_poster():
        """Gets movie poster from user input
        :return: string
        """
        while True:
            user_input = input('Enter a link for the poster: ').strip()
            if not user_input:
                print('Movie poster can not be empty')
                continue
            return user_input

    @staticmethod
    def get_year():
        """Asks user for a movie year as an input, validates the user input
        :return: integer
        """
        while True:
            try:
                year = int(input('Enter movie release year: '))
                if year > 0:
                    return year
                raise ValueError
            except ValueError:
                print('Expected a positive integer')

    @staticmethod
    def get_rating():
        """Asks user to input a rating for a movie and validates the input
        :return: float
        """
        while True:
            try:
                rating = float(input('Enter movie rating: '))
                if MovieApp.min_rating <= rating <= MovieApp.max_rating:
                    return rating
                raise ValueError
            except ValueError:
                print(f'Expected a number between {MovieApp.min_rating} and {MovieApp.max_rating}')

    def _add_movie(self):
        """Adds new movie to a database storage"""
        movie_info = MovieApp.get_movie_info()
        if movie_info:
            title, year, rating, poster, imdb_id, flag = movie_info
            self._storage.add_movie(title, year, rating, poster, imdb_id, flag)

    def _delete_movie(self):
        """Deletes a movie from a storage database
        :return: None
        """
        while True:
            title = MovieApp.get_title('you want to delete')
            try:
                self._storage.delete_movie(title)
                print(f'Movie "{title}" is deleted')
                break
            except KeyError:
                print(f'There is no movie called "{title}" in a database')

    def _update_movie(self):
        """Updates movie year and rating for a specific movie
        :return: None
        """
        while True:
            title = MovieApp.get_title('you want to update')
            try:
                if title not in self._storage.list_movies():
                    raise KeyError
            except KeyError:
                print(f'There is no movie called "{title}" in a database')
                continue
            movie_notes = ""
            while not movie_notes:
                movie_notes = input('Enter movie notes: ').strip()
                if not movie_notes:
                    print('Movie notes can not be empty.')
            self._storage.update_movie(title, movie_notes)
            print(f'Movie {title} updated successfully.')
            break

    def _command_movie_stats(self):
        """Prints statistics of storage database movies
            :return: None
            """
        data = self._storage.list_movies()
        ratings = []
        best_movies = []
        worst_movies = []
        for title, info in data.items():
            ratings.append(info['rating'])
        ratings.sort()
        worst_rating = min(ratings)
        best_rating = max(ratings)
        average = round(sum(ratings) / len(ratings), 2)
        median = round(statistics.median(ratings), 2)
        for title, info in data.items():
            if info['rating'] == worst_rating:
                worst_movies.append(title)
            if info['rating'] == best_rating:
                best_movies.append(title)
        print('Statistics about the movies in the database:')
        print(f'Average rating: {average}')
        print(f'Median rating: {median}')
        print(f'The best movie(s): {self._movie_string(best_movies)}')
        print(f'The worst movie(s): {self._movie_string(worst_movies)}')

    def _print_random_movie(self):
        """Selects random movie from a storage database and prints it
        :return: None
        """
        data = self._storage.list_movies()
        titles = list(data.keys())
        random_title = titles[random.randint(0, len(titles) - 1)]
        rating = data[random_title]['rating']
        print(f"Your movie for tonight: {random_title}, it's rated {rating}")

    def _search_movie(self):
        """Searches movies matching user input criteria
        :return: None
        """
        data = self._storage.list_movies()
        search_param = input('Enter part of movie name: ')
        found_movies = []
        for title in data.keys():
            if search_param.lower() in title.lower():
                found_movies.append(title)
        if not found_movies:
            print('There are no movies matching your request.')
        elif len(found_movies) == 1:
            print(f'One movie found matching your request: {self._movie_string(found_movies)}')
        else:
            print(f'List of found movies:{self._movie_string(found_movies)}')

    def _print_sorted_by_rating(self):
        """Prints all movies from a database sorted by theirs rating
        :return: None
        """
        data = self._storage.list_movies()
        movies_list = sorted(data.items(), key=lambda item: item[1]['rating'], reverse=True)
        titles = []
        for movie in movies_list:
            titles.append(movie[0])
        print(f'Movies sorted by rating: {self._movie_string(titles)}')

    def _print_sorted_by_year(self):
        """Prints all movies from a storage database by release year
        :return: None
        """
        data = self._storage.list_movies()
        while True:
            years_sorting = input('Do you want the latest movies firs? (Y/N) ').lower()
            is_sorting_reverse = years_sorting == "y"
            if years_sorting in ("n", "y"):
                break
            print('Please enter "Y" or "N"')
        movies_list = sorted(data.items(), key=lambda item: item[1]['year'], reverse=is_sorting_reverse)
        titles = []
        for movie in movies_list:
            titles.append(movie[0])
        print(f'Movies sorted by year: {self._movie_string(titles)}')

    @staticmethod
    def movie_filters_range(extreme):
        """Gets a minimum or maximum rating for movies filter
        :param extreme: string ('minimum' or 'maximum')
        :return: float
        """
        if extreme == "minimum":
            edge = MovieApp.min_rating
        else:
            edge = MovieApp.max_rating
        while True:
            user_input = input(f'Enter {extreme} rating '
                               f'(leave blank for no {extreme} rating): ').strip()
            if not user_input:
                return edge
            try:
                result = float(user_input)
                if MovieApp.min_rating <= result <= MovieApp.max_rating:
                    return result
                raise ValueError
            except ValueError:
                print(f'Excepted a number between {MovieApp.min_rating} and {MovieApp.max_rating}')

    @staticmethod
    def movie_filters_year(extreme):
        """Gets a start or end year for movies filter
        :param extreme: string ('start' or 'end')
        :return: integer
        """
        if extreme == "start":
            edge = 0
        else:
            edge = datetime.date.today().year
        while True:
            user_input = input('Enter start year (leave blank for no start year): ').strip()
            if not user_input:
                return edge
            try:
                result = int(user_input)
                if result > 0:
                    return result
                raise ValueError
            except ValueError:
                print('Excepted a positive integer')

    def _filter_movies(self):
        """Asks user to enter minimum, maximum rating, start and end year.
        Prints lis of movies, matching entered criteria.
        :return: None
        """
        data = self._storage.list_movies()
        filtered_movies = []
        # Getting user input
        min_rating = MovieApp.movie_filters_range("minimum")
        max_rating = MovieApp.movie_filters_range("maximum")
        start_year = MovieApp.movie_filters_year("start")
        end_year = MovieApp.movie_filters_year("end")
        # creating list of filtered movies and printing the movies
        for movie, info in data.items():
            if (min_rating <= info['rating'] <= max_rating
                    and start_year <= info['year'] <= end_year):
                filtered_movies.append(movie)
        if not filtered_movies:
            print('No movies matching your filter')
        else:
            print('Filtered movies:')
            print(self._movie_string(filtered_movies))

    @staticmethod
    def print_header(text='My Movies Database'):
        """Prints header of the program"""
        print('*' * 5, text, '*' * 5)

    @staticmethod
    def print_menu():
        """Prints user menu"""
        menu_items = []
        print('\nMenu:')
        for item in MovieApp.function_list:
            menu_items.append(item)
            print(f'\t{item}')

    @staticmethod
    def dispatcher():
        """Dispatcher function. Calls a list of functions, that draw user interface
        and calls functions based on the user input in a constant loop
        :return: None
        """
        MovieApp.print_header()
        while True:
            MovieApp.print_menu()
            last_menu_item = len(MovieApp.function_list) - 1
            try:
                menu_item = int(input(f'\nEnter choice (0 - {last_menu_item}): '))
                if menu_item < 0 or menu_item > len(MovieApp.function_list) - 1:
                    raise ValueError
            except ValueError:
                print('Invalid choice')
                continue
            if not menu_item:
                print('Bye!')
                break
            list(MovieApp.function_list.values())[menu_item]()
            input('\nPress "Enter" to continue')
            continue

    @staticmethod
    def html_tag_wrap(content, tag="div", class_=""):
        """Wraps the content into given HTML tag with given CSS class"""
        if class_:
            class_ = f'class="{class_}"'
        if tag == 'img':
            return f'<{tag} {class_} src="{content}" alt="movie-poster">'

        return f'<{tag} {class_}>{content}</{tag}>'

    @staticmethod
    def serialize_movie(title, year, rating, poster, notes, imdb_id, flag):
        """Serializes one movie, returns valid HTML markup for one move (list item)"""
        country_flag = MovieApp.html_tag_wrap(flag, "div", "flag")
        img = MovieApp.html_tag_wrap(poster, "img", "movie-poster")
        if notes:
            img = img.replace('<img',  f'<img title="{notes}" ')
        img = (img.replace('<img', f'<a href="https://imdb.com/title/{imdb_id}" target="_blank"><img')
               + '</a>')
        movie_title = MovieApp.html_tag_wrap(title, "div", "movie-title")
        release_year = MovieApp.html_tag_wrap(year, "div", "movie-year")
        rating = float(rating) #  converting for valid HTML from JSON
        rating_star = (f'<i style="left: {rating*10}%" class="fa-solid fa-star"></i>'
                       f'<span style="left: {rating*10}%" class="ratings">{rating}</span>')
        movie_rating = (MovieApp.html_tag_wrap(rating_star, "div", "movie-rating-bar")
                        .replace('<div', '<div style="background: linear-gradient(#F2A766 0 0) 0/'
                                         f'{rating*10}% no-repeat #F2D8C9;"'))
        movie_html = MovieApp.html_tag_wrap(country_flag + img + movie_title + release_year
                                            + movie_rating, "div", "movie")
        return MovieApp.html_tag_wrap(movie_html, "li")

    def _generate_website(self):
        """Generates static html file from html template"""
        movies = self._storage.list_movies()
        movies_html_list_items = ""
        for title, info in movies.items():
            movies_html_list_items += MovieApp.serialize_movie(title,
                                                               info['year'],
                                                               info['rating'],
                                                               info['poster'],
                                                               info.get('notes', ''),
                                                               info.get('imdb_id', ''),
                                                               info.get('flag', ''))
        with open("_static/index_template.html", 'r', encoding='utf-8') as handle:
            html_template = handle.read()
        with open('_static/index.html', 'w') as handle:
            handle.write(html_template.replace("__TEMPLATE_MOVIE_GRID__", movies_html_list_items)
                         .replace('__TEMPLATE_TITLE__', 'My Movie App'))
        print('Movie website was generated successfully.')

    def _update_movies_info(self):
        """Goes through each movie title and updates all other info from API"""
        new_movies = {}
        for title in self._storage.list_movies().keys():
            url = "http://www.omdbapi.com/?apikey=" + MovieApp.api_key + "&t=" + title
            try:
                response = requests.get(url).json()
            except requests.exceptions.ConnectionError:
                print('Houston, we have some connection problems. No internet connection.\n'
                      "Try updating movies' information later")
                return None
            print(f'Updating movie "{title}" info.')
            new_movies[title] = {'year': response['Year'],
                                 'rating': response['imdbRating'],
                                 'poster': response['Poster'],
                                 'notes': self._storage.list_movies()[title].get('notes', ''),
                                 'imdb_id': response['imdbID'],
                                 'flag': MovieApp.get_country_flag(response)}
        self._storage.update_database(new_movies)
        print("All movies' info was updated successfully")

    @staticmethod
    def get_movie_info():
        """Asks user of movie title, gets movie's info from api. If connection error asks user for movie info
        :return: tuple (title, year, rating, poster)
        """
        while True:
            title = MovieApp.get_title()
            url = "http://www.omdbapi.com/?apikey=" + MovieApp.api_key + "&t=" + title
            try:
                response = requests.get(url).json()
            except requests.exceptions.ConnectionError:
                print('Houston, we have some connection problems! There is no Internet connection.')
                try_again = input('Do you want to try again? y/N: ').strip().lower()
                if try_again in ['yes', 'y']:
                    continue
                while True:
                    manual_enter = input('Do you want to enter required data manually? Y/n: ').strip().lower()
                    if manual_enter in ["", "y", "yes"]:
                        return title, MovieApp.get_year(), MovieApp.get_rating(), MovieApp.get_poster()
                    print('Better luck next time!')
                    return None
            if response['Response'] == 'False':
                print(response['Error'])
                continue
            break
        return (title,
                response['Year'],
                response['imdbRating'],
                response['Poster'],
                response['imdbID'],
                MovieApp.get_country_flag(response))

    @staticmethod
    def get_country_flag(response):
        """Gets country flag emoji from api response or entered country as a string"""
        if isinstance(response, str):
            return pycountry.countries.get(name=response).flag
        country = response['Country'].split(",")[0]
        if country == 'Russia':
            country = 'Russian Federation'
        return pycountry.countries.get(name=country).flag

    def run(self):
        """Populates function_list dictionary and calls dispatcher function
            :return: None
            """
        MovieApp.function_list['0. Exit'] = "exit_loop"
        MovieApp.function_list['1. List movies'] = self._command_list_movies
        MovieApp.function_list['2. Add movie'] = self._add_movie
        MovieApp.function_list['3. Delete movie'] = self._delete_movie
        MovieApp.function_list['4. Update movie'] = self._update_movie
        MovieApp.function_list['5. Stats'] = self._command_movie_stats
        MovieApp.function_list['6. Random movie'] = self._print_random_movie
        MovieApp.function_list['7. Search movie'] = self._search_movie
        MovieApp.function_list['8. Movies sorted by rating'] = self._print_sorted_by_rating
        MovieApp.function_list['9. Movies sorted by year'] = self._print_sorted_by_year
        MovieApp.function_list['10. Filter movies'] = self._filter_movies
        MovieApp.function_list['11. Generate a website'] = self._generate_website
        MovieApp.function_list['12. Update movies info'] = self._update_movies_info
        MovieApp.dispatcher()
