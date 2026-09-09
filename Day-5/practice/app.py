from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory movies database from Day-3
movies = {
    "M101": {
        "title": "RRR",
        "director": "S.S.Rajamouli",
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

# Level 1: Home Page
@app.route("/")
def home():
    return render_template("home.html")

# Final Challenge: Movie Finder Dashboard
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Level 2: Display Movies Using Template
@app.route("/movies")
def view_movies():
    return render_template("movies.html", movies=movies)

# Level 3 & Level 4: Search Movie (GET vs POST)
@app.route("/search", methods=["GET", "POST"])
def search():
    movie = None
    searched = False
    if request.method == "POST":
        searched = True
        movie_id = request.form.get("movie_id", "").strip()
        movie = movies.get(movie_id)
    return render_template("search.html", movie=movie, searched=searched)

# Level 5: Director Search Form (Case-Insensitive)
@app.route("/director-search", methods=["GET", "POST"])
def director_search():
    results = []
    director_name = ""
    searched = False
    if request.method == "POST":
        searched = True
        director_name = request.form.get("director", "").strip()
        for movie in movies.values():
            if movie["director"].lower() == director_name.lower():
                results.append(movie["title"])
    return render_template("director_search.html", results=results, director=director_name, searched=searched)

# Level 6: Language Search Form (Case-Insensitive)
@app.route("/language-search", methods=["GET", "POST"])
def language_search():
    results = []
    language_name = ""
    searched = False
    if request.method == "POST":
        searched = True
        language_name = request.form.get("language", "").strip()
        for movie in movies.values():
            if movie["language"].lower() == language_name.lower():
                results.append(movie["title"])
    return render_template("language_search.html", results=results, language=language_name, searched=searched)

# Level 7: Rating Search Form (String to Int Conversion)
@app.route("/rating-search", methods=["GET", "POST"])
def rating_search():
    results = []
    searched = False
    error = None
    if request.method == "POST":
        searched = True
        rating_input = request.form.get("rating", "").strip()
        try:
            target_rating = int(rating_input)
            for movie in movies.values():
                if movie["rating"] == target_rating:
                    results.append(movie["title"])
        except ValueError:
            error = "Rating must be an integer"
    return render_template("rating_search.html", results=results, searched=searched, error=error)

# Level 8, 9 & 10: Add Movie with Validation & PRG Pattern
@app.route("/add-movie", methods=["GET", "POST"])
def add_movie():
    error = None
    if request.method == "POST":
        movie_id = request.form.get("movie_id", "").strip()
        title = request.form.get("title", "").strip()
        director = request.form.get("director", "").strip()
        language = request.form.get("language", "").strip()
        genre = request.form.get("genre", "").strip()
        rating_raw = request.form.get("rating", "").strip()
        year_raw = request.form.get("year", "").strip()

        # Level 10 Validations
        if movie_id in movies:
            error = "Movie ID already exists"
        elif not title:
            error = "Title cannot be empty"
        else:
            try:
                rating = int(rating_raw)
            except ValueError:
                error = "Rating must be a number"

            if not error:
                try:
                    year = int(year_raw)
                except ValueError:
                    error = "Year must be a number"

        if not error:
            movies[movie_id] = {
                "title": title,
                "director": director,
                "language": language,
                "genre": genre,
                "rating": rating,
                "year": year
            }
            # Level 9: Post-Redirect-Get pattern
            return redirect(url_for("view_movies"))

    return render_template("add_movie.html", error=error)

# Level 11: Delete Movie
@app.route("/delete-movie", methods=["GET", "POST"])
def delete_movie():
    message = None
    if request.method == "POST":
        movie_id = request.form.get("movie_id", "").strip()
        if movie_id in movies:
            del movies[movie_id]
            return redirect(url_for("view_movies"))
        else:
            message = "Movie not found"
    return render_template("delete_movie.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)