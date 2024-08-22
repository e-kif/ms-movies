import statistics
import random
import json
import datetime
import movie_storage

function_list = {}
MIN_RATING = 0
MAX_RATING = 10


def get_title(custom_string=""):
    """Function gets movie title from user input
    :param custom_string: additional string for user input
    :return: string
    """
    if custom_string:
        custom_string = " " + custom_string
    while True:
        user_input = input(f'Enter the name of a movie{custom_string}: ')
        if not user_input.strip():
            print('Movie title can not be empty')
            continue
        return user_input


def get_year():
    """Function asks user for a movie year as an input, validates the user input
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


def get_rating():
    """Function asks user to input a rating for a movie and validates the input
    :return: float
    """
    while True:
        try:
            rating = float(input('Enter movie rating: '))
            if MIN_RATING <= rating <= MAX_RATING:
                return rating
            raise ValueError
        except ValueError:
            print(f'Expected a number between {MIN_RATING} and {MAX_RATING}')


def movie_string(title):
    """Function takes a movie title and returns a string with info
    about movie or a multistring with info about movies
    :param title: movie title as a string,
    list of movie titles or a dictionary key with movie titles
    :return: string or multistring
    """
    movies = movie_storage.list_movies()
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


def list_movies():
    """Function prints information of all movies, present in a 'database'
    :return: None
    """
    try:
        data = movie_storage.list_movies()
        print(f'{len(data)} movies in total: {movie_string(data.keys())}')
    except json.decoder.JSONDecodeError:
        print('Movies database is empty!')


def add_movie():
    """Function adds new movie to a 'database'
    :return: None
    """
    title = get_title()
    year = get_year()
    rating = get_rating()
    movie_storage.add_movie(title, year, rating)


def delete_movie():
    """Function deletes a movie from a 'database'
    :return: None
    """
    while True:
        title = get_title('you want to delete')
        try:
            movie_storage.delete_movie(title)
            print(f'Movie "{title}" is deleted')
            break
        except KeyError:
            print(f'There is no movie called "{title}" in a database')


def update_movie():
    """Function updates movie year and rating for a specific movie
    :return: None
    """
    while True:
        title = get_title('you want to update')
        try:
            if title not in movie_storage.list_movies():
                raise KeyError
        except KeyError:
            print(f'There is no movie called "{title}" in a database')
            continue
        rating = get_rating()
        movie_storage.update_movie(title, rating)
        print(f'Movie {title} updated successfully.')
        break


def print_stats():
    """Function prints statistics of movies database
    :return: None
    """
    data = movie_storage.list_movies()
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
    print(f'The best movie(s): {movie_string(best_movies)}')
    print(f'The worst movie(s): {movie_string(worst_movies)}')


def print_random_movie():
    """Function selects random movie from a database and prints it
    :return: None
    """
    data = movie_storage.list_movies()
    titles = list(data.keys())
    random_title = titles[random.randint(0, len(titles) - 1)]
    rating = data[random_title]['rating']
    print(f"Your movie for tonight: {random_title}, it's rated {rating}")


def search_movie():
    """Function searches movies matching user input criteria
    :return: None
    """
    data = movie_storage.list_movies()
    search_param = input('Enter part of movie name: ')
    found_movies = []
    for title in data.keys():
        if search_param.lower() in title.lower():
            found_movies.append(title)
    if not found_movies:
        print('There are no movies matching your request.')
    elif len(found_movies) == 1:
        print(f'One movie found matching your request: {movie_string(found_movies)}')
    else:
        print(f'List of found movies:{movie_string(found_movies)}')


def print_sorted_by_rating():
    """Function prints all movies from a database sorted by theirs rating
    :return: None
    """
    data = movie_storage.list_movies()
    movies_list = sorted(data.items(), key=lambda item: item[1]['rating'], reverse=True)
    titles = []
    for movie in movies_list:
        titles.append(movie[0])
    print(f'Movies sorted by rating: {movie_string(titles)}')


def print_sorted_by_year():
    """Function prints all movies from a database sorted by release year
    :return: None
    """
    data = movie_storage.list_movies()
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
    print(f'Movies sorted by year: {movie_string(titles)}')


def movie_filters_range(extreme):
    """Function gets a minimum or maximum rating for movies filter
    :param extreme: string ('minimum' or 'maximum')
    :return: float
    """
    if extreme == "minimum":
        edge = MIN_RATING
    else:
        edge = MAX_RATING
    while True:
        user_input = input(f'Enter {extreme} rating '
                           f'(leave blank for no {extreme} rating): ').strip()
        if not user_input:
            return edge
        try:
            result = float(user_input)
            if MIN_RATING < result < MAX_RATING:
                return result
            raise ValueError
        except ValueError:
            print(f'Excepted a number between {MIN_RATING} and {MAX_RATING}')


def movie_filters_year(extreme):
    """Function gets a start or end year for movies filter
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


def filter_movies():
    """Function asks user to enter minimum, maximum rating, start and end year.
    Prints lis of movies, matching entered criteria.
    :return: None
    """
    data = movie_storage.list_movies()
    filtered_movies = []
    # Getting user input
    min_rating = movie_filters_range("minimum")
    max_rating = movie_filters_range("maximum")
    start_year = movie_filters_year("start")
    end_year = movie_filters_year("end")
    # creating list of filtered movies and printing the movies
    for movie, info in data.items():
        if (min_rating <= info['rating'] <= max_rating
                and start_year <= info['year'] <= end_year):
            filtered_movies.append(movie)
    if not filtered_movies:
        print('No movies matching your filter')
    else:
        print('Filtered movies:')
        print(movie_string(filtered_movies))


def print_header(text='My Movies Database'):
    """Function prints header of the program
    :return: None
    """
    print('*' * 5, text, '*' * 5)


def print_menu():
    """Function prints user menu
    :return: None
    """
    menu_items = []
    print('\nMenu:')
    for item in function_list:
        menu_items.append(item)
        print(f'\t{item}')


def dispatcher():
    """Dispatcher function. Calls a list of functions, that draw user interface
    and calls functions based on the user input in a constant loop
    :return: None
    """
    print_header()
    while True:
        print_menu()
        last_menu_item = len(function_list) - 1
        try:
            menu_item = int(input(f'\nEnter choice (0 - {last_menu_item}): '))
            if menu_item < 0 or menu_item > len(function_list) - 1:
                raise ValueError
        except ValueError:
            print('Invalid choice')
            continue
        if not menu_item:
            print('Bye!')
            break
        list(function_list.values())[menu_item]()
        input('\nPress "Enter" to continue')
        continue


def main():
    """Function populates function_list dictionary and calls dispatcher function
    :return: None
    """
    function_list['0. Exit'] = "exit_loop"
    function_list['1. List movies'] = list_movies
    function_list['2. Add movie'] = add_movie
    function_list['3. Delete movie'] = delete_movie
    function_list['4. Update movie'] = update_movie
    function_list['5. Stats'] = print_stats
    function_list['6. Random movie'] = print_random_movie
    function_list['7. Search movie'] = search_movie
    function_list['8. Movies sorted by rating'] = print_sorted_by_rating
    function_list['9. Movies sorted by year'] = print_sorted_by_year
    function_list['10. Filter movies'] = filter_movies
    dispatcher()


if __name__ == '__main__':
    main()
