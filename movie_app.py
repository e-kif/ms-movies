import json
import statistics
import datetime
import random


class MovieApp:
    """Main MovieApp clas responsible for user interaction"""

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
            print(f'{len(movies)} movies in total: {self.movie_string(self._storage.list_movies().keys())}')
        except json.decoder.JSONDecodeError:
            print('Movies database is empty!')

    def movie_string(self, title):
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
            user_input = input(f'Enter a link for the poster: ').strip()
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
        """Åsks user to input a rating for a movie and validates the input
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

    def add_movie(self):
        """Adds new movie to a database storage
        :return: None
        """
        title = MovieApp.get_title()
        year = MovieApp.get_year()
        rating = MovieApp.get_rating()
        poster = MovieApp.get_poster()
        self._storage.add_movie(title, year, rating, poster)

    def delete_movie(self):
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

    def update_movie(self):
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
            rating = MovieApp.get_rating()
            self._storage.update_movie(title, rating)
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
        print(f'The best movie(s): {self.movie_string(best_movies)}')
        print(f'The worst movie(s): {self.movie_string(worst_movies)}')

    def print_random_movie(self):
        """Selects random movie from a storage database and prints it
        :return: None
        """
        data = self._storage.list_movies()
        titles = list(data.keys())
        random_title = titles[random.randint(0, len(titles) - 1)]
        rating = data[random_title]['rating']
        print(f"Your movie for tonight: {random_title}, it's rated {rating}")

    def search_movie(self):
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
            print(f'One movie found matching your request: {self.movie_string(found_movies)}')
        else:
            print(f'List of found movies:{self.movie_string(found_movies)}')

    def print_sorted_by_rating(self):
        """Prints all movies from a database sorted by theirs rating
        :return: None
        """
        data = self._storage.list_movies()
        movies_list = sorted(data.items(), key=lambda item: item[1]['rating'], reverse=True)
        titles = []
        for movie in movies_list:
            titles.append(movie[0])
        print(f'Movies sorted by rating: {self.movie_string(titles)}')

    def print_sorted_by_year(self):
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
        print(f'Movies sorted by year: {self.movie_string(titles)}')

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

    def filter_movies(self):
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
            print(self.movie_string(filtered_movies))

    @staticmethod
    def print_header(text='My Movies Database'):
        """Prints header of the program
        :return: None
        """
        print('*' * 5, text, '*' * 5)

    @staticmethod
    def print_menu():
        """Prints user menu
        :return: None
        """
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

    def _generate_website(self):
        """Generates static html file from html template"""
        pass

    def run(self):
        """Populates function_list dictionary and calls dispatcher function
            :return: None
            """
        MovieApp.function_list['0. Exit'] = "exit_loop"
        MovieApp.function_list['1. List movies'] = self._command_list_movies
        MovieApp.function_list['2. Add movie'] = self.add_movie
        MovieApp.function_list['3. Delete movie'] = self.delete_movie
        MovieApp.function_list['4. Update movie'] = self.update_movie
        MovieApp.function_list['5. Stats'] = self._command_movie_stats
        MovieApp.function_list['6. Random movie'] = self.print_random_movie
        MovieApp.function_list['7. Search movie'] = self.search_movie
        MovieApp.function_list['8. Movies sorted by rating'] = self.print_sorted_by_rating
        MovieApp.function_list['9. Movies sorted by year'] = self.print_sorted_by_year
        MovieApp.function_list['10. Filter movies'] = self.filter_movies
        MovieApp.dispatcher()
