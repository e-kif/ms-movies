# MS-Movies

## About the project
This is a personal movies database program, written as an assignment in Software Engineer Bootcamp.

It supposed to store and use persistent movies database as a JSON or a CSV file.

User menu gives following options: 

1. **List movies** - *lists all movies from a database*
2. **Add movie** - *adds a movie to a database*
3. **Delete movie** - *deletes a movie from a database*
4. **Update movie** - *add or rewrite personal notes about a movie*
5. **Stats** - *prints statistics of a database*
6. **Random movie** - *suggests a random movie*
7. **Search movie** - *search movie(s) in a database matching user search frase*
8. **Movies sorted by rating** - *prints all movies ordered by ratings*
9. **Movies sorted by year** - *prints all movies ordered by release year*
10. **Filter movies** - *prints movies filtered by rating and release year*
11. **Generate a website** - *creates an HTML file with all movies from a database*
12. **Update movies info** - *rewrites release year, rating and poster url in database with info from api*

## How to set up
Install all required modules, get your own api on [OMDb API website](https://www.omdbapi.com/), set it up in your '.env' file: 

>API_KEY="%your_api_key%"

## How to use

Run `main.py` file. You can also pass a data file as command line argument: `python3 main.py data/mike.json`