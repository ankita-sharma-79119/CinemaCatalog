import functools
from flask import (
    render_template, 
    session, 
    Blueprint, 
    redirect, 
    request,
    current_app,
    url_for)
from movie_library.src.models.movie import Movie
from movie_library.src.models.featured import Featured


pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)

# Main Homepage Route
@pages.route("/")
def homepage():
    if session.get("theme") is not None:
        theme = session["theme"]
        session["theme"] = theme
    else:
        session["theme"] = "light"
    featured_movies_db = current_app.db.featured_movies.find({"$expr": { "$lt": [0.4, {"$rand": {} } ] }})
    featured_movies = [Featured(**movie) for movie in featured_movies_db]

    movie_data = current_app.db.movie.find({}, {'_id': 0})
    movies = [Movie(**movie_obj) for movie_obj in movie_data]
    return render_template("index.html", 
                            title = "CinemaCatalog",
                            movies_data = movies,
                            feature_movies = featured_movies)

# Toggle style theme
@pages.route("/toggle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if(current_theme == "dark"):
        session["theme"] = "light"
    else:
        session["theme"] = "dark"

    return redirect(request.args.get("current_page"))