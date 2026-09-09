
from flask import Flask
app = Flask(__name__)

movies = {
    "M101": {
        "title": "RRR",
        "director": "S. S. Rajamouli",
        "language": "Telugu",
        "genre": "Action",
        "rating": 8,
        "year": 2022
    },
    "M102": {
        "title": "Pushpa",
        "director": "Sukumar",
        "language": "Telugu",
        "genre": "Action",
        "rating": 7,
        "year": 2021
    },
    "M103": {
        "title": "Jersey",
        "director": "Gowtam Tinnanuri",
        "language": "Telugu",
        "genre": "Drama",
        "rating": 9,
        "year": 2019
    },
    "M104": {
        "title": "Bahubali",
        "director": "S. S. Rajamouli",
        "language": "Telugu",
        "genre": "Action",
        "rating": 9,
        "year": 2015
    },
    "M105": {
        "title": "KGF",
        "director": "Prashanth Neel",
        "language": "Kannada",
        "genre": "Action",
        "rating": 8,
        "year": 2018
    },
    "M106": {
        "title": "3 Idiots",
        "director": "Rajkumar Hirani",
        "language": "Hindi",
        "genre": "Comedy",
        "rating": 9,
        "year": 2009
    }
}

### LEVEL 1
@app.route("/")
def home():
    return "Welcome to Movie Finder"

### LEVEL 2
@app.route("/movies")
def all_movies():
    return movies

### LEVEL 3
@app.route("/movies/id=<string:movie_id>")
def find_movie(movie_id):
    if movie_id in movies:
        return movies[movie_id]
    return "Movie not found"


# LEVEL 4
@app.route("/movies/director=<string:director_name>")
def find_director(director_name):
    result = []
    for movie in movies.values():
        if movie["director"].lower() == director_name.lower():
            result.append(movie["title"])
    if result:
        return "<br>".join(result)
    return "No movies found"

# LEVEL 5
@app.route("/movies/rating=<int:rating>")
def find_rating(rating):
    result = []
    for movie in movies.values():
        if movie["rating"] == rating:
            result.append(movie["title"])
    if result:
        return "<br>".join(result)
    return "No movies found"


# LEVEL 6
@app.route("/movies/language=<string:language>")
def find_language(language):
    result = []
    for movie in movies.values():
        if movie["language"].lower() == language.lower():
            result.append(movie["title"])
    if result:
        return "<br>".join(result)
    return "No movies found"


# LEVEL 7
@app.route("/movies/genre=<string:genre>")
def find_genre(genre):
    result = []
    for movie in movies.values():
        if movie["genre"].lower() == genre.lower():
            result.append(movie["title"])
    if result:
        return "<br>".join(result)
    return "No movies found"


# LEVEL 8
@app.route("/movies/year=<int:year>")
def find_year(year):
    result = []
    for movie in movies.values():
        if movie["year"] == year:
            result.append(movie["title"])
    if result:
        return "<br>".join(result)
    return "No movies found for this year"


# LEVEL 9
@app.route("/movies/language=<string:language>/genre=<string:genre>")
def language_genre(language, genre):
    result = []
    for movie in movies.values():
        if (movie["language"].lower() == language.lower()
                and movie["genre"].lower() == genre.lower()):
            result.append(movie["title"])
    if result:
        return "<br>".join(result)
    return "No movies found"

if __name__ == "__main__":
    app.run(debug=True)

