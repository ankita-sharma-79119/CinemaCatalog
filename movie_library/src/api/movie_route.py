import datetime
import uuid
import functools
from dataclasses import asdict

from flask import (
    Blueprint, 
    current_app, 
    redirect, 
    render_template,
    request,
    url_for,
    session
)
from movie_library.src.models.forms import ( 
    ExtendedMovieForm, 
    MovieForm
)
from movie_library.src.models.movie import Movie

movie_route = Blueprint("movie_route", __name__, static_folder='static', template_folder='templates')

# Define a login required method
def login_required(movie_route):
    @functools.wraps(movie_route)
    def route_wrapper(*args, **kwargs):
        if session.get("email") is None:
            return redirect(url_for('user_route.login'))
        else:
            return movie_route(*args, **kwargs)
    return route_wrapper


# Add Movie Route
@movie_route.route("/add/movie", methods=["GET", "POST"])
@login_required
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        movie_data = Movie(
            movie_Id=uuid.uuid4().hex,
            name = form.name.data,
            director=form.director.data,
            year=form.year.data
        )
        current_app.db.movie.insert_one(asdict(movie_data))

        return redirect(url_for('pages.homepage'))
    
    return render_template("add_movie.html", 
                           title = "CinemaCatalog - Add Movie",
                           form = form)

# View a movie details
@movie_route.get("/movie/<string:id>")
def movie(id: str):
    movie_data = list(current_app.db.movie.find({"movie_Id": id}, {'_id': 0}))
    movie = Movie(**movie_data[0])
    return render_template("movie_details.html", movie=movie)

# Rate a movie
@movie_route.route("/movie/rate/<string:id>", methods=["GET"])
@login_required
def rate_movie(id):
    rating = int(request.args.get("rating"))
    current_app.db.movie.update_one({"movie_Id": id}, {"$set": {"rating": rating}})
    return redirect(url_for(".movie", id=id))

# Update last watched of movie
@movie_route.route("/movie/last_watched/<string:id>", methods=["GET"])
@login_required
def last_watched_update(id):
    current_app.db.movie.update_one({"movie_Id": id}, {"$set": {"last_watched": datetime.datetime.today()}})
    return redirect(url_for(".movie", id=id))

# Edit details of movie
@movie_route.route("/edit/movie/<string:id>", methods=["GET", "POST"])
@login_required
def edit_movie(id):
    movie_data = list(current_app.db.movie.find({"movie_Id": id}, {'_id': 0}))
    movie = Movie(**movie_data[0])
    form = ExtendedMovieForm(obj=movie)
    if form.validate_on_submit():
        movie.name = form.name.data
        movie.writers = form.writers.data
        movie.year = form.year.data
        movie.cast = form.cast.data
        movie.plot = form.plot.data
        movie.genres = form.genre.data
        movie.video_link = form.video_link.data

        current_app.db.movie.update_one({"movie_Id": id}, {"$set": asdict(movie)})
        return redirect(url_for(".movie", id=movie.movie_Id))
    
    return render_template("movie_form.html", movie=movie, form=form)

